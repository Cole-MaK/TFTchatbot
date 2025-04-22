# TFT Chatbot Frontend (React)

A simple React-based chat interface for the TFT chatbot.

## Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

## Running the App

There are three ways to run the app:

### Option 1: Development Server (with hot reloading)

```bash
npm start
```

This will start the React development server and automatically open the app in your browser at http://localhost:3000.

### Option 2: Build and Serve with Node (recommended alternative)

```bash
# First, create a production build
npm run build

# Then serve the build folder
npx serve -s build
```

This will serve the app at http://localhost:3000.

### Option 3: Build and Serve with Python

```bash
# First, create a production build
npm run build

# Then use the included Python server
./serve.py
```

This will also serve the app at http://localhost:3000.

### Troubleshooting: File Watchers Limit

If you encounter this error when using Option 1:
```
Error: ENOSPC: System limit for number of file watchers reached
```

This is because the system has reached its limit for file watchers. You can:

1. Use Option 2 or 3 above to avoid this issue entirely, or
2. Increase the limit on your system:

```bash
# Check current limit
cat /proc/sys/fs/inotify/max_user_watches

# Increase the limit temporarily
sudo sysctl fs.inotify.max_user_watches=524288

# To make it permanent, edit the sysctl configuration
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Important

Make sure the backend server is running at `http://localhost:5000` before using the chat interface.

## Usage

1. Type a message in the input box.
2. Press "Send" or hit Enter.
3. The message will be sent to the backend, and you'll receive a response.

## Building for Production

When you're ready to deploy your app, you can create a production build:
```bash
npm run build
```

This will create optimized files in the `build` folder that you can deploy to a web server. 