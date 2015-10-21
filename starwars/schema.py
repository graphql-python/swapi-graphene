import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import graphene
from graphene import resolve_only_args, relay
from graphene.contrib.django import DjangoNode, DjangoConnectionField

import models


schema = graphene.Schema(name='Starwars Relay Schema')


class Connection(relay.Connection):
    total_count = graphene.IntField()

    def resolve_total_count(self, args, info):
        return len(self.get_connection_data())


class Person(DjangoNode):
    '''An individual person or character within the Star Wars universe.'''
    class Meta:
        model = models.People
        exclude_fields = ('created', 'edited')

    connection_type = Connection


class Planet(DjangoNode):
    '''A large mass, planet or planetoid in the Star Wars Universe,
    at the time of 0 ABY.'''
    climates = graphene.ListField(graphene.StringField())
    terrains = graphene.ListField(graphene.StringField())

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


class Film(DjangoNode):
    producers = graphene.ListField(graphene.StringField())

    connection_type = Connection

    @resolve_only_args
    def resolve_producers(self):
        return [c.strip() for c in self.instance.producer.split(',')]

    '''A single film.'''
    class Meta:
        model = models.Film
        exclude_fields = ('created', 'edited', 'producer')


class Specie(DjangoNode):
    '''A type of person or character within the Star Wars Universe.'''
    eye_colors = graphene.ListField(graphene.StringField())
    hair_colors = graphene.ListField(graphene.StringField())
    skin_colors = graphene.ListField(graphene.StringField())

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
    manufacturers = graphene.ListField(graphene.StringField())

    connection_type = Connection

    @resolve_only_args
    def resolve_manufacturers(self):
        return [c.strip() for c in self.instance.manufacturer.split(',')]

    class Meta:
        model = models.Vehicle
        exclude_fields = ('created', 'edited', 'manufacturers')


class Starship(DjangoNode):
    '''A single transport craft that has hyperdrive capability.'''
    manufacturers = graphene.ListField(graphene.StringField())

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
    all_films = DjangoConnectionField(Film)
    all_species = DjangoConnectionField(Specie)
    all_characters = DjangoConnectionField(Person)
    all_vehicles = DjangoConnectionField(Vehicle)
    all_planets = DjangoConnectionField(Planet)
    all_starships = DjangoConnectionField(Starship)
    film = relay.NodeField(Film)
    specie = relay.NodeField(Specie)
    character = relay.NodeField(Person)
    vehicle = relay.NodeField(Vehicle)
    planet = relay.NodeField(Planet)
    startship = relay.NodeField(Starship)
    node = relay.NodeField()

    @resolve_only_args
    def resolve_all_films(self, **kwargs):
        return models.Film.objects.all()

    @resolve_only_args
    def resolve_all_species(self, **kwargs):
        return models.Species.objects.all()

    @resolve_only_args
    def resolve_all_characters(self, **kwargs):
        return models.People.objects.all()

    @resolve_only_args
    def resolve_all_vehicles(self, **kwargs):
        return models.Vehicle.objects.all()

    @resolve_only_args
    def resolve_all_planets(self, **kwargs):
        return models.Planet.objects.all()

    @resolve_only_args
    def resolve_all_starships(self, **kwargs):
        return models.Starship.objects.all()


schema.query = Query
