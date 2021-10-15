from typing import Any, Dict

import dask.dataframe as dd
from kedro.pipeline import node, Pipeline


def compute_null_counts(df: dd.DataFrame) -> Dict[str, Any]:
    return {
        column: int(df[column].isna().sum().compute())
        for column in df.columns
    }

def compute_unique_counts(df: dd.DataFrame) -> Dict[str, Any]:
    return {
        column: len(df[column].unique().compute())
        for column in df.columns
    }

def compute_most_frequent_streamer(df: dd.DataFrame) -> Dict[str, Any]:
    user_value_counts = df.userid.value_counts().compute()
    
    return {
        "userid": str(user_value_counts.idxmax()),
        "streams": int(user_value_counts.max())
    }

pipeline = Pipeline([
    node(
        compute_null_counts,
        name="compute_null_counts",
        inputs="streams",
        outputs="streams_column_null_counts"
    ),
    node(
        compute_unique_counts,
        name="compute_unique_counts",
        inputs="streams",
        outputs="streams_column_unique_counts"
    ),
    node(
        compute_most_frequent_streamer,
        name="compute_most_frequent_streamer",
        inputs="streams",
        outputs="most_frequent_streamer"
    )
])