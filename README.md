# LITREVIEW

## Installation

Voici les quelques étapes à suivre pour que vous puissiez pleinement tester le
projet. À la racine du projet :

- Exécutez `pip install pipenv` pour installer Pipenv si ce n'est pas déjà fait.
- Lancez `pipenv install` pour créer un environnement virtuel et installer les dépendances.
- Activez l'environnement virtuel avec `pipenv shell`.

Ici une base de données locale est déjà présente, mais si vous souhaitiez
repartir de 0 :

- `python manage.py makemigrations` pour s'assurer qu'il ne manque aucune
  migration dans le projet
- `python manage.py migrate` pour effectuer les migrations et créer la base de
  données locale

Pour créer un superuser:

- `python manage.py createsuperuser`puis suivre les instructions sur le
  terminal

## Lancement de l'application

Pour pouvoir tester le projet en local, à la racine du projet :

- `python manage.py runserver`

Assurez-vous de créer un utilisateur:
```http request
    http://127.0.0.1:8000/api/users/signup/
```
et de vous connecter avec vos credentials : 
```http request
    http://127.0.0.1:8000/api/users/login/
```
afin de récupérer le token qui vous permettra d'effectuer les différentes requêtes sur TOUS les autress endpoint,
il s'agit d'un Bearer JWT, il doit être ajouté dans le Header `Authorization` 

Enjoy :D

------------ 

# LITREVIEW

## Installation

Here are the steps to follow to fully test the project. At the root of the project:

- Run `pip install pipenv` to install Pipenv if it's not already installed.
- Execute `pipenv install` to create a virtual environment and install dependencies.
- Activate the virtual environment using `pipenv shell`.

Here, a local database is already present, but if you wish to start from
scratch:

- `python manage.py makemigrations` to ensure no migrations are missing in the
  project
- `python manage.py migrate` to perform the migrations and create the local
  database

To create a superuser:

- `python manage.py createsuperuser` then follow the instructions in the
  terminal

## Launching the Application

To test the project locally, at the root of the project:

- `python manage.py runserver`

Ensure you create a user:
```http request
    http://127.0.0.1:8000/api/users/signup/
```
and then log in with your credentials:
```http request
    http://127.0.0.1:8000/api/users/login/
```
to retrieve the token that will allow you to perform requests on ALL other endpoints.
It is a Bearer JWT, which must be added in the `Authorization` Header.

Enjoy :D
```
