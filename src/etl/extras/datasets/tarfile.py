import atexit
import functools
from pathlib import Path
import shutil
import tarfile
from tempfile import mkdtemp
from typing import Any, Dict

from kedro.io import AbstractDataSet


class TarFileDataSet(AbstractDataSet):
    """``TarFileDataSet`` loads / saves a tarball and supports common 
        compression schemes. Manages a temporary copy of the file so that
        member updates/adds/deletes are only persisted after the save operation
        (Python's built in tarfile library only exposes methods that have
        immediate side effects).

    Example:
    ::

        >>> TarFileDataSet(filepath='/img/file/path.tar.gz', compression='gz')
    """

    def __init__(self, filepath: str, compression: str = None):
        """Creates a new instance of TarFileDataSet to load / save image data at the given filepath.

        Args:
            filepath (str): The location of the tar file to load / save data.
            compression (str): The compression of the tar file to load / save data.
        """
        self._filepath = Path(filepath)
        self._compression = compression if compression is not None else ""
        self._tmp_dir = mkdtemp()
        atexit.register(functools.partial(shutil.rmtree, self._tmp_dir))
        self._tmp_tar_path = Path(self._tmp_dir, str(self._filepath).split("/")[-1])

    def _load(self) -> tarfile.TarFile:
        """ Loads the tarball.

        Returns:
            tarfile.Tarfile: the tarball.
        """
        shutil.copy2(self._filepath, self._tmp_tar_path)

        try:
            tar = tarfile.open(
                self._tmp_tar_path,
                mode=f"r:{self._compression}"
            )
        except tarfile.ReadError:
            # Somthing about the save from fileobj method appears to clobber
            # the gzip compression headers. This works fine for this
            # use case, but would be good tech debt to pay down in the future
            # if we were using the TarFileDataSet in other applications.
            tar = tarfile.open(
                self._tmp_tar_path,
                mode="r"
            )
        
        return tar

    def _save(self, data: tarfile.TarFile) -> None:
        """ Saves tarball data to the specified filepath """
        with data:
            fobj = data.fileobj if not data.name else open(data.name)
            with open(self._filepath, "wb") as target:
                shutil.copyfileobj(fobj, target)
        fobj.close()

    def _exists(self) -> bool:
        return self._filepath.is_file()

    def _describe(self) -> Dict[str, Any]:
        return {}
