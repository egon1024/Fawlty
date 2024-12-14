"""
A module to represent a Sensu rolebinding resource
"""

# Built in imports
from typing import Optional, List, Dict, Literal

# Our imports
from sensu.resources.base import ResourceBase
from sensu.client import SensuClient

# 3rd party imports
from pydantic import BaseModel, validator

# Constants
BASE_URL = "/api/core/v2/namespaces/{namespace}/rolebindings"

def get_url(namespace: str, name: str = None) -> str:
    """
    Get a url to retrieve a list of matching rolebindings resources.
    """

    url = BASE_URL.format(namespace=namespace)
    if name is not None:
        url += f"/{name}"
    
    return url


class RoleBindingMetadata(BaseModel):
    """
    A class to represent the data structure of a rolebinding metadata
    """
    name: str
    namespace: str
    created_by: Optional[str] = None
    labels: Optional[dict[str, str]] = {}
    annotations: Optional[dict[str, str]] = {}


class RoleBindingSubject(BaseModel):
    """
    A class to represent the data structure of a rolebinding subject
    """
    name: str
    type: Literal["Group", "User"]


class RoleBindingRoleRef(BaseModel):
    """
    A class to represent the data structure of a rolebinding role_ref
    """
    name: str
    type: Literal["Role"] = "Role"


class RoleBinding(ResourceBase):
    """
    A class to represent a Sensu rolebinding resource
    """

    metadata: RoleBindingMetadata
    role_ref: RoleBindingRoleRef
    subjects: List[RoleBindingSubject]
    _sensu_client: Optional[SensuClient] = None


    def urlify(self, purpose: str=None) -> str:
        """
        Return the URL for the rolebinding resource(s).

        :return: The URL for the rolebinding resource.
        """

        url = BASE_URL.format(namespace=self.metadata.namespace)

        if purpose != "create":
            url += f"/{self.metadata.name}"

        return url
