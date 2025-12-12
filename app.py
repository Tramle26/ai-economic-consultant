import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, jsonify
import requests
import ai
import context_harness 

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")  # For session management

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def get_time_series_daily(symbol:str):
    url = (
        "https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    )
    r = requests.get(url)
    data = r.json()
    if "Time Series (Daily)" not in data:
        return None, data
    return data["Time Series (Daily)"], None

def get_top_movers():
    """Fetch top movers data from Alpha Vantage API"""
    url = f'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={API_KEY}'
    
    try:
        r = requests.get(url)
        data = r.json()
        
        if 'top_gainers' in data:
            return {
                'top_gainers': data['top_gainers'][:10],
                'top_losers': data['top_losers'][:10],
                'most_actively_traded': data['most_actively_traded'][:10],
                'error': None
            }
        else:
            return {
                'top_gainers': [],
                'top_losers': [],
                'most_actively_traded': [],
                'error': data
            }
    except Exception as e:
        return {
            'top_gainers': [],
            'top_losers': [],
            'most_actively_traded': [],
            'error': str(e)
        }

def get_economic_news():
    """Fetch economic news from Alpha Vantage NEWS_SENTIMENT API"""
    if not API_KEY:
        return []
    
    try:
        # Alpha Vantage NEWS_SENTIMENT endpoint for economic news
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'NEWS_SENTIMENT',
            'topics': 'economy_macro',
            'apikey': API_KEY,
            'limit': 50
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check if we got valid data
        if 'feed' in data:
            articles = data['feed']
            
            # Format articles to match template expectations
            news_list = []
            for article in articles:
                if article.get('title'):
                    # Format date from Alpha Vantage format (YYYYMMDDTHHMMSS) to YYYY-MM-DD
                    published_date = ''
                    if article.get('time_published'):
                        time_str = article.get('time_published')
                        if len(time_str) >= 8:
                            # Format: YYYYMMDDTHHMMSS -> YYYY-MM-DD
                            published_date = f"{time_str[0:4]}-{time_str[4:6]}-{time_str[6:8]}"
                    
                    news_list.append({
                        'title': article.get('title', ''),
                        'description': article.get('summary', '') or 'No description available',
                        'url': article.get('url', ''),
                        'image': article.get('banner_image', '') or article.get('source_logo', ''),
                        'source': article.get('source', 'Unknown'),
                        'published_at': published_date
                    })
            
            return news_list[:50]  # Limit to 50 articles
        else:
            # API might return error message
            print(f"Alpha Vantage news error: {data}")
            return []
    except Exception as e:
        # Return empty list on error (don't break the page)
        print(f"Error fetching news: {str(e)}")
        return []

def get_symbol_news(symbol: str):
    """Fetch news articles specifically related to a stock symbol from Alpha Vantage NEWS_SENTIMENT API"""
    if not API_KEY:
        return []
    
    try:
        # Alpha Vantage NEWS_SENTIMENT endpoint for symbol-specific news
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': symbol.upper(),
            'apikey': API_KEY,
            'limit': 50
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check if we got valid data
        if 'feed' in data:
            articles = data['feed']
            
            # Format articles to match template expectations
            news_list = []
            for article in articles:
                if article.get('title'):
                    # Format date from Alpha Vantage format (YYYYMMDDTHHMMSS) to YYYY-MM-DD
                    published_date = ''
                    if article.get('time_published'):
                        time_str = article.get('time_published')
                        if len(time_str) >= 8:
                            # Format: YYYYMMDDTHHMMSS -> YYYY-MM-DD
                            published_date = f"{time_str[0:4]}-{time_str[4:6]}-{time_str[6:8]}"
                    
                    news_list.append({
                        'title': article.get('title', ''),
                        'description': article.get('summary', '') or 'No description available',
                        'url': article.get('url', ''),
                        'image': article.get('banner_image', '') or article.get('source_logo', ''),
                        'source': article.get('source', 'Unknown'),
                        'published_at': published_date
                    })
            
            return news_list[:50]  # Limit to 50 articles
        else:
            # API might return error message
            print(f"Alpha Vantage symbol news error for {symbol}: {data}")
            return []
    except Exception as e:
        # Return empty list on error (don't break the page)
        print(f"Error fetching symbol news for {symbol}: {str(e)}")
        return []

@app.route('/search')
def search():
    symbol = request.args.get('symbol','').upper()
    time_series = None
    error = None
    symbol_news = None
    if symbol:
        time_series, error = get_time_series_daily(symbol)
        # Fetch symbol-specific news
        symbol_news = get_symbol_news(symbol)
        # Store searched symbol in session for AI context
        session['current_symbol'] = symbol
        session.modified = True
    else:
        # Clear symbol if no search
        session.pop('current_symbol', None)
        session.modified = True
    movers = get_top_movers()
    news = get_economic_news()
    return render_template(
        'index.html',
        data= movers,
        symbol= symbol,
        time_series = time_series,
        search_error= error,
        question=None,
        answer=None,
        ai_error=None,
        chat_history=session.get('chat_history', []),
        news=news,
        symbol_news=symbol_news
    )

@app.route('/')
def index():
    """Main page displaying top movers"""
    # Initialize chat history if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []
    # Clear any previous symbol search when going to main page
    session.pop('current_symbol', None)
    session.modified = True
    data = get_top_movers()
    news = get_economic_news()
    return render_template(
        'index.html',
        data=data,
        symbol=None,
        time_series=None,
        search_error=None,
        question=None,
        answer=None,
        ai_error=None,
        chat_history=session.get('chat_history', []),
        news=news,
        symbol_news=None
    )

@app.route('/api/consult', methods=['POST'])
def api_consult():
    """API endpoint for async chat - returns JSON"""
    data = request.get_json()
    question = data.get('question', '').strip() if data else ''
    
    # Initialize chat history if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    if not question:
        return jsonify({'error': 'Question cannot be empty'}), 400
    
    try:
        # Gather current market data for context (reuse same data for UI and AI)
        movers = get_top_movers()
        news = get_economic_news()
        
        # Get time series if symbol was searched (from request body, session, or query param)
        time_series = None
        symbol = None
        symbol_news = None
        
        # Priority: request body > session > query param
        if data and data.get('symbol'):
            symbol = data.get('symbol').upper().strip()
        elif session.get('current_symbol'):
            symbol = session.get('current_symbol')
        else:
            searched_symbol = request.args.get('symbol', '').upper()
            if searched_symbol:
                symbol = searched_symbol
        
        # Fetch time series and symbol-specific news if we have a symbol
        if symbol:
            time_series, _ = get_time_series_daily(symbol)
            symbol_news = get_symbol_news(symbol)
        
        # Format market context for AI
        context_data = context_harness.get_full_context_data(
            top_movers=movers,
            time_series=time_series,
            symbol=symbol,
            news=news,
            symbol_news=symbol_news
        )
        
        # Get AI response with market context
        market_context = context_data['ai_prompt_addition']
        answer = ai.respond(question, context=market_context)
        
        message = {
            'question': question,
            'answer': answer,
            'error': None
        }
        # Add to chat history
        session['chat_history'].append(message)
        session.modified = True
        return jsonify(message)
    except Exception as e:
        error_msg = str(e)
        message = {
            'question': question,
            'answer': None,
            'error': error_msg
        }
        # Add error to chat history
        session['chat_history'].append(message)
        session.modified = True
        return jsonify(message), 500

@app.route('/consult', methods=['POST'])
def consult():
    """Legacy form endpoint - uses context harness for consistency"""
    question = request.form.get('question', '')
    
    # Initialize chat history if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    if question:
        try:
            # Gather current market data for context (reuse same data for UI and AI)
            movers = get_top_movers()
            news = get_economic_news()
            
            # Get symbol from session if available
            symbol = session.get('current_symbol')
            time_series = None
            symbol_news = None
            if symbol:
                time_series, _ = get_time_series_daily(symbol)
                symbol_news = get_symbol_news(symbol)
            
            # Format market context for AI
            context_data = context_harness.get_full_context_data(
                top_movers=movers,
                time_series=time_series,
                symbol=symbol,
                news=news,
                symbol_news=symbol_news
            )
            
            # Get AI response with market context
            market_context = context_data['ai_prompt_addition']
            answer = ai.respond(question, context=market_context)
            
            # Add to chat history
            session['chat_history'].append({
                'question': question,
                'answer': answer,
                'error': None
            })
        except Exception as e:
            error_msg = str(e)
            # Add error to chat history
            session['chat_history'].append({
                'question': question,
                'answer': None,
                'error': error_msg
            })
        # Mark session as modified
        session.modified = True
    
    movers = get_top_movers()
    news = get_economic_news()
    return render_template(
        'index.html',
        data=movers,
        symbol=None,
        time_series=None,
        search_error=None,
        question='',  # Clear the input after submission
        answer=None,
        ai_error=None,
        chat_history=session.get('chat_history', []),
        news=news,
        symbol_news=None
    )

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Clear the chat history"""
    session['chat_history'] = []
    session.modified = True
    news = get_economic_news()
    return render_template(
        'index.html',
        data=get_top_movers(),
        symbol=None,
        time_series=None,
        search_error=None,
        question=None,
        answer=None,
        ai_error=None,
        chat_history=[],
        news=news,
        symbol_news=None
    )
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

