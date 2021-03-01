import factory
# from apiv1.tests.factories import AccountFactory
from account.models import Account
from household.models.book import Book
from household.models.tag import Tag


class AccountFactory(factory.django.DjangoModelFactory):
    """AccountのFactory"""

    class Meta:
        model = Account
    username = "testuser2"
    email = "testusr2@sample.com"
    password = "password"


class TagFactory(factory.django.DjangoModelFactory):
    """TagのFactory"""

    class Meta:
        model = Tag
    name = factory.Sequence(lambda n: 'test tag {0}'.format(n))
    color = "grey"
    account = factory.SubFactory(AccountFactory)


class BookFactory(factory.django.DjangoModelFactory):
    """BookのFactory"""
    title = factory.Sequence(lambda n: 'test title {0}'.format(n))
    description = factory.Faker('text')
    money = factory.Sequence(lambda n: n)
    date = factory.Faker('date')
    account = factory.SubFactory(AccountFactory)
    tag = factory.SubFactory(TagFactory)

    class Meta:
        model = Book
