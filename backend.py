from flask import Flask, request, jsonify
from flask_cors import CORS
from src.frontend_func import frontend_func
from src.function_call import filter_tool
import os
import google
from google import genai
from google.genai.types import Tool
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# chat history list
contents = []

@app.route('/chat', methods=['POST'])
def chat():

    # chat setup
    load_dotenv()
    api_key = os.getenv('API_KEY')
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash-preview-04-17"

    # choose what function we wanna use/test, realistically will have more in the future and will prob init all of them here.
    get_filters_function = filter_tool()
    tools = [Tool(function_declarations=[get_filters_function])]

    system_prompt = "You are an expert in Team fight tactics Set 14 that provides concise and actionable responses. You are data-oriented so data and tables are vital to your thought process and take precident over retrieved information. Users tend to want to know what units or traits to target immediately, rather than large overviews. Provide explanations but keep it brief and short. You're aim is to help players place higher either with average placement, top 4, or delta. Focus on statistics rather than your intuition. Remember even though League of Legends and TFT share champions and items, these are two distinct games. Only answer questions about TFT - Teamfight Tactics. Your response should never start with the phrase, Based on the data. The user can not see the results of the function call so do not reference it."
    
    client_config = {
        "model":model,
        "tools":tools,
        "system":system_prompt,

    }

    # start of user interactions
    on = True
    while on:
        data = request.get_json()
        user_message = data.get('user_message', '')
        
        #append user question to chat history
        contents.append({"parts": [{"text":user_message}], "role":"user"})
        
        llm_response = frontend_func(contents, client, client_config)

        response = {
            "message": f"{llm_response}"
        }

        #append model response to chat history
        contents.append({"parts": [{"text":llm_response}], "role":"model"})
        
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 