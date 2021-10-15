import atexit
import shutil
import functools
from io import BytesIO
import tarfile
from tempfile import mkdtemp
from typing import Tuple
from urllib.request import urlopen
from logging import getLogger
from pathlib import Path
import csv


import pandas as pd
import dask.dataframe as dd
from kedro.pipeline import node, Pipeline


logger = getLogger(f"kedro.pipeline.extract")


def extract_archive_from_last_fm(
    uri: str,
    compression: str = None
) -> tarfile.TarFile:
    """ Extracts track and user datasets in a Tar Archive from LastFM.

    Args:
        uri (str): the URI used to fetch the Tar from.
        compression (str, optional): The compression used with the tar archive. Shoud be 
            one of ["gz", "bz2", "xz"] indicating gzip, bzip2, or lzma compression, 
            respectively, or can be None, indicating no compression. Defaults to None.

    Returns:
        tarfile.TarFile: the tarball containing the data.
    """
    if compression is None:
        compression = ""

    read_mode_with_compression = f"r:{compression}"

    with urlopen(uri) as tar_fd:
        tar_bytes = BytesIO(tar_fd.read())

    return tarfile.open(
        fileobj=tar_bytes,
        mode=read_mode_with_compression
    )

def extract_datasets_from_archive(
    archive: tarfile.TarFile,
    streams_filename: str,
    streams_md5: str,
    users_filename: str,
    users_md5: str,
) -> Tuple[dd.DataFrame, pd.DataFrame]:
    """ Extracts track and user datasets from a Tar Archive from LastFM.

    Args:
        archive (tarfile.TarFile): the Tar archive containing the datasets.
        streams_filename (str): the name of the file within the tar containing the streams dataset.
        streams_md5 (str): the md5 hash of the streams_filename (used for validation).
        users_filename (str): the name of the file within the tar containing the streams dataset.
        users_md5 (str): the md5 hash of the users_filename (used for validation).

    Returns:
        Tuple[dd.DataFrame, pd.DataFrame]: the streams dataset and users dataset (in this order) as
            pandas DataFrames.
    """
    tdir = mkdtemp()
    atexit.register(functools.partial(shutil.rmtree, tdir))

    archive.extract(streams_filename, path=tdir)
    archive.extract(users_filename, path=tdir)

    ddf_streams = dd.read_csv(
        Path(tdir, *streams_filename.split("/")),
        sep='\t',
        names=[
            "userid",
            "timestamp",
            "musicbrainz_artist_id",
            "artist_name",
            "musicbrainz_track_id",
            "track_name"
        ],
        quoting=csv.QUOTE_NONE,
        dtype={'musicbrainz_track_id': 'object'},
    )

    df_users = pd.read_csv(
        Path(tdir, *users_filename.split("/")),
        sep='\t',
        names=[
            "userid",
            "gender",
            "age",
            "country",
            "signup"
        ]
    )

    return ddf_streams, df_users


pipeline = Pipeline([
    node(
        extract_archive_from_last_fm,
        inputs=[
            "params:archive.uri",
            "params:archive.compression"
        ],
        outputs="archive",
        name="extract_archive"
    ),
    node(
        extract_datasets_from_archive,
        inputs=[
            "archive",
            "params:archive.streams_filename",
            "params:archive.streams_md5",
            "params:archive.users_filename",
            "params:archive.users_md5"
        ],
        outputs=[
            "streams",
            "users"
        ],
        name="extract_datasets"
    ),
])
