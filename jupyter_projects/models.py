import collections

from pydantic import BaseModel, Field
from typing import List, Any, Type
import datetime

from .db import User, Group, Project, APIToken


class ORMModel(BaseModel):
    """A subclass of Pydantic's Base model that handles the
    conversion of ORM objects to ORM Pydantic Models and vice versa.

    Every ORMModel must have a ORM Base object that mirrors it. Set
    the `__orm__` attribute to this Base object.

    Nested ORM Base Objects / ORMModels are allowed and handled by
    this class.
    """
    # Set this attribute to the ORM Base object that mirrors this
    # Pydantic object
    __orm__ = None

    class Config:
        # This is a pydantic thing. This allows models
        # to be constructed from ORM objects.
        # See `to_orm` below for the reverse case where
        # you need to convery an ORMModel to an ORM object.
        orm_mode = True

    def to_orm(self):
        """
        Recursively iterate through a pydantic base model
        and convert all `ORMModel`s to ORM objects.
        """
        data = {}
        for key, value in self:
            # If field is Type[ORMModel],
            # recursively convert to an ORM object.
            if hasattr(value, "__orm__"):
                data[key] = value.to_orm()
            # If the field is a dictionary, iterate over
            # values and convert any ORM models to ORM objects
            # else leave them alone.
            elif isinstance(value, dict):
                nested_data = {}
                for nested_key, nested_value in value:
                    if hasattr(nested_value, "__orm__"):
                        nested_data[key] = nested_value.to_orm()
                    else:
                        nested_data[key] = value
                data[key] = nested_data
            # If the field is an iterable, iterate through list
            # and convert ORM Models to ORM objects.
            #
            # There has to be a better way to write this conditional...
            elif (
                isinstance(value, collections.Iterable) and
                type(value) not in (str, bytearray, bytes)
            ):
                nested_data = []
                for nested_value in value:
                    if hasattr(nested_value, "__orm__"):
                        nested_data.append(nested_value.to_orm())
                    else:
                        nested_data.append(nested_value)
                # Convert iterable to the appropriate type at the
                # end.
                data[key] = type(value)(nested_data)
            # Leave the value alone if its not an ORMModel
            else:
                data[key] = value
        return self.__orm__(**data)


class APITokenModel(ORMModel):
    __orm__ = APIToken
    id: int = ...
    hashed: str = ...
    prefix: str = ...
    created: datetime.datetime = None
    expires_at: datetime.datetime = None
    last_activity: datetime.datetime = None
    note: str = None


class UserModel(ORMModel):
    __orm__ = User
    id: int = ...
    name: str = ...
    admin: bool = ...
    created: datetime.datetime = None
    last_activity: datetime.datetime = None
    api_tokens: List[APITokenModel] = None
    cookie_id: str = None
    encrypted_auth_state: bytes = None


class GroupModel(ORMModel):
    __orm__ = Group
    id: int = None
    name: str = ...
    users: List[UserModel]


class GroupListModel(ORMModel):
    groups: List[GroupModel]


class ProjectModel(ORMModel):
    __orm__ = Project
    id: int = None
    name: str = ...
    groups: List[GroupModel]


class ProjectListModel(BaseModel):
    projects: List[ProjectModel]