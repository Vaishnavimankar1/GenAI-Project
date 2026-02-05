# Complete Setup Guide

This guide will walk you through setting up the project step-by-step.

## 🎯 Overview

You'll need to:
1. Install Python and dependencies
2. Get 3 API keys (all free tier available)
3. Configure environment variables
4. Run the application

**Time required:** ~15 minutes

---

## 📋 Step-by-Step Setup

### Step 1: Install Python

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

You need Python 3.8 or higher.

**If not installed:**
- **Windows:** Download from https://www.python.org/downloads/
- **Mac:** `brew install python3`
- **Linux:** `sudo apt install python3 python3-pip`

### Step 2: Clone and Navigate

```bash
git clone <your-repo-url>
cd trulymadly-genai-assignment
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

This installs:
- `anthropic` - Claude AI SDK
- `requests` - HTTP library
- `python-dotenv` - Environment variable loader
- `streamlit` - Web interface (optional)

### Step 4: Get API Keys

#### 4.1 Anthropic API Key (Claude AI)

1. Go to: https://console.anthropic.com/
2. Click "Sign Up" (or "Log In" if you have account)
3. Verify your email
4. Go to "API Keys" section
5. Click "Create Key"
6. **Copy the key** (starts with `sk-ant-`)
7. Save it - you'll add it to `.env` file

**Free Tier:** $5 credit for new users

#### 4.2 OpenWeatherMap API Key

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (or "Sign In")
3. Verify your email
4. Go to: https://home.openweathermap.org/api_keys
5. You'll see a default API key already created
6. **Copy the key** (32-character string)

**Free Tier:** 60 calls/minute, 1,000,000 calls/month

#### 4.3 Google Places API Key

1. Go to: https://console.cloud.google.com/
2. Create a new project or select existing one
3. Click "Enable APIs and Services"
4. Search for "Places API"
5. Click "Enable"
6. Go to "Credentials" in left menu
7. Click "Create Credentials" → "API Key"
8. **Copy the key**
9. (Optional) Restrict the key to "Places API" for security

**Free Tier:** $200 credit for new users, then ~$17/1000 requests

**Important:** You may need to enable billing in Google Cloud Console, but you won't be charged if you stay within free tier.

### Step 5: Configure Environment

Create `.env` file:
```bash
cp .env.example .env
```

Open `.env` in a text editor and add your keys:
```env
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
OPENWEATHER_API_KEY=your-32-char-key-here
GOOGLE_PLACES_API_KEY=AIzaSy-your-key-here
```

**Save the file!**

### Step 6: Test the Setup

Run the test script:
```bash
python test.py
```

You should see:
```
✅ Environment variables configured
✅ TEST PASSED - System is working correctly!
```

If you see errors, check:
- Are all 3 API keys in `.env`?
- Did you copy them correctly (no extra spaces)?
- Did you enable the APIs in Google Cloud Console?

---

## 🚀 Running the Application

### Option 1: Command Line Interface

```bash
python main.py
```

Then type your query when prompted, or press Enter for example query.

### Option 2: Web Interface (Recommended)

```bash
streamlit run app.py
```

This opens a browser with a nice UI at http://localhost:8501

---

## 🧪 Testing with Example Queries

Try these in order:

1. **Simple query:**
   ```
   Plan a weekend trip to Mumbai
   ```

2. **With weather:**
   ```
   Show me weather and hotels in Goa
   ```

3. **With attractions:**
   ```
   Plan a Delhi trip with tourist attractions
   ```

4. **Complete request:**
   ```
   I want to visit Bangalore for 2 days. Show me weather forecast, 
   top hotels, and best restaurants
   ```

---

## 🔧 Troubleshooting

### Error: "Missing environment variables"

**Solution:** Check your `.env` file
```bash
cat .env
# Should show all 3 keys
```

### Error: "401 Unauthorized" (Anthropic)

**Solutions:**
1. Check key starts with `sk-ant-`
2. Verify key is correct in console.anthropic.com
3. Check if you have API credits remaining

### Error: "401 Unauthorized" (OpenWeather)

**Solutions:**
1. Wait 10 minutes after creating key (activation delay)
2. Check key in https://home.openweathermap.org/api_keys
3. Verify email is confirmed

### Error: "403 Forbidden" (Google Places)

**Solutions:**
1. Enable "Places API" in Google Cloud Console
2. Check if billing is enabled (required even for free tier)
3. Wait a few minutes after enabling API

### Error: "ModuleNotFoundError"

**Solution:** Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: Port already in use (Streamlit)

**Solution:** Use different port
```bash
streamlit run app.py --server.port 8502
```

---

## 📊 Understanding the Output

### 1. Planner Agent Output
Shows the execution plan with steps:
```json
[
  {
    "step_number": 1,
    "action": "get_weather_forecast",
    "parameters": {"city": "Mumbai"}
  }
]
```

### 2. Executor Agent Output
Shows results from each API call:
- Weather data with temperatures
- Places with names, ratings, addresses

### 3. Verifier Agent Output
Shows validation:
- Completeness score (0-100)
- Pass/Fail status
- Issues found

### 4. Final Response
Natural language summary of all information

---

## 🎓 Next Steps

1. **Try different cities:** Test with your hometown
2. **Modify queries:** Ask for specific types of places
3. **Check the code:** Read `main.py` to understand agents
4. **Extend functionality:** Add more APIs or features

---

## 📞 Getting Help

If you're still stuck:

1. Check the error message carefully
2. Google the specific error
3. Check API documentation:
   - Anthropic: https://docs.anthropic.com/
   - OpenWeather: https://openweathermap.org/api
   - Google Places: https://developers.google.com/maps/documentation/places/web-service

4. Verify your API keys are active and have credits

---

## ✅ Final Checklist

Before submission, verify:

- [ ] All 3 API keys are configured
- [ ] `python test.py` passes
- [ ] `python main.py` runs successfully
- [ ] At least 3 example queries work
- [ ] README.md is complete
- [ ] Code is pushed to GitHub
- [ ] Repository is public or shared with evaluator

---

**You're all set! 🎉**

The system is now ready to plan trips using AI agents and real APIs.
