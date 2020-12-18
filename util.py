import os
import attr
from pathlib import Path
import urllib
import streamlit as st
import gdown



@attr.s(auto_attribs=True, frozen=True)
class RemoteData:
    filename: str = "my_file.exr"
    url: str = "https://path/to/resource.exr"
    size: int = 0

    def download(self, output_dir="."):
        # mostly taken from https://github.com/streamlit/demo-face-gan/blob/master/streamlit_app.py
        root = Path(output_dir).resolve()
        path = root / self.filename

        # Don't download the file twice. (If possible, verify the download using the file length.)
        if os.path.exists(path):
            if not self.size or os.path.getsize(path) == self.size:
                return path

        # These are handles to two visual elements to animate.
        status, progress_bar = None, None
        try:
            status = st.warning("Downloading %s..." % path)

            # handle cases where files hosted on gdrive someitimes fail to download
            if "google.com" in self.url:
                gdown.cached_download(self.url, path=path)

            else:
                progress_bar = st.progress(0)
                with open(path, "wb") as output_file:
                    with urllib.request.urlopen(self.url) as response:
                        length = int(response.info()["Content-Length"])
                        counter = 0.0
                        MEGABYTES = 2.0 ** 20.0
                        while True:
                            data = response.read(8192)
                            if not data:
                                break
                            counter += len(data)
                            output_file.write(data)

                            # We perform animation by overwriting the elements.
                            status.warning("Downloading %s... (%6.2f/%6.2f MB)" %
                                (path, counter / MEGABYTES, length / MEGABYTES))
                            progress_bar.progress(min(counter / length, 1.0))

        # Finally, we remove these visual elements by calling .empty().
        finally:
            if status is not None:
                status.empty()
            if progress_bar is not None:
                progress_bar.empty()