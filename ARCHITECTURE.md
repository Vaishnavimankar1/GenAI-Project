# System Architecture

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│  (Command Line / Streamlit Web App)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  MULTI-AGENT ORCHESTRATOR                    │
│  • Coordinates all agents                                    │
│  • Manages execution flow                                    │
│  • Handles errors and recovery                               │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   PLANNER    │   │   EXECUTOR   │   │   VERIFIER   │
│    AGENT     │──▶│    AGENT     │──▶│    AGENT     │
│              │   │              │   │              │
│ Creates Plan │   │ Executes     │   │ Validates    │
│ (Claude LLM) │   │ API Calls    │   │ Results      │
└──────────────┘   └──────────────┘   └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Anthropic    │   │ OpenWeather  │   │ Google Places│
│ Claude API   │   │     API      │   │     API      │
│              │   │              │   │              │
│ (LLM)        │   │ (Weather)    │   │ (Places)     │
└──────────────┘   └──────────────┘   └──────────────┘
```

## 🔄 Execution Flow

### Phase 1: Planning
```
User Query
    ↓
Planner Agent (Claude LLM)
    ↓
Structured JSON Plan
    [
      {step: 1, action: "get_weather", params: {...}},
      {step: 2, action: "search_places", params: {...}}
    ]
```

### Phase 2: Execution
```
For each step in plan:
    ↓
Execute action
    ├─ get_weather_forecast() → OpenWeatherMap API
    └─ search_places() → Google Places API
    ↓
Collect results
    {
      step_results: [result1, result2, ...],
      errors: [...]
    }
```

### Phase 3: Verification
```
Execution Results + Original Plan
    ↓
Verifier Agent (Claude LLM)
    ↓
Verification Report
    {
      verification_passed: true/false,
      completeness_score: 0-100,
      issues: [...],
      recommendations: [...]
    }
```

### Phase 4: Response Generation
```
All collected data
    ↓
Orchestrator (Claude LLM)
    ↓
Natural Language Response
    "Based on the weather forecast and available hotels..."
```

## 🧩 Component Details

### 1. Planner Agent

**Technology:** Claude Sonnet 4.5

**Input:** User query (string)

**Output:** Execution plan (JSON array)

**Responsibilities:**
- Parse user intent
- Identify required API calls
- Create sequential execution plan
- Handle ambiguous queries

**Example Output:**
```json
[
  {
    "step_number": 1,
    "action": "get_weather_forecast",
    "parameters": {
      "city": "Mumbai",
      "country_code": "IN"
    },
    "description": "Get weather forecast for Mumbai"
  },
  {
    "step_number": 2,
    "action": "search_places",
    "parameters": {
      "query": "hotels",
      "location": "Mumbai"
    },
    "description": "Search for hotels in Mumbai"
  }
]
```

### 2. Executor Agent

**Technology:** Python + API Clients

**Input:** Execution plan (JSON array)

**Output:** Execution results (dict)

**Responsibilities:**
- Execute each step sequentially
- Call appropriate APIs
- Handle API errors gracefully
- Collect and structure results

**API Integrations:**

#### OpenWeatherMap API
```python
# Endpoint
GET http://api.openweathermap.org/data/2.5/forecast

# Parameters
{
  "q": "Mumbai,IN",
  "appid": "API_KEY",
  "units": "metric",
  "cnt": 8  # 24 hours in 3-hour intervals
}

# Returns
{
  "city": {...},
  "list": [
    {
      "dt_txt": "2024-02-05 12:00:00",
      "main": {"temp": 28.5, ...},
      "weather": [{"description": "clear sky"}]
    }
  ]
}
```

#### Google Places API
```python
# Endpoint
GET https://maps.googleapis.com/maps/api/place/textsearch/json

# Parameters
{
  "query": "hotels in Mumbai",
  "key": "API_KEY"
}

# Returns
{
  "results": [
    {
      "name": "Taj Hotel",
      "formatted_address": "...",
      "rating": 4.5,
      "user_ratings_total": 1234
    }
  ]
}
```

### 3. Verifier Agent

**Technology:** Claude Sonnet 4.5

**Input:** Plan + Execution results + User query

**Output:** Verification report (JSON)

**Responsibilities:**
- Check completeness
- Validate data quality
- Identify missing information
- Score overall success
- Provide recommendations

**Example Output:**
```json
{
  "verification_passed": true,
  "completeness_score": 95,
  "issues": [],
  "summary": "All required information retrieved successfully",
  "recommendations": [
    "Consider adding hotel price information",
    "Could include travel time between locations"
  ]
}
```

### 4. Multi-Agent Orchestrator

**Technology:** Python coordination layer

**Responsibilities:**
- Initialize all agents
- Manage execution sequence
- Handle inter-agent communication
- Aggregate final results
- Generate user-friendly response
- Error handling and recovery

## 🔐 API Key Management

```
Environment Variables (.env)
    ↓
