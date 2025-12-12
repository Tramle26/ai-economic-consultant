# Search And AI UX Enhancements

We want to enhance the search functionality to create a unified, filtered view when users search for a stock symbol. When a user searches for a stock, the entire interface should dynamically filter to show relevant information, and the AI context should be aware of this search context.

## Search Filtering Requirements

When a user searches for a stock symbol (e.g., "AAPL"), the following areas should be filtered:

1. **Time Series Data** (already implemented)
   - Shows daily price data for the searched symbol below the search box
   - This is currently working

2. **Top Movers Data Filtering**
   - Filter the three stock lists (Top Gainers, Top Losers, Most Actively Traded) to show only stocks matching the search symbol
   - If the searched symbol appears in any of these lists, highlight it prominently
   - If the symbol doesn't appear in the lists, show an empty state or message indicating the symbol isn't in the top movers
   - Consider showing a "clear filter" option to return to full view

3. **News Filtering**
   - Filter the Economic News section to show only news articles related to the searched symbol
   - This may require checking article titles, descriptions, or using symbol matching
   - If no news is found for the symbol, show an appropriate empty state
   - Maintain the same visual layout but with filtered content

4. **Other Relevant Areas**
   - Any other data displays that could be filtered by symbol should also be filtered
   - Ensure consistent filtering behavior across all data sections

## AI Context Integration

The AI context harness should be enhanced to explicitly know about the current search:

1. **Search Context Awareness**
   - When a symbol is searched, the AI should be explicitly informed that the user is currently viewing/focusing on that symbol
   - The context should include a clear statement like: "The user is currently searching/viewing data for [SYMBOL]"
   - This helps the AI understand the user's current focus and provide more relevant responses

2. **Filtered Data Context**
   - The AI should receive information about what filtered data is being shown
   - If the searched symbol appears in top movers, the AI should know its position and ranking
   - If news is filtered, the AI should know which news articles are currently visible
   - This allows the AI to reference the exact data the user is seeing

3. **Context Updates**
   - The search symbol should be passed to the AI context on every query
   - The `/api/consult` endpoint should include the current search symbol in the context
   - The session should maintain the search state so AI queries remember the current search

## Implementation Plan

### Phase 1: Data Filtering

**1. Top Movers Filtering**
- Modify the `/search` route in `app.py` to filter top movers data by symbol
- Update `templates/index.html` to handle filtered data display
- Add visual highlighting for the searched symbol when it appears in lists
- Add a "Clear Filter" button to return to full view

**2. News Filtering**
- Enhance `get_economic_news()` or create a filtering function to filter news by symbol
- This may require checking article content for symbol mentions (ticker symbols in titles/descriptions)
- Update the news section in the template to show filtered results
- Handle cases where no news matches the symbol

**3. UI/UX Enhancements**
- Add visual indicators showing that filters are active
- Show the current search symbol prominently
- Ensure smooth transitions when filtering/unfiltering
- Maintain responsive design during filtering

### Phase 2: AI Context Enhancement

**1. Context Harness Updates**
- Modify `context_harness.py` to include explicit search context information
- Add a function to format search context: "User is currently viewing/searching for [SYMBOL]"
- Update `get_full_context_data()` to include search context when a symbol is provided

**2. API Integration**
- Ensure `/api/consult` endpoint receives and uses the search symbol
- Pass search symbol from frontend JavaScript to the API
- Update session management to maintain search state for AI queries

**3. Context Formatting**
- Format the search context clearly in the AI prompt
- Make it obvious to the AI that the user is focused on a specific symbol
- Include information about filtered data visibility

### Phase 3: Testing & Refinement

**1. Filtering Accuracy**
- Test symbol matching in top movers (exact match, case-insensitive)
- Test news filtering accuracy (symbol mentions in various article fields)
- Handle edge cases (symbols not in movers, no news available)

**2. AI Context Verification**
- Test that AI responses reference the searched symbol appropriately
- Verify AI understands the filtered context
- Ensure AI can answer questions about the currently viewed symbol

**3. User Experience**
- Test filter clearing functionality
- Verify smooth transitions between filtered and unfiltered views
- Ensure search state persists appropriately

## Benefits

- **Unified View**: Users see a focused view of all data related to their search
- **Better AI Responses**: AI understands user's current focus and can provide more relevant answers
- **Improved UX**: Consistent filtering behavior across all data sections
- **Context Awareness**: AI can reference exactly what the user is seeing on screen
- **Efficient Navigation**: Users can quickly filter to see all information about a specific stock

## Technical Considerations

- **Performance**: Filtering should be fast and not require additional API calls
- **Data Reuse**: Reuse existing data structures, avoid duplicating API calls
- **State Management**: Maintain search state in session and pass to frontend appropriately
- **Error Handling**: Handle cases where symbol doesn't exist or has no data
- **Backward Compatibility**: Ensure existing functionality continues to work when no search is active

