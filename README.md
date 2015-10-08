# GraphQL SWAPI using Graphene 

[Graphene](http://graphene-python.org) is a free, open, simple GraphQL framework for Python.

This is a integration example of Graphene in Django.
[View demo](http://swapi.graphene-python.org/)


## Structure

All the [models](./starwars/models.py) and [fixtures](./starwars/fixtures/) are based in the original [swapi repo](https://github.com/phalt/swapi).

The schema is in [starwars/schema.py](./starwars/schema.py).
> Look ma, a GraphQL integration with Django models in less than 150 LOC!


## Deploying on [Heroku](http://heroku.com)

To get your own GraphQL Starwars example running on Heroku, click the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/graphql-python/django-graphene-example)

Fill out the form, and you should be cooking with gas in a few seconds.

## Deploying locally

You can also have your own GraphQL Starwars example running on locally.
Just run the following commands and you'll be all set!

```bash
git clone git@github.com:graphql-python/django-graphene-example.git
cd django-graphene-example

# Install the requirements
pip install -r requirements_base.txt

# Setup the db and load the fixtures
python manage.py migrate
```

Once you have everything done, just run:

```bash
python manage.py runserver
```

Open your browser and visit [localhost:8080](http://localhost:8080/) et voilá!
