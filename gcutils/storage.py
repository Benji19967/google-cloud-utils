from typing import Generator

from google.cloud.storage import Blob, Bucket
from google.cloud.storage.client import Client

from gcutils.exceptions import BlobNotFound

# TODO: Should I throw errors in JSON format so they are easier to analyze downstream?


# TODO: Add retry
class GCStorageClient:
    _BUCKETS: dict[str, Bucket] = {}

    def __init__(self, client: Client) -> None:
        self._client: Client = client
        if not self._client.project:
            raise ValueError("`project` needs to be set for Client")

    def list_buckets(self, prefix: str | None) -> Generator[Bucket, None, None]:
        for bucket in self._client.list_buckets(prefix=prefix):
            yield bucket

    def get_bucket(self, bucket_or_name: Bucket | str) -> Bucket:
        if isinstance(bucket_or_name, Bucket):
            return bucket_or_name
        if bucket_or_name in self._BUCKETS:
            return self._BUCKETS[bucket_or_name]
        return self._client.get_bucket(bucket_or_name=bucket_or_name)

    def list_blobs(
        self, bucket_or_name: Bucket | str, prefix: str | None, limit: int | None
    ) -> Generator[Blob, None, None]:
        bucket = self.get_bucket(bucket_or_name=bucket_or_name)
        for blob in bucket.list_blobs(prefix=prefix, max_results=limit):
            yield blob

    def get_blob(self, bucket_or_name: Bucket | str, blob_name: str) -> Blob:
        bucket = self.get_bucket(bucket_or_name=bucket_or_name)
        blob: Blob | None = bucket.get_blob(blob_name=blob_name)
        if not blob:
            raise BlobNotFound(
                f"Could not find Blob with name: {blob_name} in bucket: {bucket.name}"
            )
        return blob