os.environ.get()
    ↓
Passed to respective clients
    ├─ Anthropic client
    ├─ OpenWeather requests
    └─ Google Places requests
```

**Security:**
- Keys stored in `.env` (gitignored)
- Never hardcoded in source
- Not logged or exposed in output

## 📊 Data Flow

```
1. User Query (string)
   ↓
2. Parsed Intent (structured)
   ↓
3. Execution Plan (JSON)
   ↓
4. API Calls (HTTP requests)
   ↓
5. Raw API Data (JSON)
   ↓
6. Processed Results (structured dict)
   ↓
7. Verification Report (JSON)
   ↓
8. Final Response (natural language)
   ↓
9. Display to User
```

## 🎯 Design Decisions

### Why 3 Agents?

1. **Separation of Concerns**
   - Each agent has single responsibility
   - Easier to debug and maintain
   - Can swap implementations independently

2. **Modularity**
   - Add new agents without changing existing ones
   - Can run agents in parallel (future enhancement)

3. **Verification Step**
   - Ensures quality before response
   - Can retry failed steps
   - Provides transparency

### Why Claude Sonnet 4.5?

- **Balanced:** Good quality/speed/cost tradeoff
- **Structured Output:** Native JSON support
- **Tool Use:** Built-in function calling
- **Context Window:** Large enough for complex plans

### Why These APIs?

1. **OpenWeatherMap**
   - Free tier sufficient
   - Reliable uptime
   - Good documentation
   - Global coverage

2. **Google Places**
   - Comprehensive data
   - High accuracy
   - Well-maintained
   - Rich metadata

## 🔄 Error Handling Strategy

```
┌─────────────────┐
│  API Call Fails │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Log Error       │─────▶│ Continue     │
│ Store in        │      │ Other Steps  │
│ errors[]        │      └──────────────┘
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Verifier Notes  │
│ Missing Data    │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Inform User     │
│ (Partial Result)│
└─────────────────┘
```

**Strategy:**
- Fail gracefully on individual steps
- Continue execution when possible
- Aggregate errors for verification
- Provide partial results to user

## 🚀 Scalability Considerations

### Current Implementation
- Sequential execution
- Single-threaded
- Stateless (no persistence)

### Future Enhancements

1. **Parallel Execution**
   ```python
   import asyncio
   
   async def execute_parallel(plan):
       tasks = [execute_step(step) for step in plan]
       results = await asyncio.gather(*tasks)
   ```

2. **Caching Layer**
   ```python
   # Cache API responses for 1 hour
   cache = {
       "weather:Mumbai": {"data": ..., "expires": ...}
   }
   ```

3. **Database Integration**
   ```python
   # Store queries and results
   db.save_query(user_id, query, results)
   ```

4. **Rate Limiting**
   ```python
   # Prevent API quota exhaustion
   rate_limiter.check_and_wait("openweather")
   ```

## 📈 Performance Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Planning Time | 1-2s | <1s |
| Execution Time | 3-5s | 2-3s |
| Verification Time | 1-2s | <1s |
| Total Latency | 5-9s | <5s |

**Bottlenecks:**
1. API response time (3-4s)
2. LLM inference (1-2s per agent)
3. Sequential execution

**Optimizations:**
1. Use async HTTP requests
2. Cache frequently requested data
3. Parallel agent execution where possible

## 🧪 Testing Strategy

### Unit Tests
```python
# Test individual agents
test_planner_creates_valid_plan()
test_executor_handles_api_errors()
test_verifier_scores_accurately()
```

### Integration Tests
```python
# Test full flow
test_end_to_end_query()
test_error_recovery()
test_partial_results()
```

### Load Tests
```python
# Test under load
test_concurrent_queries()
test_api_rate_limits()
```

## 📝 Code Structure

```
trulymadly-genai-assignment/
├── main.py               # Core agents + orchestrator
├── app.py                # Streamlit web interface
├── test.py               # Test suite
├── requirements.txt      # Dependencies
├── .env.example          # API key template
├── README.md             # Main documentation
├── SETUP_GUIDE.md        # Detailed setup
├── QUICKSTART.md         # 5-min quick start
└── ARCHITECTURE.md       # This file
```

## 🔮 Future Roadmap

1. **Additional APIs**
   - Flight booking (Skyscanner)
   - Hotel pricing (Booking.com)
   - Restaurant reservations (OpenTable)

2. **Enhanced Features**
   - Multi-day itineraries
   - Budget optimization
   - User preferences learning
   - Collaborative planning

3. **Technical Improvements**
   - WebSocket for real-time updates
   - Redis for caching
   - PostgreSQL for persistence
   - Kubernetes deployment

---

**Last Updated:** February 2024
**Version:** 1.0.0
