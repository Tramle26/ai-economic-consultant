# Symbol Search with Stock Data and Related News

We want to enhance the search functionality so that when a user searches for any stock symbol, they receive both the stock price data AND related news articles for that specific symbol in a unified view.

## Feature Overview

When a user searches for a stock symbol (e.g., "AAPL", "MSFT", "GOOGL"), the system should:

1. **Fetch Stock Data** (already implemented)
   - Retrieve daily time series data for the symbol
   - Display price history, OHLCV data, and recent trading information
   - This functionality currently exists in the `/search` route

2. **Fetch Related News** (new functionality)
   - Retrieve news articles specifically related to the searched symbol
   - Use Alpha Vantage NEWS_SENTIMENT API with symbol parameter
   - Display news articles alongside the stock data
   - Show relevant headlines, descriptions, sources, and publication dates

3. **Unified Display**
   - Present stock data and related news together in a cohesive view
   - Make it clear that both sections are related to the searched symbol
   - Maintain consistent styling with the existing UI

## Implementation Requirements

### Backend Changes

**1. New Function: `get_symbol_news(symbol: str)`**
- Create a new function in `app.py` to fetch news for a specific symbol
- Use Alpha Vantage NEWS_SENTIMENT API with `tickers` parameter instead of `topics`
- API call format: `function=NEWS_SENTIMENT&tickers={SYMBOL}&apikey={API_KEY}&limit=50`
- Parse and format the response similar to `get_economic_news()`
- Return a list of news articles formatted consistently with existing news structure
- Handle errors gracefully (invalid symbol, API errors, no news available)

**2. Update `/search` Route**
- Modify the existing `/search` route to call `get_symbol_news()` when a symbol is provided
- Fetch both time series data and symbol-specific news
- Pass both datasets to the template
- Maintain backward compatibility with existing functionality

**3. Data Formatting**
- Ensure news articles follow the same format as `get_economic_news()`:
  - title, description, url, image, source, published_at
- Format dates consistently (YYYY-MM-DD from Alpha Vantage's YYYYMMDDTHHMMSS format)
- Handle missing fields gracefully (use defaults like 'No description available')

### Frontend Changes

**1. Template Updates (`templates/index.html`)**
- Add a new section to display symbol-specific news when a search is performed
- Position the news section near the time series data (below or alongside)
- Use consistent styling with the existing news section
- Show a clear heading indicating these are news articles for the searched symbol
- Display news in a scrollable, card-based layout similar to the economic news section

**2. Visual Design**
- Make it visually clear that the news is related to the searched symbol
- Use a section title like "📰 News for [SYMBOL]" or "Related News: [SYMBOL]"
- Maintain responsive design for mobile and desktop
- Ensure the news section doesn't overwhelm the stock data display

**3. Empty States**
- Handle cases where no news is available for a symbol
- Show a friendly message: "No recent news articles found for [SYMBOL]"
- Don't break the layout when news is unavailable

### AI Context Integration

**1. Context Harness Updates**
- Update `context_harness.py` to include symbol-specific news in the AI context
- When a symbol is searched, include the related news articles in the context data
- Format news for AI consumption: include titles, sources, and dates
- Limit to top 5-10 most relevant articles to keep context manageable

**2. AI Awareness**
- Ensure the AI knows when symbol-specific news is available
- The AI should be able to reference both stock data and related news when answering questions
- Update `get_full_context_data()` to accept and include symbol-specific news

## Implementation Plan

### Phase 1: Backend Function Development

**Step 1: Create `get_symbol_news()` function**
- Implement function in `app.py`
- Use Alpha Vantage NEWS_SENTIMENT API with tickers parameter
- Parse response and format articles consistently
- Add error handling and logging
- Test with various symbols (AAPL, MSFT, invalid symbols)

**Step 2: Update `/search` route**
- Integrate `get_symbol_news()` call into the search route
- Fetch news when symbol is provided
- Pass news data to template alongside time_series
- Test that existing functionality still works

### Phase 2: Frontend Integration

**Step 3: Template Updates**
- Add news display section in `index.html`
- Position it appropriately relative to time series data
- Style consistently with existing news section
- Add empty state handling

**Step 4: UI/UX Refinement**
- Ensure responsive design
- Test on different screen sizes
- Verify visual hierarchy and readability

### Phase 3: AI Context Integration

**Step 5: Context Harness Updates**
- Modify `context_harness.py` to handle symbol-specific news
- Update serialization functions to include symbol news
- Ensure news is formatted for AI consumption

**Step 6: API Integration**
- Update `/api/consult` to include symbol-specific news in context
- Test that AI can reference symbol news in responses

### Phase 4: Testing & Refinement

**Step 7: Functional Testing**
- Test with valid symbols that have news
- Test with valid symbols that have no news
- Test with invalid symbols
- Test error handling and edge cases

**Step 8: Integration Testing**
- Verify stock data and news display together correctly
- Test AI context includes symbol news
- Verify no duplicate API calls
- Check performance with multiple searches

## API Details

### Alpha Vantage NEWS_SENTIMENT for Symbols

**Endpoint:** `https://www.alphavantage.co/query`

**Parameters:**
- `function`: `NEWS_SENTIMENT`
- `tickers`: `{SYMBOL}` (e.g., "AAPL")
- `apikey`: `{API_KEY}`
- `limit`: `50` (optional, default is 50)

**Response Format:**
- Returns JSON with `feed` array containing articles
- Each article has: `title`, `summary`, `url`, `banner_image`, `source`, `time_published`, `ticker_sentiment` (array)
- `ticker_sentiment` contains sentiment data for the symbol

**Example Request:**
```
GET https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey={API_KEY}&limit=50
```

## Benefits

- **Comprehensive View**: Users get both stock data and related news in one search
- **Better Context**: News provides additional context for understanding stock movements
- **Improved UX**: No need to search separately for news about a stock
- **AI Enhancement**: AI can reference both price data and news when answering questions
- **Efficient**: Single search returns all relevant information

## Technical Considerations

- **API Rate Limits**: Be mindful of Alpha Vantage API rate limits when fetching both time series and news
- **Error Handling**: Handle cases where symbol doesn't exist, has no news, or API fails
- **Performance**: Consider caching news data if appropriate (but respect API terms)
- **Data Consistency**: Ensure news formatting matches existing news display patterns
- **Backward Compatibility**: Don't break existing search functionality when no symbol is provided

## Future Enhancements (Optional)

- Add sentiment analysis display for news articles
- Show news articles sorted by relevance or recency
- Add filtering options for news (date range, source)
- Display ticker sentiment scores from the API response
- Add "Load More" functionality for additional news articles

