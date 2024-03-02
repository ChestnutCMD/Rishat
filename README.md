docker-compose up -d
docker ps

CONTAINER ID   IMAGE                  COMMAND                  CREATED         STATUS                   PORTS                              NAMES
<container name>   tetstapi-api           "bash entrypoint.sh …"   6 minutes ago   Up 6 minutes             0.0.0.0:7000->7000/tcp, 8000/tcp   tetstapi-api-1
8339d725393c   postgres:13.0-alpine   "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes (healthy)   0.0.0.0:5432->5432/tcp             tetstapi-postgres-1


docker exec -it <container name> bash 
python manage.py createsuperuser
