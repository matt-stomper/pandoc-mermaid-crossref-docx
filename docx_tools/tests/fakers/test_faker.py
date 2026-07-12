import pytest
from faker import Faker

from fakers.revision_faker import RevisionFaker


class TestFaker(Faker,
                RevisionFaker):
    pass

test_faker: Faker | TestFaker = Faker()
test_faker.add_provider(RevisionFaker)