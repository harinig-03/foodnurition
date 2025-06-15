import streamlit as st
import requests
import re
import pandas as pd
import urllib.parse

# --- Helper function to extract macronutrients ---
def extract_macro(names, text):
    if text is None:
        return 0.0
    for name in names:
        pattern = fr"{name}\s*[:\-=]?\s*([0-9]+(?:\.[0-9]+)?)\s*(g|grams)?"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return 0.0
    return 0.0

# --- Streamlit Setup ---
st.set_page_config(page_title="Food Nutrition Dashboard", layout="centered")
st.title("🥗 AI-Based Food Nutrition Analyzer")

# --- Session State Setup ---
if "nutrition_data" not in st.session_state:
    st.session_state.nutrition_data = None
if "food_item" not in st.session_state:
    st.session_state.food_item = ""

# --- Input ---
food_item = st.text_input("Enter a food item (e.g., banana, oats, eggs):", value=st.session_state.food_item)

if st.button("Analyze"):
    if not food_item.strip():
        st.warning("Please enter a food item.")
    else:
        try:
            url = f"https://foodnurition-5.onrender.com/analyze/{urllib.parse.quote(food_item)}"
            with st.spinner("Analyzing nutrition..."):
                response = requests.get(url)
            if response.status_code == 200:
                st.session_state.nutrition_data = response.json()
                st.session_state.food_item = food_item
            else:
                st.error(f"API error. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- Display if Data Exists ---
data = st.session_state.nutrition_data

if isinstance(data, dict) and "nutrition_info" in data:
    nutrition_text = data["nutrition_info"]

    # Extract macros
    protein = extract_macro(["Protein"], nutrition_text)
    fat = extract_macro(["Fat", "Fats"], nutrition_text)
    carbs = extract_macro(["Carbohydrates", "Carbs"], nutrition_text)
    fiber = extract_macro(["Fiber"], nutrition_text)

    # Show summary
    st.subheader(f"Nutrition info for: {st.session_state.food_item.capitalize()}")
    st.write(nutrition_text)

    # Macronutrient bar chart
    df = pd.DataFrame({
        "Macronutrient": ["Protein", "Fat", "Carbs", "Fiber"],
        "Grams": [protein, fat, carbs, fiber]
    })
    st.markdown("### 🧩 Macronutrient Breakdown")
    st.bar_chart(df.set_index("Macronutrient"))

    # Health Score
    score = 0
    if fiber > 2.5: score += 1
    if protein > 7: score += 1
    if fat < 5: score += 1
    if carbs < 27: score += 1

    health_status = {
        4: "Excellent 🟢",
        3: "Good 🟡",
        2: "Fair 🟠",
        1: "Poor 🔴",
        0: "Very Poor 🔴"
    }
    st.markdown(f"### 🩺 Health Score: {score}/4 — **{health_status[score]}**")

    # Suggested Pairings
    suggestions = {
        "banana": "Pair banana with Greek yogurt and oats for a complete breakfast.",
        "oats": "Top your oats with berries and nuts for extra fiber and healthy fats.",
        "eggs": "Pair boiled eggs with whole grain toast and avocado for a protein-rich meal.",
    }
    default_suggestion = "Try combining this food with greens, healthy fats, and lean protein."
    st.markdown("### 🍽 Suggested Pairing:")
    st.info(suggestions.get(st.session_state.food_item.lower(), default_suggestion))

else:
    if data is not None:
        st.error("❌ 'nutrition_info' is missing or data format is invalid.")
        st.write("Raw response:")
        st.write(data)

# --- Chat Section ---
st.markdown("## 🧠 Chat with the Nutritionist AI")
chat_input = st.text_input("Ask something", key="chat_input")

if "chat_response" not in st.session_state:
    st.session_state.chat_response = None

if st.button("Chat with Me"):
    if not chat_input.strip():
        st.warning("Please enter a question.")
    else:
        try:
            encoded_chat = urllib.parse.quote(chat_input)
            url = f"https://foodnurition-5.onrender.com/ask/{encoded_chat}"
            with st.spinner("Getting answer..."):
                response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                st.session_state.chat_response = data["answer"]
            else:
                st.error("❌ Failed to get response from server.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ✅ Show the answer if it exists
if st.session_state.chat_response:
    st.success(f"🗨️ {st.session_state.chat_response}")

