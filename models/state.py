#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            all_models = models.storage.all()
            city_instances = []
            matching_cities = []

            # Extract City instances from the storage
            for key in all_models:
                object_key = key.replace('.', ' ')
                object_parts = shlex.split(object_key)
                if object_parts[0] == 'City':
                    city_instances.append(all_models[key])

            # Filter cities associated with this state
            for city_instance in city_instances:
                if city_instance.state_id == self.id:
                    matching_cities.append(city_instance)

            return matching_cities
