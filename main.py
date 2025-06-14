from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ai_model import get_nutrition_info
from ai_model import query_nutrition_knowledge


GEMINI_API_KEY="AIzaSyAqY9CIljkQ5lXOu4smGch51DbbOZ2vQww"
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI-Based Food Nutrition Analyzer is running!"}


@app.get("/analyze/{food_item}")
async def analyze_food(food_item: str):
    """
    Get structured nutrition info for a food item.
    """
    result_text = get_nutrition_info(food_item)  # This is now the full text

    structured_response = {
        "food": food_item,
        "nutrition_info": result_text.replace("\n", " ")  # Flatten for JSON
    }

    return JSONResponse(content=structured_response, status_code=200)


@app.get("/ask/{question}")
async def ask_nutrition_question(question: str):
    try:
        result = query_nutrition_knowledge(question)
        structured_response = {
            "question": question,
            "answer": result.replace("\n", " ")
        }
        return JSONResponse(content=structured_response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
