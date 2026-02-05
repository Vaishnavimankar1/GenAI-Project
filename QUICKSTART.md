# ⚡ Quick Start Guide - 5 Minutes

Get your system running in 5 minutes!

## 1️⃣ Install Dependencies (1 min)

```bash
pip install anthropic requests python-dotenv streamlit
```

## 2️⃣ Get API Keys (3 min)

### Anthropic (Claude AI)
- Go to: https://console.anthropic.com/
- Sign up → API Keys → Create Key
- Copy key (starts with `sk-ant-`)

### OpenWeatherMap
- Go to: https://openweathermap.org/api
- Sign up → API Keys tab
- Copy the default key

### Google Places
- Go to: https://console.cloud.google.com/
- Create project → Enable "Places API"
- Credentials → Create API Key
- Copy key

## 3️⃣ Create .env File (30 sec)

Create a file named `.env` in project folder:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENWEATHER_API_KEY=your-weather-key-here
GOOGLE_PLACES_API_KEY=your-google-key-here
```

## 4️⃣ Run (30 sec)

```bash
# Option 1: Command line
python main.py

# Option 2: Web interface (better!)
streamlit run app.py
```

## ✅ Test It

Try this query:
```
Plan a weekend trip to Mumbai with weather and hotels
```

You should see:
- 🧠 Planner creates a plan
- ⚡ Executor calls APIs
- ✓ Verifier validates results
- 📝 Final formatted response

---

## 🚨 Common Issues

**"Missing API keys"**
→ Check your `.env` file exists and has all 3 keys

**"401 Error"**
→ Wait 10 min after creating OpenWeather key, or check Anthropic credits

**"403 Error"**
→ Enable billing in Google Cloud Console (won't be charged in free tier)

---

## 📝 Example Queries to Test

1. `Plan a trip to Goa with weather and restaurants`
2. `Show me hotels and weather in Bangalore`
3. `I want to visit Delhi - give me tourist attractions and weather`
4. `Beach vacation in Kerala with weather forecast`
5. `Business trip to Pune - need hotels and current weather`

---

**That's it! You're ready to submit! 🎉**

Make sure to:
1. Push to GitHub
2. Make repo public or share access
3. Test with at least 3 queries
4. Submit the GitHub link
