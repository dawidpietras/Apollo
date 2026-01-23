from backend.prompts import *
from models.chat_models import ShoppingList
from backend.llm_client import get_sync_client

class Nutritionist:
    
    def __init__(self):
        self.client = get_sync_client()
    
    def set_model(self, model):
        self.model = model
    
    def change_persona(self, persona):
        if persona == "Dawid":
            self.system_prompt = dawid_system_prompt
        elif persona == "Emilia":
            self.system_prompt = emilia_system_prompt
        elif persona == "Lista zakupów":
            self.system_prompt = shopping_list_system_prompt
            
        self.messages = [
            {"role": "system", "content": self.system_prompt}
]
    
    def send_user_prompt(self, prompt):
        
        self.messages.append({"role": "user", "content": prompt})
        stream = self.client.chat.completions.create(model=self.model, messages=self.messages, stream=True)
        response = ""
        for chunk in stream:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content is not None:
                response += chunk_content
                yield chunk_content
        
        assistant_response = response
        
        self.messages.append({"role": "assistant", "content": assistant_response})
        

    def get_list_of_ingredients(self, recipe) -> ShoppingList:
        messages = [
            {"role": "system", "content": get_ingredients_system_prompt},
            {"role": "user", "content": get_igredients_prompt + "\n\n" + recipe}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_model=ShoppingList
        )
        
        return response