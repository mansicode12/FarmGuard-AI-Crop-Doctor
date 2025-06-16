from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from customlogic import predict_disease_custom, generate_doc_custom, weather_forecast_custom, fetch_news_custom
from customlogic import ask_chatbot
import os

app = Flask(__name__)
app.secret_key = "farmguard_secret_key"
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["REPORT_FOLDER"] = os.path.join("static", "reports")

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["REPORT_FOLDER"], exist_ok=True)

# ✅ Dosage advice per crop & disease
dosage_advice = {
    "Wheat": {
        "Rust": "Spray Propiconazole 25% EC at 500 ml/ha.",
        "Healthy": "No signs of disease. Continue standard practices."
    },
    "Tomato": {
        "Mosaic_Virus": "Use virus-resistant seeds. Remove infected plants.",
        "Spot": "Apply copper-based fungicides. Maintain good airflow.",
        "Healthy": "No disease detected. Maintain proper care."
    },
    "Maize": {
        "Rust": "Use Mancozeb 75% WP fungicide as per label.",
        "Healthy": "No issues detected. Maintain regular care."
    },
    "Rice": {
        "Blight": "Apply copper-based bactericides. Avoid over-irrigation.",
        "Healthy": "No issues detected. Maintain field hygiene."
    }
}

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        session["password"] = password
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if session.get("username") == username and session.get("password") == password:
        return redirect(url_for("dashboard"))
    return render_template("login.html", error="Invalid credentials")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html")

@app.route("/predict", methods=["POST"])
def predict():
    if 'file' not in request.files or 'plant' not in request.form:
        return redirect(url_for('dashboard'))

    file = request.files['file']
    plant = request.form['plant'].strip().lower()

    if file.filename == '':
        return redirect(url_for('dashboard'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        result = predict_disease_custom(filepath, plant)
        prediction = result.get("prediction", "Unknown")
        confidence = result.get("confidence", 0)
        note = result.get("note", "")

        crop_key = plant.capitalize()
        disease_key = prediction.replace(" ", "_")
        dosage = dosage_advice.get(crop_key, {}).get(disease_key, "Dosage advice not found.")

        weather_info = weather_forecast_custom({"city": "Dehradun"})
        report_result = generate_doc_custom({
            "crop": plant,
            "disease": prediction,
            "confidence": confidence,
            "recommendation": dosage,
            "area": "N/A",
            "dosage": dosage
        })
        report_path = report_result.get("download_link", None)

        return render_template(
            "dashboard.html",
            prediction=prediction,
            confidence=confidence,
            note=note,
            dosage=dosage,
            weather_info=weather_info,
            report_path=report_path,
            image_url=url_for('static', filename='uploads/' + filename)
        )

    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return render_template("dashboard.html",
            prediction="Error",
            confidence="",
            note=str(e),
            dosage="N/A",
            weather_info={},
            report_path=None,
            image_url=None
        )

# ✅ Updated news route using correct function
@app.route("/news")
def news():
    articles = fetch_news_custom()
    if "error" in articles:
        return render_template("news.html", error=articles["error"])
    return render_template("news.html", articles=articles["articles"])

# ✅ New weather API route
@app.route("/weather")
def weather():
    city = request.args.get("city", "Dehradun")
    weather_data = weather_forecast_custom({"city": city})
    return weather_data


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({'response': "No input provided"}), 400
    
    reply = ask_chatbot(user_input)
    return jsonify({'response': reply})


@app.route("/community")
def community():
    return render_template("community.html")
# Health check endpoint (Render uses this to check if your app is alive)
@app.route("/health")
def health():
    return {"status": "OK", "message": "FarmGuard backend is healthy."}

# Run locally only (won't be used on Render, but useful for testing)
if __name__ == "__main__":
    # Set host='0.0.0.0' and port=5000 so it works locally
    app.run(debug=True, host="0.0.0.0", port=5000)


