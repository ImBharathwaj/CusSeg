# ingestors/sftp_ingest.py
import paramiko
import os
import requests

SFTP_HOST = os.getenv("SFTP_HOST", "ftp.dlptest.com")
SFTP_USERNAME = os.getenv("SFTP_USERNAME", "dlpuser")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD", "rNrKYTX9g7z3RgJRmxWuGHbeu")
SFTP_DIR      = os.getenv("SFTP_DIR", ".")
UPLOAD_URL    = os.getenv("API_UPLOAD_URL", "http://localhost:8000/upload")
ACCESS_TOKEN  = os.getenv("API_ACCESS_TOKEN")

def upload_to_api(filename, local_path):
    with open(local_path, "rb") as file:
        resp = requests.post(
            UPLOAD_URL,
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            files={"file": (filename, file)}
        )
        print(f"Uploaded {filename}: {resp.status_code} {resp.text}")

def main():
    transport = paramiko.Transport((SFTP_HOST, 22))
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    for filename in sftp.listdir(SFTP_DIR):
        remote_path = f"{SFTP_DIR.rstrip('/')}/{filename}"
        local_path = f"/tmp/{filename}"
        sftp.get(remote_path, local_path)
        upload_to_api(filename, local_path)
        os.remove(local_path)
    sftp.close()
    transport.close()

if __name__ == "__main__":
    main()
