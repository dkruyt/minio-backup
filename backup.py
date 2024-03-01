import os
import tarfile
import datetime
from minio import Minio
from threading import Thread


# Function to log messages with timestamp.
def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}", flush=True)
      
class SimpleProgress(Thread):
    def __init__(self, total_size):
        Thread.__init__(self)
        self.total_size = total_size
        self.uploaded_size = 0

    def update(self, size):
        self.uploaded_size += size
        percentage = (self.uploaded_size / self.total_size) * 100
        log("Progress: {:.2f}%".format(percentage))

    def set_meta(self, total_length=None, object_name=None):
        if total_length:
            self.total_size = total_length
    
# MinIO settings from environment variables.
MINIO_URL = os.getenv('MINIO_URL', 'http://localhost:9000')
ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioAccessKey')
SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioSecretKey')
BUCKET = os.getenv('MINIO_BUCKET', 'my_bucket')


# Initialize MinIO Client.
minio_client = Minio(
    MINIO_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=True
)
  
log("MinIO client initialized")

# Create bucket if not exists.
try:
    found = minio_client.bucket_exists(BUCKET)
    if not found:
        minio_client.make_bucket(BUCKET)
        log(f"Bucket '{BUCKET}' created")
except Exception as e:
    log(f"Failed to create or check bucket '{BUCKET}': {e}")
    exit(1)

# Path to directory to backup.
backup_path = '/backup'

# List directories inside `/opt`.
for item in os.listdir(backup_path):
    dir_path = os.path.join(backup_path, item)
    if os.path.isdir(dir_path):
        # Create a tar.gz file of the directory.
        tar_path = f"/tmp/{item}.tar.gz"
        log(f"Creating tarball for '{item}' at '{tar_path}'")
        with tarfile.open(tar_path, "w:gz") as tar:
            tar.add(dir_path, arcname=item)

        # Get the size of the tar file.
        tar_size = os.path.getsize(tar_path)            
        log(f"Starting upload of '{item}.tar.gz'")
        try:
            progress = SimpleProgress(tar_size)
            minio_client.fput_object(
                BUCKET, f"{item}.tar.gz", tar_path,
                progress=progress,
            )
            log(f"Upload completed: {item}.tar.gz ({tar_size} bytes)")
        except Exception as e:
            log(f"Failed to upload backup '{item}.tar.gz': {e}")

        # Remove the local backup file.
        os.remove(tar_path)

log("Backup completed")
