import os

from google.cloud import storage


class GcsManager:
    def __init__(self):
        """
        Initialize the GcsManager with a Google Cloud Storage client.
        """
        self.storage_client = storage.Client()

    def upload_to_gcs(self, source_directory, bucket_name, destination_prefix):
        """
        Upload the contents of a local directory to a GCS bucket.

        Args:
            source_directory (str): The local directory to upload.
            bucket_name (str): The name of the GCS bucket.
            destination_prefix (str): The prefix (folder) in the bucket where files will be uploaded.
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)

            for root, _, files in os.walk(source_directory):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, source_directory)
                    blob_path = os.path.join(destination_prefix, relative_path)

                    blob = bucket.blob(blob_path)
                    blob.upload_from_filename(local_path)

                    print(f"Uploaded {local_path} to gs://{bucket_name}/{blob_path}")
        except Exception as e:
            print(f"Error while uploading to GCS: {e}")
            raise
