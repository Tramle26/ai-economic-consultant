"""
AI Context Harness Module

This module aggregates market data from various sources and formats it
for use in the AI model's context window. It ensures data reuse between
the UI display and AI model, avoiding redundant API calls.
"""

import json
from typing import Optional, Dict, Any, List


def serialize_stock_data(stocks: List[Dict[str, Any]], category: str) -> str:
    """
    Serialize a list of stocks into a compact, LLM-friendly format.
    
    Args:
        stocks: List of stock dictionaries (from top_movers data)
        category: Category name (e.g., "Top Gainers", "Top Losers", "Most Active")
    
    Returns:
        Formatted string representation of stocks
    """
    if not stocks:
        return f"{category}: No data available"
    
    lines = [f"{category}:"]
    # Limit to top 5 for context window efficiency
    for stock in stocks[:5]:
        ticker = stock.get('ticker', 'N/A')
        price = stock.get('price', 'N/A')
        change = stock.get('change_amount', 'N/A')
        change_pct = stock.get('change_percentage', 'N/A')
        volume = stock.get('volume', 'N/A')
        lines.append(
            f"  {ticker}: ${price} ({change} {change_pct}) Volume: {volume}"
        )
    
    return "\n".join(lines)


def serialize_time_series(time_series: Optional[Dict], symbol: str) -> str:
    """
    Serialize time series data into a compact format.
    
    Args:
        time_series: Dictionary of daily time series data
        symbol: Stock ticker symbol
    
    Returns:
        Formatted string representation of time series
    """
    if not time_series:
        return f"Time Series for {symbol}: No data available"
    
    lines = [f"Time Series for {symbol} (Last 5 days):"]
    
    # Sort dates in descending order and take first 5
    sorted_dates = sorted(time_series.keys(), reverse=True)[:5]
    
    for date in sorted_dates:
        data = time_series[date]
        open_price = data.get('1. open', 'N/A')
        close_price = data.get('4. close', 'N/A')
        high = data.get('2. high', 'N/A')
        low = data.get('3. low', 'N/A')
        volume = data.get('6. volume', 'N/A')
        
        lines.append(
            f"  {date}: Open ${open_price}, Close ${close_price}, "
            f"High ${high}, Low ${low}, Volume {volume}"
        )
    
    return "\n".join(lines)


def serialize_news(news_articles: List[Dict[str, Any]]) -> str:
    """
    Serialize economic news into a compact format.
    
    Args:
        news_articles: List of news article dictionaries
    
    Returns:
        Formatted string representation of news
    """
    if not news_articles:
        return "Economic News: No articles available"
    
    lines = ["Economic News Headlines:"]
    
    # Limit to top 5 articles for context efficiency
    for article in news_articles[:5]:
        title = article.get('title', 'N/A')
        source = article.get('source', 'Unknown')
        date = article.get('published_at', 'N/A')
        lines.append(f"  - {title} (Source: {source}, {date})")
    
    return "\n".join(lines)


def serialize_symbol_news(news_articles: List[Dict[str, Any]], symbol: str) -> str:
    """
    Serialize symbol-specific news into a compact format for AI context.
    
    Args:
        news_articles: List of news article dictionaries related to the symbol
        symbol: Stock ticker symbol
    
    Returns:
        Formatted string representation of symbol-specific news
    """
    if not news_articles:
        return f"News for {symbol}: No articles available"
    
    lines = [f"Recent News for {symbol} (Top 10 most relevant articles):"]
    
    # Limit to top 10 articles for symbol-specific news (more relevant than general news)
    for article in news_articles[:10]:
        title = article.get('title', 'N/A')
        source = article.get('source', 'Unknown')
        date = article.get('published_at', 'N/A')
        description = article.get('description', '')
        # Truncate description if too long
        if description and len(description) > 100:
            description = description[:100] + "..."
        lines.append(f"  - {title} (Source: {source}, {date})")
        if description:
            lines.append(f"    Summary: {description}")
    
    return "\n".join(lines)


def format_market_context(
    top_movers: Dict[str, Any],
    time_series: Optional[Dict] = None,
    symbol: Optional[str] = None,
    news: Optional[List[Dict]] = None,
    symbol_news: Optional[List[Dict]] = None,
) -> str:
    """
    Format all market data into a comprehensive context string for the AI model.
    
    This function takes market data (top movers, time series, news) and formats it
    into a readable, token-efficient context that the AI model can reference.
    
    Args:
        top_movers: Dictionary with 'top_gainers', 'top_losers', 'most_actively_traded' keys
        time_series: Optional time series data for a specific symbol
        symbol: Optional symbol being searched (if time series is provided)
        news: Optional list of general economic news articles
        symbol_news: Optional list of news articles specific to the searched symbol
    
    Returns:
        Formatted context string ready for inclusion in AI system prompt
    """
    context_parts = []
    
    # Add search context if symbol is provided
    if symbol:
        context_parts.append(f"User is currently viewing/searching for: {symbol}")
    
    # Add top movers data
    if top_movers:
        context_parts.append(serialize_stock_data(
            top_movers.get('top_gainers', []),
            "Top Gainers"
        ))
        context_parts.append(serialize_stock_data(
            top_movers.get('top_losers', []),
            "Top Losers"
        ))
        context_parts.append(serialize_stock_data(
            top_movers.get('most_actively_traded', []),
            "Most Actively Traded"
        ))
    
    # Add time series if provided
    if time_series and symbol:
        context_parts.append(serialize_time_series(time_series, symbol))
    
    # Add symbol-specific news if provided (prioritize this over general news when symbol is searched)
    if symbol_news and symbol:
        context_parts.append(serialize_symbol_news(symbol_news, symbol))
    
    # Add general economic news if provided (and no symbol-specific news)
    if news and not (symbol_news and symbol):
        context_parts.append(serialize_news(news))
    
    # Join all parts with clear separators
    context_str = "\n\n".join(context_parts)
    
    return context_str


def create_ai_context_prompt(market_context: str) -> str:
    """
    Wrap market context into a formatted prompt addition for the AI system message.
    
    Args:
        market_context: Formatted market data string from format_market_context()
    
    Returns:
        Formatted context block to append to system prompt
    """
    if not market_context.strip():
        return ""
    
    return f"""
You have access to the following current market data and context:

{market_context}

Use this data to inform your responses. When making recommendations or analysis, refer to specific stocks, prices, and trends visible in this data. You can assume the user has this same information on their screen."""


def get_full_context_data(
    top_movers: Dict[str, Any],
    time_series: Optional[Dict] = None,
    symbol: Optional[str] = None,
    news: Optional[List[Dict]] = None,
    symbol_news: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Get complete context data in both formatted string and raw data forms.
    
    Useful when you need both the formatted context for the AI and the raw data
    for other purposes (e.g., passing back to the UI).
    
    Args:
        top_movers: Dictionary with market mover data
        time_series: Optional time series data
        symbol: Optional stock symbol
        news: Optional general economic news articles
        symbol_news: Optional news articles specific to the searched symbol
    
    Returns:
        Dictionary with 'formatted_context' (string) and 'raw_data' (dict)
    """
    formatted = format_market_context(top_movers, time_series, symbol, news, symbol_news)
    
    return {
        "formatted_context": formatted,
        "ai_prompt_addition": create_ai_context_prompt(formatted),
        "raw_data": {
            "top_movers": top_movers,
            "time_series": time_series,
            "symbol": symbol,
            "news": news,
            "symbol_news": symbol_news,
        }
    }
