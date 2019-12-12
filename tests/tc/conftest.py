from pathlib import Path
import pytest
import yaml

from .fixtures.github import *
from .fixtures.taskcluster import *


@pytest.fixture
def taskcluster_yml():
    with Path(__file__).parent.parent.with_name(".taskcluster.yml").open() as f:
        return yaml.safe_load(f.read())

