from typing import Generator, Any

import pytest

from fakers.test_faker import test_faker


@pytest.fixture
def test_faker_fixture() -> Generator[Any, Any, None]:
    yield test_faker

