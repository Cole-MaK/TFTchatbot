# TFT Chatbot Backend

A simple backend server for the TFT chatbot with a chat endpoint.

## Setup

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run the backend server:
```bash
python3 backend.py
```

3. Build the frontend:
```
npm run build
```

4. Start the frontend in another terminal:
```
cd frontend/
npx serve -s build
```

The server will start on http://localhost:5000.

## API Endpoints

### Chat

- **URL**: `/chat`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "user_message": "Your message here"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
  }
  ```

Currently, the endpoint returns a default Latin response regardless of the input message. 