docker-compose --file qiwi-system-docker-compose.yml stop
docker-compose --file tron-system-docker-compose.yml stop
docker-compose --file qiwi-system-docker-compose.yml up --build
docker-compose --file tron-system-docker-compose.yml up --build