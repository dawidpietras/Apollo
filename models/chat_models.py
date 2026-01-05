from pydantic import BaseModel, Field
from typing import List

class Ingredient(BaseModel):
    name: str = Field(..., description="Nazwa składnika")
    quantity: int = Field(..., description="Ilość składnika jaki jest potrzebna")
    unit: str = Field(..., description="Jednostka miary")

class ShoppingList(BaseModel):
    formatted_summary: str = Field(
        default_factory=str,
        description="Ładnie sformatowana lista w bullet pointach (Markdown) gotowa do wyświetlenia użytkownikowi w oknie odpowiedzi assistant LLM"
    )
    
    ingredients: List[Ingredient] = Field(
        default_factory=list,
        description="Kompletna lista wszystkich składników, jednostki (units) podawaj w sztukach (szt) lub w gramach (g)"
    )