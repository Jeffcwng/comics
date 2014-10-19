import factory

__author__ = 'miguelbarbosa'


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'xkcd.Person'


class LikesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'xkcd.Like'
