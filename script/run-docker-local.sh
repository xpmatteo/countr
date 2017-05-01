
set -e
#docker build -t dockr:latest .

docker run -it  \
    -p 5000:5000 \
    -e RDS_DB_NAME=countr_dev \
    -e RDS_HOSTNAME=192.168.1.67 \
    -e RDS_PORT=3306 \
    -e RDS_USERNAME=countr \
    -e RDS_PASSWORD=countr \
    dockr:latest
