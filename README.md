# CusSeg
A Customer Segmentation Platform

sudo docker run -p 9000:9000 -p 9001:9001 --name minio \
    -e "MINIO_ROOT_USER=minioadmin" \
    -e "MINIO_ROOT_PASSWORD=minioadmin" \
    -v /path/to/data:/data \
    -v /path/to/config:/root/.minio \
    minio/minio server /data --console-address ":9001"

curl -F "file=@/home/bharathwaj/Documents/Datasets/adult_census.csv" http://localhost:8000/upload

curl -F "file=@/home/bharathwaj/Documents/Datasets/adult_census.csv" "http://localhost:8000/upload?storage=minio"

curl -F "file=@/home/bharathwaj/Downloads/video.mp4" "http://localhost:8000/upload?storage=minio"

curl -F "file=@/home/bharathwaj/Documents/Datasets/adult_census.csv" "http://localhost:8000/upload?storage=hdfs"

curl -X POST http://localhost:8000/webhook \
    -H "Content-Type: application/json" \
    -d '{"event": "user_signed_up", "user_id": 42, "source": "landing_page"}'

curl -H "X-API-Key: key-for-client1" -F "file=@/home/bharathwaj/Documents/Datasets/adult_census.csv" http://localhost:8000/upload

curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"username": "dhanasekar", "email": "dhana@sekar.com", "password": "password"}'

curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=dhanasekar&password=password"

curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=youruser&password=strongpassword"

curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer JWT.TOKEN" \
  -F "file=@/home/bharathwaj/Documents/Datasets/adult_census.csv"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000