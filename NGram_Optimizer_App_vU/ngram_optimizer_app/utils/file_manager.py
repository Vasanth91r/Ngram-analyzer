# File manager (zip outputs) placeholder
import zipfile
import os
import tempfile

def zip_outputs(paths):
    zip_path = os.path.join(tempfile.gettempdir(), "ngram_outputs.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for path in paths:
            arcname = os.path.basename(path)
            zipf.write(path, arcname=arcname)
    return zip_path
