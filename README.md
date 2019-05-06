# jengu
ERP for independent therapist

## Requirements

* [docker](https://docs.docker.com/install/linux/docker-ce/debian/)
* [docker-compose](https://docs.docker.com/compose/install/)

or you could just use [my script](https://github.com/ZarebskiDavid/server_setting)

## Usage

### Testing and dev

clone this repo
```
git clone https://github.com/ZarebskiDavid/jengu.git
cd jengu
```

run the app
```
docker-compose up -d --build
```

### add environement files for production

You will need two files at the root of the project: 

**.env**

```
DEBUG=0
SECRET_KEY=some_secret_key_of_your_choice
STATIC_FILES_HOST=/usr/local/share/jengu/staticfiles  # leave it this way or change the proxy conf accordingly
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=some_db_name
SQL_USER=some_user_name
SQL_PASSWORD=some_looooooooong_password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```
**.env.db**

```
POSTGRES_USER=some_user_name
POSTGRES_PASSWORD=some_looooooooong_password
POSTGRES_DB=some_db_name
```

### run in production

To run and / or apply change to running containers
```
sudo docker-compose -f docker-compose.prod.yml up -d --build
```

To create a *superuser* (i.e. administrator)

```
sudo docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --username=joe --email=joe@example.com
```

for db migrations (i.e. django migrations and custom sql functions and triggers)

```
sudo docker-compose -f docker-compose.prod.yml exec web sh migrate.sh
```

### Set an Apache Proxy Pass up

```
a2enmod proxy proxy_http rewrite
```