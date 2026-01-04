from openai import OpenAI
from dotenv import load_dotenv
import os
from backend.prompts import *
import instructor
from models.chat_models import Ingredient, ShoppingList

load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")
client = instructor.patch(OpenAI(api_key=api_key))

class Nutritionist:
    
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
        stream = client.chat.completions.create(model=self.model, messages=self.messages, stream=True)
        response = ""
        for chunk in stream:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content is not None:
                response += chunk_content
                yield chunk_content
        
        assistant_response = response
        
        self.messages.append({"role": "assistant", "content": assistant_response})
        
        # print(response.choices[0].message.content)
        # return assistant_response

    def get_list_of_ingredients(self, recipe) -> ShoppingList:
        messages = [
            {"role": "system", "content": get_ingredients_system_prompt},
            {"role": "user", "content": get_igredients_prompt + "\n\n" + recipe}
        ]
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_model=ShoppingList
        )
        print(recipe)
        # return response.choices[0].message.content
        return response

# a = Nutritionist()
# a.change_persona("Dawid")
# b = a.send_user_prompt("Cześć!")
# print(b)
# print(response)

# print(f'Input tokens: {response.usage.prompt_tokens}')
# print(f'Output tokens: {response.usage.completion_tokens}')
# print(f'Total tokens: {response.usage.total_tokens}')
# print(f'Total cost: {response._hidden_params["response_cost"]*100:.4f} cents')