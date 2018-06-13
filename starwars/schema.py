import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import graphene
from graphene import resolve_only_args, Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.debug import DjangoDebug

import models


def connection_for_type(_type):
    class Connection(graphene.Connection):
        total_count = graphene.Int()

        class Meta:
            name = _type._meta.name + 'Connection'
            node = _type

        def resolve_total_count(self, args, context, info):
            return self.length

    return Connection


class Person(DjangoObjectType):
    '''An individual person or character within the Star Wars universe.'''
    class Meta:
        model = models.People
        exclude_fields = ('created', 'edited')
        filter_fields = ('name', )
        interfaces = (Node, )

Person.Connection = connection_for_type(Person)


class Planet(DjangoObjectType):
    '''A large mass, planet or planetoid in the Star Wars Universe,
    at the time of 0 ABY.'''
    climates = graphene.List(graphene.String)
    terrains = graphene.List(graphene.String)

    @resolve_only_args
    def resolve_climates(self):
        return [c.strip() for c in self.climate.split(',')]

    @resolve_only_args
    def resolve_terrains(self):
        return [c.strip() for c in self.terrain.split(',')]

    class Meta:
        model = models.Planet
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'climate', 'terrain')
        filter_fields = ('name', )

Planet.Connection = connection_for_type(Planet)


class Film(DjangoObjectType):
    producers = graphene.List(graphene.String)

    @resolve_only_args
    def resolve_producers(self):
        return [c.strip() for c in self.producer.split(',')]

    '''A single film.'''
    class Meta:
        model = models.Film
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'producer')
        filter_fields = {'episode_id': ('gt', )}

Film.Connection = connection_for_type(Film)


class Specie(DjangoObjectType):
    '''A type of person or character within the Star Wars Universe.'''
    eye_colors = graphene.List(graphene.String)
    hair_colors = graphene.List(graphene.String)
    skin_colors = graphene.List(graphene.String)

    @resolve_only_args
    def resolve_eye_colors(self):
        return [c.strip() for c in self.eye_colors.split(',')]

    @resolve_only_args
    def resolve_hair_colors(self):
        return [c.strip() for c in self.hair_colors.split(',')]

    @resolve_only_args
    def resolve_skin_colors(self):
        return [c.strip() for c in self.skin_colors.split(',')]

    class Meta:
        model = models.Species
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'eye_colors', 'hair_colors',
                          'skin_colors')

Specie.Connection = connection_for_type(Specie)


class Vehicle(DjangoObjectType):
    '''A single transport craft that does not have hyperdrive capability'''
    manufacturers = graphene.List(graphene.String)

    @resolve_only_args
    def resolve_manufacturers(self):
        return [c.strip() for c in self.manufacturer.split(',')]

    class Meta:
        model = models.Vehicle
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'manufacturers')
        filter_fields = {'name': {'startswith'}}

Vehicle.Connection = connection_for_type(Vehicle)


class Hero(DjangoObjectType):
    '''A hero created by fans'''

    class Meta:
        model = models.Hero
        interfaces = (Node, )
        exclude_fields = ('created', 'edited')
        filter_fields = {'name': {'startswith', 'contains'}}

Hero.Connection = connection_for_type(Hero)


class Starship(DjangoObjectType):
    '''A single transport craft that has hyperdrive capability.'''
    manufacturers = graphene.List(graphene.String)

    @resolve_only_args
    def resolve_manufacturers(self):
        return [c.strip() for c in self.manufacturer.split(',')]

    @resolve_only_args
    def resolve_max_atmosphering_speed(self):
        if self.max_atmosphering_speed == 'n/a':
            return None
        return self.max_atmosphering_speed

    class Meta:
        model = models.Starship
        interfaces = (Node, )
        exclude_fields = ('created', 'edited', 'manufacturers')

Starship.Connection = connection_for_type(Starship)


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

    def resolve_viewer(self, *args, **kwargs):
        return self


class CreateHero(graphene.Mutation):

    class Input:
        name = graphene.String(required=True)
        homeworld_id = graphene.String(required=True)

    hero = graphene.Field(Hero)
    ok = graphene.Boolean()

    def mutate(self, args, context, info):
        name = args.get('name')
        homeworld_id = args.get('homeworld_id')
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
