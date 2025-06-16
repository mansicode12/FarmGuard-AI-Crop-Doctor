const express = require("express");
const cors = require("cors");
const multer = require("multer");
const fs = require("fs");
const axios = require("axios");
const xml2js = require("xml2js");
const path = require("path");
const FormData = require("form-data");
const dotenv = require("dotenv");
dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());

const upload = multer({ dest: "uploads/" });
app.use("/uploads", express.static(path.join(__dirname, "uploads")));

// 🌿 Health check
app.get("/health", (req, res) => {
  res.json({ status: "running" });
});

// 🚀 Upload & Prediction Route
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });

    const originalExt = path.extname(req.file.originalname);
    const safeFileName = `${Date.now()}${originalExt}`;
    const filePath = path.join(__dirname, "uploads", safeFileName);
    fs.renameSync(req.file.path, filePath);

    const url = `${process.env.FRONTEND_URL || "http://localhost:4000"}/uploads/${safeFileName}`;

    const { plant, city, area, severity } = req.body;
    const prediction = await identifyCrop(filePath, { plant, city, area, severity });

    res.json({ url, prediction });
  } catch (error) {
    console.error("Upload failed:", error);
    res.status(500).json({ error: "Upload failed: " + (error.message || "Unknown error") });
  }
});

// 🔬 Helper: Communicate with Flask Backend
async function identifyCrop(filePath, { plant, city, area, severity }) {
  const formData = new FormData();
  formData.append("file", fs.createReadStream(filePath), path.basename(filePath));
  formData.append("plant", plant);
  formData.append("city", city || "Dehradun");
  formData.append("area", area || "1");
  formData.append("severity", severity || "moderate");

  try {
    const response = await axios.post(
      `${process.env.FLASK_BACKEND_URL || "http://localhost:5000"}/predict`,
      formData,
      { headers: formData.getHeaders() }
    );
    return response.data;
  } catch (error) {
    console.error("Prediction error:", error.response?.data || error.message);
    throw new Error("Prediction failed: " + (error.response?.data?.error || error.message));
  }
}

// 📰 Agriculture News (from RSS or API)
// 📰 Agriculture News (News API or Google RSS fallback)
app.get("/get-agriculture-news", async (req, res) => {
  try {
    const newsApiKey = process.env.NEWS_API_KEY;

    if (newsApiKey) {
      const newsUrl = `https://newsapi.org/v2/everything?q=agriculture%20India&apiKey=${newsApiKey}&language=en&sortBy=publishedAt`;
      const { data } = await axios.get(newsUrl);
      const articles = data.articles.slice(0, 10).map(item => ({
        title: item.title,
        link: item.url,
        published: item.publishedAt || "No date available"
      }));
      return res.json({ source: "NewsAPI", articles });
    }

    // 🔁 Fallback to Google RSS if no API key
    const RSS_FEED_URL = "https://news.google.com/rss/search?q=agriculture+India&hl=en-IN&gl=IN&ceid=IN:en";
    const response = await axios.get(RSS_FEED_URL);
    const parser = new xml2js.Parser();
    parser.parseString(response.data, (err, result) => {
      if (err) return res.status(500).json({ error: "RSS parsing error" });
      const newsItems = result.rss.channel[0].item.slice(0, 10).map(item => ({
        title: item.title[0],
        link: item.link[0],
        published: item.pubDate ? item.pubDate[0] : "No date available"
      }));
      res.json({ source: "Google RSS", articles: newsItems });
    });
  } catch (error) {
    console.error("News fetch error:", error.message);
    res.status(500).json({ error: "Unable to fetch news" });
  }
});

// 🌦️ Weather Forecast via OpenWeatherMap
app.get("/get-weather", async (req, res) => {
  try {
    const { city = "Dehradun" } = req.query;
    const weatherKey = process.env.WEATHER_API_KEY;

    if (!weatherKey) return res.status(400).json({ error: "Missing WEATHER_API_KEY in environment." });

    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${weatherKey}&units=metric`;
    const { data } = await axios.get(url);

    res.json({
      city,
      temperature: data.main.temp,
      description: data.weather[0].description,
      humidity: data.main.humidity,
      wind: data.wind.speed,
      suggestion: data.weather[0].main.includes("Rain")
        ? "🌧️ Avoid spraying pesticides today."
        : "✅ Good time for field activity."
    });
  } catch (err) {
    console.error("Weather fetch error:", err.message);
    res.status(500).json({ error: "Unable to fetch weather for given city" });
  }
});


// 🌐 Start Server
const PORT = process.env.PORT || 4000;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`🚀 FarmGuard Express server running on port ${PORT}`);
});
