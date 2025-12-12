import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def respond(prompt: str, context: Optional[str] = None) -> str:
    """
    Generate a response from the AI model based on the user's prompt and optional market context.
    
    Args:
        prompt: The user's question or request
        context: Optional market context string containing current stock data, news, etc.
                 This is appended to the system prompt to give the AI awareness of current market state.
    
    Returns:
        The AI model's response as a string
    """
    # Build system prompt with optional context
    system_content = "You are an economic consulting assistant. Explain in clear, simple English."
    
    if context:
        system_content += f"\n\n{context}"
    
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": prompt},
    ]
    resp = client.chat.completions.create(
        model="gpt-4.1",
        temperature=0.33,
        messages=messages,
    )
    return resp.choices[0].message.content
