# yourapp/storage.py
from whitenoise.storage import CompressedManifestStaticFilesStorage

class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def post_process(self, *args, **kwargs):
        try:
            return super().post_process(*args, **kwargs)
        except ValueError as e:
            if 'The file' in str(e) and 'could not be found' in str(e):
                self.stderr.write("Ignoring missing file error: {}".format(e))
                return []
            raise
