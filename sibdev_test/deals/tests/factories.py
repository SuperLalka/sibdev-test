import random

import factory
from datetime import datetime

from deals import models
from django.contrib.auth.models import User


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(lambda n: f'{n.first_name}{n.last_name}')


GEM_LIST = ("Сапфир", "Рубин", "Топаз", "Жемчуг")


class GemsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Gem

    name = factory.Faker('random_element', elements=GEM_LIST)


class DealsFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = models.Deal

    customer = factory.SubFactory(UsersFactory)
    item = factory.SubFactory(GemsFactory)
    total = factory.Faker('random_int', min=100, max=1000)
    quantity = factory.Faker('random_int', min=1, max=10)
    date = factory.LazyFunction(datetime.now)
