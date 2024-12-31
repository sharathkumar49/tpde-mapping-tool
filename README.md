# Mappers Insert Tool

Mappers Insert tool is used to perform data processing using Django Framework

## Installation
Install Python 3.x version
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages which are in requirement.txt file.

```bash
pip install package_name
```

## Project Configuration

```python
git clone remote-url
git checkout -b new_branch_name
```
Change working directory to 'project_name/tpde-mapping-tool/mappers_insert'

```python
# To create a migration file
python manage.py makemigrations

# To create tables in database
python manage.py migrate

# Create superuser and use the username and password to login
python manage.py createsuperuser

# Run django application
python manage.py runserver
```

## Access Application Web

Once run the application, use 
```python
http://127.0.0.1:8000 
```



