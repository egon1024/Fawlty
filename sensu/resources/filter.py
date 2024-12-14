"""
A module to represent a Sensu filter resource
"""

# Built in imports
from typing import Optional, List, Dict, Literal

# Our imports
from sensu.resources.base import ResourceBase
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/filters"

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching filter resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class FilterMetadata(BaseModel):
    """
    A class to represent the data structure of a filter metadata
    """
    name: str
    namespace: str
    created_by: Optional[str] = None
    labels: Optional[dict[str, str]] = {}
    annotations: Optional[dict[str, str]] = {}


class Filter(ResourceBase):
    """
    A class to represent a Sensu filter resource
    """

    action: Literal["allow", "deny"]
    expressions: List[str] = []
    runtime_assets: Optional[List[str]] = []
    metadata: FilterMetadata

    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the filter resource(s).

        :return: The URL for the filter resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
