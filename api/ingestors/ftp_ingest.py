import ftplib
import os
import requests

FTP_HOST        = os.getenv("FTP_HOST", 'ftp.dlptest.com')
FTP_USERNAME    = os.getenv("FTP_USERNAME", 'dlpuser')
FTP_PASSWORD    = os.getenv("FTP_PASSWORD", "rNrKYTX9g7z3RgJRmxWuGHbeu")
FTP_DIR         = os.getenv("FTP_DIR", ".")
UPLOAD_URL      = os.getenv("API_UPLOAD_URL", "http://localhost:8000/upload")
ACCESS_TOKEN    = os.getenv("API_ACCESS_TOKEN")  # Store a valid JWT here
FILE_TO_FETCH = "/home/bharathwaj/Documents/Datasets/bank.csv"

def upload_to_api(filename, local_path):
    with open(local_path, "rb") as file:
        resp = requests.post(
            UPLOAD_URL,
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
            files={"file": (filename, file)}
        )
        print(f"Uploaded {filename}: {resp.status_code} {resp.text}")

def main():
    with ftplib.FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        ftp.cwd(FTP_DIR)
        files = ftp.nlst()
        for filename in files:
            local_path = f"/tmp/{filename}"
            with open(local_path, "wb") as f:
                ftp.retrbinary(f"RETR {filename}", f.write)
            upload_to_api(filename, local_path)
            os.remove(local_path)

if __name__ == "__main__":
    main()