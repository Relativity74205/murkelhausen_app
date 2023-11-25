# Murkelhausen App

## Setup

### Running app on beowulf (temporary)

```bash
screen -S murkel -d -m poetry run python manage.py runserver 0.0.0.0:8000
```

accessing the screen session:

```bash
screen -r murkel
```

Killing the screen session:

```bash
screen -X -S murkel quit
```



### Database

```sql
CREATE DATABASE murkelhausen_app;
CREATE USER murkelhausen_app WITH PASSWORD '';
ALTER DATABASE murkelhausen_app OWNER TO murkelhausen_app;
GRANT CONNECT ON DATABASE murkelhausen_datastore TO murkelhausen_app;
GRANT USAGE ON SCHEMA kafka TO murkelhausen_app;
GRANT SELECT ON ALL TABLES IN SCHEMA kafka TO murkelhausen_app;
```