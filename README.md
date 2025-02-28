# PlantPulse - AI Crop Disease Detection & Treatment Advisor

## Overview
PlantPulse is an AI-powered mobile application designed to help farmers detect and manage crop diseases efficiently. By leveraging Convolutional Neural Networks (CNNs), image processing, and AI-generated recommendations, PlantPulse provides farmers with early warnings, treatment suggestions, and prevention techniques. The Flutter-based mobile app ensures a user-friendly experience, enabling modern solutions for agricultural challenges.

## Features
- **Disease Detection:** Uses AI-powered image processing to identify and classify crop diseases.
- **Treatment Suggestions:** Provides effective recommendations for disease treatment and prevention.
- **Disease History Storage:** Maintains a record of previously detected diseases for future reference.
- **Weather-Based Analysis:** Predicts disease spread based on weather conditions.
- **Community Support:** Offers forums or chat options for farmer interaction and shared experiences.
- **News Integration:** Delivers updates on current crop disease outbreaks.
- **AI Chatbot:** Answers farmers' queries instantly for quick assistance.

## Technology Stack
### **Frontend**
- Flutter (Cross-platform mobile development)

### **Backend**
- Node.js (Application logic)
- Flask (Hosts ML model for disease detection)

### **Machine Learning Model**
- CNN-based AI model for disease detection
- Integrated with Flask for real-time processing

### **Data Storage**
- S3 Buckets (Stores crop images & generates public URLs for processing)
- MongoDB (Stores user profiles, disease history, and weather data)

## Architecture & Workflow
1. **Image Upload:** Users upload images of affected crops via the Flutter app.
2. **Storage & Processing:** Images are stored in an S3 bucket and processed by the CNN-based ML model.
3. **Disease Detection:** The model classifies the disease and returns results to the backend.
4. **Treatment & Prevention Recommendations:** AI generates suggestions and displays them in the app.
5. **Weather-Based Analysis:** System predicts potential disease spread based on weather data.
6. **Community Support & News Integration:** Farmers can discuss issues and receive real-time updates.

## Setup Instructions
### **1. Clone the Repository**
```bash
 git clone https://github.com/your-repository/PlantPulse.git
 cd PlantPulse
```

### **2. Install Dependencies**
#### **Frontend (Flutter)**
```bash
 flutter pub get
```

#### **Backend (Node.js & Flask ML Model)**
```bash
 npm install   # Install dependencies for Node.js backend
 pip install -r requirements.txt   # Install dependencies for Flask ML model
```

### **3. Configure Environment Variables**
#### **Backend (Node.js)**
Create a `.env` file in the backend directory and add:
```bash
 API_KEY="your_crop.health_API_key"
 accessKeyId="your_S3_BucketID"
 secretAccess="your_S3_secretAccessKey"
```

#### **Flask (ML Model API)**
Create a `.env` file in the Flask directory and add:
```bash
 API_KEY="your_Gemini_api_key"
```

### **4. Run the Application**
#### **Start Backend (Node.js)**
```bash
 npm start
```

#### **Start Flask ML Model API**
```bash
 python app.py
```

#### **Start Frontend (Flutter)**
```bash
 flutter run
```

## Future Scope
- **Enhanced AI Models:** Improving accuracy for rare disease detection.
- **Geolocation Mapping:** Identifying disease hotspots and spread patterns.
- **Multilingual Support:** Adding regional languages for better accessibility.

---
For any questions, feel free to reach out to Team Neural Knights.

## Presentation
[Project PPT](https://drive.google.com/file/d/1IJ0FKWMBDul37KM5-d8QNJnOfvlimpfj/view?usp=sharing)
