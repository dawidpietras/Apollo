from sqlmodel import SQLModel, Field
from enum import Enum
import streamlit as st

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ShoppingItem(SQLModel, table=True, extend_existing=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., description="Name of the ingredient in polish language")
    quantity: int = Field(None,
                          description="""Item quantity declared in pieces
                          (szt in polish) or in grams depends on user input.
                          Use polish szt or just g for grams. This field can be empty
                          because user can just say 'bananas' without defining quantity.
                          Quantity unit is not included here just number.""")
    unit: str = Field(None,
                      description="""Quantity unit declared by user. Use szt for slices or
                      units and grams (g) for weight units.""",
                      schema_extra={"type": "string"})
    bought: bool = Field(False,
                         description="""If no info is given from user, assume that False is
                         the right value""")

class ToDoTask(SQLModel, table=True, extend_existing=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(..., description="Title of the task taht will be visible in to-do list")
    priority: Priority = Field(Priority.MEDIUM,
                               description="""Declared priority of the task. If user declared
                               similar level, for example moderate instead of medium try to
                               adjust it to allowed values.""")
    assigned: str = Field(None, description="""If user assigned someone to mentioned task
                          then write here the name, full name or nick.""")