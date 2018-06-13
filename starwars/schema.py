from __future__ import unicode_literals
import graphene
from graphene import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.debug import DjangoDebug

import starwars.models as models


class Connection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        return self.length


class Person(DjangoObjectType):
    '''An individual person or character within the Star Wars universe.'''
    class Meta:
        model = models.People
        exclude_fields = ('created', 'edited')
        filter_fields = ('name', )
        interfaces = (Node, )
        connection_class = Connection


class Planet(DjangoObjectType):
    '''A large mass, planet or planetoid in the Star Wars Universe,
    at the time of 0 ABY.'''
    climates = graphene.List(graphene.String)
    terrains = graphene.List(graphene.String)

    def resolve_climates(self, info):
        return [c.strip() for c in self.climate.split(',')]

    def resolve_terrains(self, info):
        return [c.strip() for c in self.terrain.split(',')]

    class Meta:
        model = models.Planet
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'climate', 'terrain')
        filter_fields = ('name', )
        connection_class = Connection


class Film(DjangoObjectType):
    '''A single film.'''
    producers = graphene.List(graphene.String)

    def resolve_producers(self, info):
        return [c.strip() for c in self.producer.split(',')]

    class Meta:
        model = models.Film
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'producer')
        filter_fields = {'episode_id': ('gt', )}
        connection_class = Connection


class Specie(DjangoObjectType):
    '''A type of person or character within the Star Wars Universe.'''
    eye_colors = graphene.List(graphene.String)
    hair_colors = graphene.List(graphene.String)
    skin_colors = graphene.List(graphene.String)

    def resolve_eye_colors(self, info):
        return [c.strip() for c in self.eye_colors.split(',')]

    def resolve_hair_colors(self, info):
        return [c.strip() for c in self.hair_colors.split(',')]

    def resolve_skin_colors(self, info):
        return [c.strip() for c in self.skin_colors.split(',')]

    class Meta:
        model = models.Species
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'eye_colors', 'hair_colors',
                          'skin_colors')
        filter_fields = {'name': {'startswith', 'contains'}}
        connection_class = Connection


class Vehicle(DjangoObjectType):
    '''A single transport craft that does not have hyperdrive capability'''
    manufacturers = graphene.List(graphene.String)

    def resolve_manufacturers(self, info):
        return [c.strip() for c in self.manufacturer.split(',')]

    class Meta:
        model = models.Vehicle
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'manufacturers')
        filter_fields = {'name': {'startswith'}}
        connection_class = Connection


class Hero(DjangoObjectType):
    '''A hero created by fans'''

    class Meta:
        model = models.Hero
        interfaces = (Node, )
        exclude_fields = ('created', 'edited')
        filter_fields = {'name': {'startswith', 'contains'}}
        connection_class = Connection


class Starship(DjangoObjectType):
    '''A single transport craft that has hyperdrive capability.'''
    manufacturers = graphene.List(graphene.String)

    def resolve_manufacturers(self, info):
        return [c.strip() for c in self.manufacturer.split(',')]

    def resolve_max_atmosphering_speed(self, info):
        if self.max_atmosphering_speed == 'n/a':
            return None
        return self.max_atmosphering_speed

    class Meta:
        model = models.Starship
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'manufacturers')
        filter_fields = {'name': {'startswith', 'contains'}}
        connection_class = Connection


class Query(graphene.ObjectType):
    all_films = DjangoFilterConnectionField(Film)
    all_species = DjangoFilterConnectionField(Specie)
    all_characters = DjangoFilterConnectionField(Person)
    all_vehicles = DjangoFilterConnectionField(Vehicle)
    all_planets = DjangoFilterConnectionField(Planet)
    all_starships = DjangoFilterConnectionField(Starship)
    all_heroes = DjangoFilterConnectionField(Hero)
    film = Node.Field(Film)
    specie = Node.Field(Specie)
    character = Node.Field(Person)
    vehicle = Node.Field(Vehicle)
    planet = Node.Field(Planet)
    starship = Node.Field(Starship)
    hero = Node.Field(Hero)
    node = Node.Field()
    viewer = graphene.Field(lambda: Query)

    debug = graphene.Field(DjangoDebug, name='__debug')

    def resolve_viewer(self, info):
        return self


class CreateHero(graphene.ClientIDMutation):

    class Input:
        name = graphene.String(required=True)
        homeworld_id = graphene.String(required=True)

    hero = graphene.Field(Hero)
    ok = graphene.Boolean()

    def mutate_and_get_payload(self, info, name, homeworld_id, client_id_mutation=None):
        try:
            homeworld_id = int(homeworld_id)
        except ValueError:
            try:
                _type, homeworld_id = Node.from_global_id(homeworld_id)
                assert _type == 'planet', 'The homeworld should be a Planet, but found {}'.format(resolved.type)
            except:
                raise Exception("Received wrong Planet id: {}".format(homeworld_id))

        homeworld = Planet._meta.model.objects.get(id=homeworld_id)
        hero = Hero._meta.model(name=name, homeworld=homeworld)
        hero.save()

        return CreateHero(hero=hero, ok=bool(hero.id))


class Mutation(graphene.ObjectType):
    create_hero = CreateHero.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
