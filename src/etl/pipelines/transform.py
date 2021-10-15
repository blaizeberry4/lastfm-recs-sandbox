from datetime import datetime, timedelta
from uuid import uuid4

from kedro.pipeline import node, Pipeline
import dask.dataframe as dd
import pandas as pd


def compute_sessions(df: pd.DataFrame) -> pd.DataFrame:
    df_sorted = df.sort_values(by='timestamp', ascending=True)
    df_sorted["delta"] =  df_sorted.timestamp - df_sorted.timestamp.shift(1)

    session_ids = [str(uuid4())]
    for delta in df_sorted["delta"][1:]:
        if delta < timedelta(minutes=20):
            session_ids.append(session_ids[-1])
        else:
            session_ids.append(str(uuid4()))

    df_sorted["session_id"] = session_ids

    return df_sorted.drop(columns=["delta", "userid"])

def compute_partition_sessions(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(df.userid).apply(compute_sessions)

def transform_streams_to_sessions(df: dd.DataFrame) -> dd.DataFrame:
    df.timestamp = df.timestamp.astype('datetime64[ns]')

    return df.set_index(df.userid).map_partitions(compute_partition_sessions)

def transform_sessions_to_most_frequent_tracks(
    df: dd.DataFrame,
    n_longest_sessions: int,
    n_most_frequent_tracks: int
) -> pd.DataFrame:
    longest_sessions = set(
        df
            .session_id
            .value_counts()
            .nlargest(n_longest_sessions)
            .compute()
            .index
    )

    return (
        df
            [df.session_id.isin(longest_sessions)]  # Filter to only include tracks from n longest sessions
            .compute()                              # At this stage, data is tiny to switch to pandas
            .groupby(["artist_name", "track_name"]) # Identify unique tracks
            .size()                                 # Count streams for unique tracks
            .nlargest(n_most_frequent_tracks)        # Take n most frequently streamed in these sessions
            .reset_index(name="play_count")         # pd.Series -> pd.DataFrame with counts as play_count
    )


pipeline = Pipeline([
    node(
        transform_streams_to_sessions,
        name="transform_streams_to_sessions",
        inputs="streams",
        outputs="sessions"
    ),
    node(
        transform_sessions_to_most_frequent_tracks,
        name="transform_sessions_to_most_frequent_tracks",
        inputs=[
            "sessions",
            "params:sessions.n_longest",
            "params:tracks.n_most_played"
        ],
        outputs="most_played_tracks"
    )
])