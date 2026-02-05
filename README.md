# Multi-Agent Travel Planning System

A production-ready multi-agent system that demonstrates a multi-agent architecture
for planning, executing, and verifying travel-related queries using real-world APIs.


## 🏗️ Architecture

This system implements a **three-agent architecture**:

### 1. **Planner Agent** 🧠
- **Role**: Analyzes user queries and creates structured execution plans
- **Technology**: Claude Sonnet 4.5 with structured JSON output
- **Output**: Step-by-step execution plan with API calls

### 2. **Executor Agent** ⚡
- **Role**: Executes each step in the plan by calling real APIs
- **APIs Used**:
  - **OpenWeatherMap API** - For weather forecasts
  - **Google Places API** - For hotels, restaurants, attractions
- **Output**: Collected data from all API calls

### 3. **Verifier Agent** ✓
- **Role**: Validates execution results for completeness and accuracy
- **Technology**: Claude Sonnet 4.5 for intelligent verification
- **Output**: Verification report with completeness score

### Orchestrator
- Coordinates all three agents
- Generates final natural language response
- Handles error recovery

```
User Query → Planner → Executor → Verifier → Final Response
              (Plan)   (API Data) (Validation)  (Formatted)
```

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- API Keys (see below)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd trulymadly-genai-assignment
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
```

### 4. Get API Keys

#### Anthropic API Key (Claude)
1. Visit: https://console.anthropic.com/
2. Sign up / Log in
3. Go to API Keys section
4. Create a new key
5. Copy the key to your `.env` file

#### OpenWeatherMap API Key
1. Visit: https://openweathermap.org/api
2. Sign up for free account
3. Go to API Keys section
4. Copy the default key or create new one
5. Add to your `.env` file

#### Google Places API Key
1. Visit: https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable "Places API"
4. Go to Credentials → Create API Key
5. Add to your `.env` file

### 5. Run the Application
```bash
python main.py
```

Or with environment variables inline:
```bash
ANTHROPIC_API_KEY=sk-xxx OPENWEATHER_API_KEY=xxx GOOGLE_PLACES_API_KEY=xxx python main.py
```

## 📋 Example Test Prompts

Try these queries when running the application:

1. **Basic Trip Planning**
   ```
   Plan a weekend trip to Mumbai with weather forecast and top hotels
   ```

2. **Restaurant Search**
   ```
   I want to visit Goa. Show me the weather and best restaurants
   ```

3. **Tourist Attractions**
   ```
   Plan a trip to Delhi with weather info and tourist attractions
   ```

4. **Beach Vacation**
   ```
   Plan a beach vacation in Kerala with weather and beach resorts
   ```

5. **Business Trip**
   ```
   I have a business trip to Bangalore. Find weather forecast and business hotels
   ```

## 🔌 Integrated APIs

### 1. OpenWeatherMap API
- **Purpose**: Real-time weather forecasts
- **Endpoint**: `http://api.openweathermap.org/data/2.5/forecast`
- **Data Retrieved**: 
  - Temperature (current & forecast)
  - Weather descriptions
  - Humidity & wind speed
  - 24-hour forecast in 3-hour intervals

### 2. Google Places API
- **Purpose**: Search hotels, restaurants, attractions
- **Endpoint**: `https://maps.googleapis.com/maps/api/place/textsearch/json`
- **Data Retrieved**:
  - Place names & addresses
  - Ratings & review counts
  - Place types & categories
  - Geographic coordinates

### 3. Anthropic Claude API
- **Purpose**: LLM for planning, verification, and response generation
- **Model**: Claude Sonnet 4.5
- **Features**:
  - Structured JSON output
  - Tool/function calling capability
  - Natural language understanding

## 🎯 System Flow

```
1. USER INPUT
   ↓
2. PLANNER AGENT
   - Analyzes query
   - Creates execution plan
   - Identifies required API calls
   ↓
3. EXECUTOR AGENT
   - Executes each step
   - Calls OpenWeatherMap API
   - Calls Google Places API
   - Collects all results
   ↓
4. VERIFIER AGENT
   - Validates completeness
   - Checks data quality
   - Generates verification report
   ↓
5. ORCHESTRATOR
   - Synthesizes results
   - Generates natural response
   ↓
6. OUTPUT TO USER
```

## ⚠️ Known Limitations & Tradeoffs

### Limitations
1. **API Rate Limits**: 
   - OpenWeatherMap free tier: 60 calls/minute
   - Google Places: Limited free quota
   - Solution: Implement caching for repeated queries

2. **Geographic Coverage**: 
   - Optimized for Indian cities
   - International queries may have varying accuracy

3. **Weather Forecast Window**: 
   - Limited to 24-hour forecast (8 data points)
   - For longer forecasts, requires paid API tier

4. **Place Search Results**: 
   - Limited to top 5 results per query
   - Tradeoff between comprehensiveness and response speed
5. **API Authorization & Billing**:
   - Some third-party APIs (OpenWeatherMap and Google Places) may return
     authorization or billing-related errors depending on API key permissions.
   - The system handles these failures gracefully without crashing.

### Design Tradeoffs

1. **Sequential vs Parallel Execution**:
   - Current: Sequential execution of steps
   - Tradeoff: Simpler error handling, but slower
   - Future: Parallel API calls for speed

2. **LLM Model Selection**:
   - Using Claude Sonnet 4.5 (balanced performance/cost)
   - Could use Claude Opus for better planning (higher cost)
   - Could use Claude Haiku for faster responses (lower quality)

3. **Error Handling**:
   - Continues execution even if one step fails
   - Tradeoff: Partial results vs complete failure

4. **Response Format**:
   - Natural language output (user-friendly)
   - Tradeoff: Less structured than pure JSON, but more accessible

## 🧪 Testing

The system validates:
- ✅ Multi-agent coordination
- ✅ Real API integration (no hardcoded responses)
- ✅  Structured output from planner logic
- ✅ End-to-end query processing
- ✅ Error handling and recovery




