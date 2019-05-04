# jengu
ERP for independent therapist

## Usage

### clone this repo

```
git clone https://github.com/ZarebskiDavid/jengu.git
cd jengu
```

### add environement files for production

You will need two files at the root of the project: 

**.env**

```
DEBUG=0
SECRET_KEY=some_secret_key_of_your_choice
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

```
sudo docker-compose -f docker-compose.prod.yml up -d --build
```

for migrations (i.e. django migrations and custom sql functions and triggers)

```
sudo docker-compose -f docker-compose.prod.yml exec web sh migrate.sh
```