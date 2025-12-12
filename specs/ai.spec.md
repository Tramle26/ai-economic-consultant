# Ai agent UX
We want to build an augmented UI for our Economics Consultant AI 
The interface should have two modes
1. A collapsed search input allowing users to type a query
2. When query is sent, open a message window

## Chat UX ehancement
- The UI should not reload when send a message
- Show spinder when submit a query
- Use tailwind to build chat UI
- Move chat UI and server code to its own model

### AI Context "Harness"

- Let's make sure our AI has access to all the same data the user is looking at on the screen
- Design this carefully to allow for data re-use in the UI and server and that were are not replicating things too much
- The AI should have this in the context window so that when the user asks a question it can infer the correct answers from the same data
- make a careful plan in this same section, before starting work

#### AI Context Harness Plan

**Architecture Overview:**
The goal is to create a unified data pipeline where market data flows from APIs → Flask backend → both UI display AND AI context, eliminating redundancy while ensuring the AI has full visibility into what the user sees.

**1. Data Collection Layer**
- Create `context_harness.py` module to aggregate all available market data at query time
- Collect: top gainers/losers/active stocks (from `get_top_movers()`), economic news (from `get_economic_news()`), time-series data for searched symbol, user's current search context
- These endpoints already exist in `app.py` - reuse them

**2. Context Formatting Strategy**
- Serialize collected data into a compact, LLM-friendly format (JSON string)
- Prioritize recent/relevant data (last 5 time-series entries, top 5 stocks per category)
- Format: Include date, ticker, price, change%, volume, news titles/sources
- Compact representation to minimize token usage while preserving essential info

**3. Data Reuse & Deduplication**
- The same data fetched for the UI (top_movers, time_series, news) should be passed to AI
- In `/api/consult` endpoint: call data-gathering functions once, return data to UI AND pass to AI
- Avoid duplicate API calls by reusing existing response data

**4. Integration Points**
- Modify `ai.respond(prompt, context=None)` to accept optional market context
- Append context to the system prompt so AI understands the current market state
- In `/api/consult` endpoint: gather all current data, pass as context parameter
- The AI can now say "Based on the data showing AAPL is the #2 top gainer..." without needing additional lookups

**5. Implementation Sequence**
1. Create `context_harness.py` with data collection & serialization functions
2. Update `ai.respond()` to accept and use context in the system prompt
3. Update `/api/consult` to gather context and pass to `ai.respond()`
4. Test: Verify AI can reference specific stocks/data, no duplicate API calls

**Benefits:**
- AI has full market context without extra API calls
- UI and AI use the same data → consistency
- Questions like "Which of the top gainers would you recommend?" can be answered with the exact data shown to user
- Compact serialization keeps token usage reasonable