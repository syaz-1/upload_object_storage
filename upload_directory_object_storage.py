import oci
import os
import sys
import time

# ====== OCI CONFIG ======
config = oci.config.from_file("~/.oci/config", "DEFAULT")

# ====== VARIABLES ======
local_directory = "/home/opc/myfiles"     # <-- Folder to upload
namespace_name = "my-namespace"           # Replace with your namespace
bucket_name = "my-bucket"                 # Replace with your bucket
destination_prefix = "uploads/"           # Folder path inside bucket

# ====== INIT CLIENT ======
object_storage_client = oci.object_storage.ObjectStorageClient(config)
upload_manager = oci.object_storage.UploadManager(object_storage_client)


# ====== PROGRESS CALLBACK ======
def make_progress_callback(filename, total_size):
    """Create a custom progress callback for each file."""
    start_time = time.time()

    def progress_callback(bytes_uploaded):
        elapsed = time.time() - start_time
        speed = bytes_uploaded / elapsed if elapsed > 0 else 0
        remaining_bytes = total_size - bytes_uploaded
        eta = remaining_bytes / speed if speed > 0 else 0

        progress = (bytes_uploaded / total_size) * 100
        sys.stdout.write(
            f"\r[{filename}] {bytes_uploaded:,}/{total_size:,} bytes "
            f"({progress:.2f}%) | Speed: {speed/1024/1024:.2f} MB/s | ETA: {eta:.1f}s"
        )
        sys.stdout.flush()

    return progress_callback


# ====== UPLOAD FUNCTION ======
def upload_directory(local_directory, namespace_name, bucket_name, destination_prefix):
    """Upload every file in a directory (recursive)."""
    print(f"Starting directory upload: {local_directory}\n")

    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            local_file_path = os.path.join(root, filename)

            # Calculate relative path to preserve folder structure in bucket
            relative_path = os.path.relpath(local_file_path, local_directory)
            object_name = os.path.join(destination_prefix, relative_path).replace("\\", "/")

            total_size = os.path.getsize(local_file_path)

            print(f"\nUploading file: {relative_path} ({total_size / (1024*1024):.2f} MB)")
            try:
                response = upload_manager.upload_file(
                    namespace_name=namespace_name,
                    bucket_name=bucket_name,
                    object_name=object_name,
                    file_path=local_file_path,
                    progress_callback=make_progress_callback(relative_path, total_size)
                )
                print(f"\n✅ Upload complete: {object_name}")

            except Exception as e:
                print(f"\n❌ Failed to upload {relative_path}: {str(e)}")

    print("\nAll files uploaded successfully!")


# ====== RUN UPLOAD ======
upload_directory(local_directory, namespace_name, bucket_name, destination_prefix)
