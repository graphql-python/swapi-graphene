import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import graphene
from graphene import resolve_only_args, relay
from graphene.contrib.django import DjangoNode, DjangoConnection
from graphene.contrib.django.filter import DjangoFilterConnectionField
from graphene.contrib.django.debug import DjangoDebugPlugin
from graphql_relay.node.node import from_global_id

import models


schema = graphene.Schema(name='Starwars Relay Schema', plugins=[DjangoDebugPlugin()])


class Connection(DjangoConnection):
    total_count = graphene.Int()

    def resolve_total_count(self, args, info):
        return len(self.get_connection_data())


class Person(DjangoNode):
    '''An individual person or character within the Star Wars universe.'''
    class Meta:
        model = models.People
        exclude_fields = ('created', 'edited')
        filter_fields = ('name', )

    connection_type = Connection


class Planet(DjangoNode):
    '''A large mass, planet or planetoid in the Star Wars Universe,
    at the time of 0 ABY.'''
    climates = graphene.String().List
    terrains = graphene.String().List

    connection_type = Connection

    @resolve_only_args
    def resolve_climates(self):
        return [c.strip() for c in self.instance.climate.split(',')]

    @resolve_only_args
    def resolve_terrains(self):
        return [c.strip() for c in self.instance.terrain.split(',')]

    class Meta:
        model = models.Planet
        exclude_fields = ('created', 'edited', 'climate', 'terrain')
        filter_fields = ('name', )


@schema.register
class Film(DjangoNode):
    producers = graphene.String().List

    connection_type = Connection

    @resolve_only_args
    def resolve_producers(self):
        return [c.strip() for c in self.instance.producer.split(',')]

    '''A single film.'''
    class Meta:
        model = models.Film
        exclude_fields = ('created', 'edited', 'producer')
        filter_fields = {'episode_id': ('gt', )}


class Specie(DjangoNode):
    '''A type of person or character within the Star Wars Universe.'''
    eye_colors = graphene.String().List
    hair_colors = graphene.String().List
    skin_colors = graphene.String().List

    connection_type = Connection

    @resolve_only_args
    def resolve_eye_colors(self):
        return [c.strip() for c in self.instance.eye_colors.split(',')]

    @resolve_only_args
    def resolve_hair_colors(self):
        return [c.strip() for c in self.instance.hair_colors.split(',')]

    @resolve_only_args
    def resolve_skin_colors(self):
        return [c.strip() for c in self.instance.skin_colors.split(',')]

    class Meta:
        model = models.Species
        exclude_fields = ('created', 'edited', 'eye_colors', 'hair_colors',
                          'skin_colors')


class Vehicle(DjangoNode):
    '''A single transport craft that does not have hyperdrive capability'''
    manufacturers = graphene.String().List

    connection_type = Connection

    @resolve_only_args
    def resolve_manufacturers(self):
        return [c.strip() for c in self.instance.manufacturer.split(',')]

    class Meta:
        model = models.Vehicle
        exclude_fields = ('created', 'edited', 'manufacturers')
        filter_fields = {'name': {'startswith'}}


class Hero(DjangoNode):
    '''A hero created by fans'''
    connection_type = Connection

    class Meta:
        model = models.Hero
        exclude_fields = ('created', 'edited')
        filter_fields = {'name': {'startswith', 'contains'}}


class Starship(DjangoNode):
    '''A single transport craft that has hyperdrive capability.'''
    manufacturers = graphene.String().List

    connection_type = Connection

    @resolve_only_args
    def resolve_manufacturers(self):
        return [c.strip() for c in self.instance.manufacturer.split(',')]

    @resolve_only_args
    def resolve_max_atmosphering_speed(self):
        if self.instance.max_atmosphering_speed == 'n/a':
            return None
        return self.instance.max_atmosphering_speed

    class Meta:
        model = models.Starship
        exclude_fields = ('created', 'edited', 'manufacturers')


class Query(graphene.ObjectType):
    all_films = DjangoFilterConnectionField(Film)
    all_species = DjangoFilterConnectionField(Specie)
    all_characters = DjangoFilterConnectionField(Person)
    all_vehicles = DjangoFilterConnectionField(Vehicle)
    all_planets = DjangoFilterConnectionField(Planet)
    all_starships = DjangoFilterConnectionField(Starship)
    all_heroes = DjangoFilterConnectionField(Hero)
    film = relay.NodeField(Film)
    specie = relay.NodeField(Specie)
    character = relay.NodeField(Person)
    vehicle = relay.NodeField(Vehicle)
    planet = relay.NodeField(Planet)
    startship = relay.NodeField(Starship)
    hero = relay.NodeField(Hero)
    node = relay.NodeField()
    viewer = graphene.Field('self')

    def resolve_viewer(self, *args, **kwargs):
        return self


class CreateHero(relay.ClientIDMutation):

    class Input:
        name = graphene.String(required=True)
        homeworld_id = graphene.String(required=True)

    hero = graphene.Field(Hero)
    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, input, info):
        name = input.get('name')
        homeworld_id = input.get('homeworld_id')
        assert homeworld_id, 'homeworld_id must be not null'
        try:
            homeworld_id = int(homeworld_id)
        except ValueError:
            try:
                resolved = from_global_id(homeworld_id)
                resolved.type.lower == 'planet', 'The homeworld should be a Planet, but found {}'.format(resolved.type)
                homeworld_id = resolved.id
            except:
                raise Exception("Received wrong Planet id: {}".format(homeworld_id))

        homeworld = Planet._meta.model.objects.get(id=homeworld_id)
        hero = Hero._meta.model(name=name, homeworld=homeworld)
        hero.save()

        return CreateHero(hero=hero, ok=bool(hero.id))


class Mutation(graphene.ObjectType):
    create_hero = graphene.Field(CreateHero)


schema.query = Query
schema.mutation = Mutation
