import factory
__author__ = 'miguelbarbosa'


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'xkcd.Person'
    username = factory.Sequence(lambda i: 'User{}'.format(i))
    password = factory.PostGenerationMethodCall('set_password', 'password')


class LikesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'xkcd.Like'

    liked_by = factory.SubFactory(PersonFactory)
