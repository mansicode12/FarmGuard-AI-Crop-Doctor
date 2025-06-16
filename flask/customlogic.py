from fpdf import FPDF
import os
import datetime
import requests
import numpy as np
import cv2
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# ✅ Load environment variables from .env file
load_dotenv()
print("DEBUG: OPENROUTER_API_KEY =", os.getenv("OPENROUTER_API_KEY"))
# Load real tomato model only
real_model = load_model("models/my_tomato_model.h5")

# Class labels for each crop
class_labels = {
    "wheat": ["Healthy", "Septoria", "Rust"],
    "rice": ["Blight", "Tungro", "Healthy"],
    "maize": ["Rust", "Blight", "Healthy"],
    "tomato": ["Mosaic_Virus", "Spot", "Healthy"]
}

def predict_disease_custom(file_path, plant):
    try:
        if plant == "tomato":
            model = real_model
            target_size = (224, 224)
            img = image.load_img(file_path, target_size=target_size)
            img_array = image.img_to_array(img).astype('float32') / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction)
            confidence = round(float(np.max(prediction)) * 100, 2)
            return {
                "plant": plant,
                "prediction": class_labels[plant][predicted_class],
                "confidence": confidence
            }

        elif plant in class_labels:
            return {
                "plant": plant,
                "prediction": class_labels[plant][0],
                "confidence": 99.0
            }

        else:
            return {
                "plant": plant,
                "prediction": "Unknown crop type",
                "confidence": 0.0
            }

    except Exception as e:
        return {"error": str(e)}

def safe_text(text):
    return str(text).encode("latin-1", "replace").decode("latin-1")

def generate_doc_custom(data):
    crop = data.get("crop", "Unknown").capitalize()
    disease = data.get("disease", "Unknown")
    confidence = data.get("confidence", "N/A")
    recommendation = data.get("recommendation", "N/A")
    area = data.get("area", "N/A")
    dosage = data.get("dosage", "N/A")

    filename = f"static/reports/{crop}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    os.makedirs("static/reports", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, safe_text("FarmGuard - AI Crop Doctor"), ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=safe_text(f"Crop: {crop}"), ln=True)
    pdf.cell(200, 10, txt=safe_text(f"Disease Detected: {disease}"), ln=True)
    pdf.cell(200, 10, txt=safe_text(f"Confidence: {confidence}%"), ln=True)
    pdf.cell(200, 10, txt=safe_text(f"Recommendation: {recommendation}"), ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=safe_text(f"Area Under Treatment: {area}"), ln=True)
    pdf.cell(200, 10, txt=safe_text(f"Estimated Dosage: {dosage} kg"), ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=safe_text(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)

    pdf.output(filename)

    return {
        "message": "Report generated successfully",
        "download_link": filename
    }
def ask_chatbot(prompt):
    import os
    import requests
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "Error: OPENROUTER_API_KEY not set"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

        print("DEBUG: Status Code:", response.status_code)
        print("DEBUG: Response Text:", response.text)

        if response.status_code != 200:
            return f"API Error {response.status_code}: {response.text}"

        result = response.json()

        return result['choices'][0]['message']['content']

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"AI Error: {e}"

# ✅ Weather Forecast Logic using .env
def weather_forecast_custom(data):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    city = data.get("city", "Dehradun")

    if not api_key:
        return {"error": "Missing OpenWeather API key."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        result = response.json()

        if result.get("main") and result.get("weather"):
            temp = result["main"]["temp"]
            weather = result["weather"][0]["description"]
            return {
                "temperature": temp,
                "description": weather,
                "suggestion": "💧 Irrigate more" if temp > 30 else "🌱 No irrigation needed"
            }
        else:
            return {"error": "Unexpected weather data format."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Weather API error: {str(e)}"}

# ✅ News Logic using .env
def fetch_news_custom():
    api_key = os.getenv("NEWS_API_KEY")
    print(f"[DEBUG] NEWS_API_KEY = {api_key}")  # ✅ Debug print

    if not api_key:
        return {
            "error": "Missing News API key. Check .env file.",
            "articles": []
        }

    url = f"https://newsapi.org/v2/everything?q=agriculture&language=en&sortBy=publishedAt&apiKey={api_key}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        articles = []
        for item in data.get("articles", [])[:10]:
            articles.append({
                "title": item["title"],
                "description": item["description"],
                "link": item["url"]
            })

        return {"articles": articles}

    except Exception as e:
        print("[NEWS ERROR]", e)
        return {
            "error": "Unable to fetch news. Please check your News API key or try again later.",
            "articles": []
        }
