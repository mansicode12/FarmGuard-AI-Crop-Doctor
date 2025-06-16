import os
import google.generativeai as genai  
from dotenv import load_dotenv

from prompt import Disease_Predictor
from getcoordinate import get_coordinates
from dose import get_fertilizer_dosage
from weather import weatherprompt
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_prediction(disease, crop, location):
    prompt = Disease_Predictor(disease, crop, location)
    print("Calling Gemini for Disease Prediction...")
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else None
    except Exception as e:
        print(f"Error generating prediction with Gemini: {str(e)}")
        return None

def coordinate(location):
    prompt = get_coordinates(location)
    print("Calling Gemini for Locatin detection...")
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else None
    except Exception as e:
        print(f"Error generating prediction with Gemini: {str(e)}")
        return None

def weatherpred(Disease,Crop,Duration,Location):
    prompt = weatherprompt(Disease,Crop,Duration,Location)
    print("Calling Gemini for weatherpred...")
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else None
    except Exception as e:
        print(f"Error generating prediction with Gemini: {str(e)}")
        return None

def dosepred(Crop_type,Growth_stage,Fertilizer_name,Plot_size):
    prompt = get_fertilizer_dosage(Crop_type,Growth_stage,Fertilizer_name,Plot_size)
    print("Calling Gemini for get_fertilizer_dosage...")
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else None
    except Exception as e:
        print(f"Error generating prediction with Gemini: {str(e)}")
        return None