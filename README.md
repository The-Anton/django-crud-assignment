# Django CRUD Assignment

## Credentials

Staff User - 

```
username - superuser
password - superuser
```

Normal User - 

```
username - normaluser
password - user123!@#
```

Available endpoints - 


```
    api/v1/box/<int:pk> - Retrieve, Update, Delete new boxes 
    api/v1/new-box/ - Create new boxes
    api/v1/available-boxes/ - List all available boxes in the store
    api/v1/staff-boxes/ - list all staff's(current user) boxes in the store
```

Staff is user having staff permissions.

### *Note - You need to provide auth credentials to call these endpoint and filter your results

## Neccessary Steps - 


Create Migrations 

```
cd inventory
python manage.py makemigrations products
python manage.py migrate
```

Create a superuser

```
pythone manage.py createsuperuser
```