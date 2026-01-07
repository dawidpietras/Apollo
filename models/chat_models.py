from pydantic import BaseModel, Field
from typing import List

class Ingredient(BaseModel):
    canonical_name: str = Field(..., description="Nazwa podstawowa składnika, bez dodatkowych określeń")
    optional_name: str = Field('', description="Opcjonalna dodatkowa, szczegółowa nazwa składnika lub dodatkowe określenia i przymiotniki")
    quantity: int = Field(..., description="Ilość lub waga lub pojemność składnika jaka jest potrzebna")
    unit: str = Field(..., description="Jednostka miary wynikająca z ilości składnika")

class IngredientWithBoughtStatus(Ingredient):
    bought: bool = Field(
        default=False,
        description="Status czy składnik został już kupiony (True) czy nie (False)"
    )

class ShoppingList(BaseModel):
    formatted_summary: str = Field(
        default_factory=str,
        description="Ładnie sformatowana lista w bullet pointach (Markdown) gotowa do wyświetlenia użytkownikowi w oknie odpowiedzi assistant LLM"
    )
    
    ingredients: List[Ingredient] = Field(
        default_factory=list,
        description="Kompletna lista wszystkich składników, jednostki (units) podawaj w sztukach (szt) lub w gramach (g)"
    )