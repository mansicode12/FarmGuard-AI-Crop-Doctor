🌾 FarmGuard – AI Crop Doctor
FarmGuard is an AI-powered web app that helps farmers identify tomato plant diseases using deep learning. It also offers AI chatbot advice, weather forecasts, dosage estimation, and PDF reporting to support smarter, more informed farming decisions.

<!-- Optional image -->

🚀 Features
📸 AI Tomato Disease Detection – Upload tomato leaf images to detect diseases with a trained deep learning model.

🌾 Placeholder Support for Other Crops – Rice, Wheat, and Maize currently return placeholder results (full models coming soon).

💬 AI Chatbot (OpenRouter) – Ask crop-related questions and get answers powered by OpenRouter’s free AI models.

🌦️ Weather Forecast – 5-day forecast for your location (OpenWeather API).

💊 Dosage Estimator – Suggests pesticide/fertilizer doses based on crop, area, and severity.

📄 PDF Report Generator – Download detailed disease diagnosis reports.

👤 Login/Register System – Simple farmer login system with session tracking.

📰 Agri News Feed – Stay updated with real-time agricultural news.

🧑‍🌾 Community Tab (optional) – Discuss and learn from fellow farmers.
## 🖼️ Screenshots

**📊 Dashboard**
![Dashboard](screenshots/2.jpg)

**📊 Dashboard**
![Dashboard](screenshots/3.jpg)

**🔐 Login Page/Register Page**
![Login](screenshots/1.jpg)

**📰 News Feed**
![News](screenshots/4.jpg)

**👨‍🌾 Community Forum**
![Community](screenshots/5.jpg)

**🏠 Chatbot**
![Home](screenshots/6.jpg)


🛠 Tech Stack
🐍 Flask (Python backend)

🖼 Tailwind CSS (UI)

📦 Express.js (upload server)

🧠 TensorFlow (Tomato model)

🌤 OpenWeather API

💬 OpenRouter AI (Chatbot)

📁 Tomato Model Only (Real)
✅ Tomato – Real model trained using PlantVillage dataset

🚧 Rice, Wheat, Maize – Placeholder logic only (model integration coming)

🛠️ Getting Started
bash
Copy
Edit
# Clone the project
git clone https://github.com/yourusername/farmguard.git
cd farmguard

# Create a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set your environment variables in `.env`
OPENROUTER_API_KEY=your_openrouter_key
WEATHER_API_KEY=your_openweather_key
NEWS_API_KEY=your_newsapi_key

# Run the Flask server
cd flask
python app.py
Ensure the tomato model file (e.g., tomato_model.h5) is placed in the correct path under the /models directory.

💬 Chatbot Examples
Ask the AI:

“How to prevent early blight in tomato?”

“What is the ideal weather for tomato crops?”

“How much pesticide is needed for 2 acres of tomato field?”

📷 Screenshots (Add Your Own)
Dashboard UI

Tomato prediction result

Chatbot reply

Generated PDF preview

🌍 Deployment Tips
Backend: Render

Frontend: Vercel or localhost

Free-tier APIs used (no paid keys required for chatbot via OpenRouter)

👨‍💻 Author
Mansi Bisht
📎 LinkedIn
💻 GitHub

