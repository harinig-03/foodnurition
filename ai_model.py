from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables
from loguru import logger

import os
import google.generativeai as genai

GEMINI_API_KEY=AIzaSyAqY9CIljkQ5lXOu4smGch51DbbOZ2vQww
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-2.0-flash") 
  

chat = model.start_chat(history=[])
def get_nutrition_info(food_item: str) -> str:
    prompt = f"""
You are a professional nutritionist.

First, provide a concise, point-wise overview of the nutritional benefits of the given food item. 
Do not include any section titles like 'Section 1' or 'Section 2'.
Do not use bullets, stars, asterisks, emojis, or special symbols.
Each benefit should start on a new line.

Then, in a new paragraph, provide the exact macronutrient values in grams.
Each macronutrient should appear on its own line in this format:
Carbohydrates: <value>  
Fiber: <value>  
Fats: <value>  
Protein: <value>  

Only analyze the food item exactly as provided. Do not mention cooking variations, cuts, or generalizations.

Food item: {food_item}
"""

    response=chat.send_message(prompt,stream=True)
    return response




def query_nutrition_knowledge(chat_item: str) -> str:
    prompt = f"""
You are a professional nutritionist.

Answer the question accordingly.
Only analyze the food item exactly as provided. Do not mention cooking variations, cuts, or generalizations.

Food item: {chat_item}
"""
    # Replace with your actual LLM call
    # <-- You should already have `chat` set up
    response = chat.send_message(prompt)
    return response.text  # ✅ extract the actual text
