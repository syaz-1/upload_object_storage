import oci
import os
import sys
import time

# ====== OCI CONFIG ======
config = oci.config.from_file("~/.oci/config", "DEFAULT")

# ====== STATIC VARIABLES ======
local_file_path = "/home/opc/myfiles/bigfile.zip"  # <-- Local file to upload
namespace_name = "my-namespace"                    # Replace with your namespace
bucket_name = "my-bucket"                          # Replace with your bucket
destination_object_name = "uploads/bigfile.zip"    # Object name in Object Storage

# ====== INIT CLIENT ======
object_storage_client = oci.object_storage.ObjectStorageClient(config)
upload_manager = oci.object_storage.UploadManager(object_storage_client)

# ====== START TIMER ======
start_time = time.time()

# ====== PROGRESS CALLBACK ======
def progress_callback(bytes_uploaded):
    """Display upload progress, speed, and ETA."""
    elapsed = time.time() - start_time
    speed = bytes_uploaded / elapsed if elapsed > 0 else 0  # Bytes per second
    remaining_bytes = total_size - bytes_uploaded
    eta = remaining_bytes / speed if speed > 0 else 0       # Seconds

    progress = (bytes_uploaded / total_size) * 100
    sys.stdout.write(
        f"\rUploading: {bytes_uploaded:,}/{total_size:,} bytes "
        f"({progress:.2f}%) | Speed: {speed/1024/1024:.2f} MB/s | ETA: {eta:.1f}s"
    )
    sys.stdout.flush()

# ====== UPLOAD FILE ======
try:
    # Check if the file exists
    if not os.path.exists(local_file_path):
        raise FileNotFoundError(f"Local file not found -> {local_file_path}")

    total_size = os.path.getsize(local_file_path)
    print(f"Starting upload for: {local_file_path}")
    print(f"File size: {total_size / (1024*1024):.2f} MB\n")

    # Upload with progress callback
    response = upload_manager.upload_file(
        namespace_name=namespace_name,
        bucket_name=bucket_name,
        object_name=destination_object_name,
        file_path=local_file_path,
        progress_callback=progress_callback  # <-- Progress tracking with ETA
    )

    # Final status
    total_time = time.time() - start_time
    print(f"\n✅ Upload successful! Completed in {total_time:.1f} seconds.")
    print(f"File URL:\nhttps://objectstorage.{config['region']}.oraclecloud.com/n/{namespace_name}/b/{bucket_name}/o/{destination_object_name}")

except FileNotFoundError as fnf_error:
    print(f"❌ {fnf_error}")
except Exception as e:
    print(f"\n❌ Upload failed: {str(e)}")
