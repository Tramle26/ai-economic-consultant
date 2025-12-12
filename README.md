# [EconoSense_AI]

An AI-powered economic consulting assistant that provides real-time insights, forecasts, and strategy recommendations in plain English.

## Project Overview

EconoSense AI platform is a economic website, combining real-time news, financial data, and econometric forecasting to help users understand markets and make data-driven decisions. It is a simplified, chat-based Bloomberg Terminal, allowing users to search economic news and view updated data. There is AI-generated strategic advice backed by real datasets and forecasting models, suggesting economics strategies for users.

## Features

- Smart Search Box: Search stock ticker
- Real-Time News Feed: Live global news updates powered by ALPHA VANTAGE
- AI Consulting Assistant: Generates plain English insights, forecasts, and market entry strategies using GPT models and OpenAi

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Add your API keys to `.env`:
   - Get an Alpha Vantage API key from https://www.alphavantage.co/support/#api-key
   - Get an OpenAI API key from https://platform.openai.com/api-keys
   - Open the `.env` file in your editor and replace the placeholders:
     ```bash
     ALPHAVANTAGE_API_KEY=your-actual-alphavantage-key-here
     OPENAI_API_KEY=your-actual-openai-key-here
     ```
   - **Important**: Make sure your `.env` file is in `.gitignore` (it should be) so you don't accidentally commit your API keys!

## Running the App

```bash
python app.py
```

Then open http://localhost:5000 in your browser.


## Usage
1. Run `python app.py`
2. Type any question into the search bar (e.g., “Vietnam’s GDP for the next 5 years”)
3. View results, charts, real-time news, stock
4. There is a AI chat box to ask questions, giving strategy recommendations (e.g., Should NVIDIA continue to outsource their products to TSMC?)

## Credits
- Tram Le
- Professor Mark Johnson

- AI tools: ChatGPT, Claude, GitHub Copilot, AntiGravity, Cursor
