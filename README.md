# OCI Object Storage Uploader

This project provides simple Python scripts to **upload files and directories** to Oracle Cloud Infrastructure (OCI) Object Storage using the official `oci` SDK.

## **Prerequisites**
- Python 3.7 or later
- `oci` Python SDK  
  ```bash
  pip install oci

OCI config file set up at ~/.oci/config with a profile named DEFAULT.
Example ~/.oci/config:
```text
[DEFAULT]
user=ocid1.user.oc1..aaaa...
fingerprint=aa:bb:cc:dd:ee:ff
key_file=/home/opc/.oci/oci_api_key.pem
tenancy=ocid1.tenancy.oc1..aaaa...
region=ap-singapore-1
```