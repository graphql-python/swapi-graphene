# GraphQL SWAPI using Graphene 

This is a integration example of [Graphene](http://graphene-python.org) in Django.
[View demo](http://swapi.graphene-python.org/)


## Structure

All the [models](./starwars/models.py) and [fixtures](./starwars/fixtures/) are based in the original [swapi project](https://github.com/phalt/swapi).

The schema (*where all the magic happens*) is in [starwars/schema.py](./starwars/schema.py).
> Look ma, a GraphQL integration with Django models in less than 150 LOC!


## Deploying locally

You can also have your own GraphQL Starwars example running on locally.
Just run the following commands and you'll be all set!

```bash
git clone git@github.com:graphql-python/swapi-graphene.git
cd swapi-graphene

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

**For querying the schema we recomend using [/graphiql](http://localhost:8080/graphiql)**


## Deploying on [Heroku](http://heroku.com)

To get your own GraphQL Starwars example running on Heroku, click the button below:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/graphql-python/swapi-graphene)

Fill out the form, and you should be cooking with gas in a few seconds.
