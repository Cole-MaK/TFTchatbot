from flask import Flask, request, jsonify
from flask_cors import CORS
from src.function_call import frontend_func

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('user_message', '')
    
    # For now, just return a default Latin response
    response = {
        "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit test."
    }
    response = {
        "message": f"{frontend_func(user_message)}"
    }
    print(response)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 