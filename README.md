# gesture-remote-control/gesture-remote-control/README.md

# Gesture Remote Control

Gesture Remote Control is a project that allows users to control a Chrome extension remotely using hand gestures. The project consists of three main components: a Chrome extension, a remote server, and a client application.

## Project Structure

```
gesture-remote-control
├── chrome-extension
│   ├── manifest.json        # Metadata for the Chrome extension
│   ├── background.js        # Background script for managing events
│   ├── popup.html           # HTML structure for the popup interface
│   ├── popup.js             # JavaScript for handling popup interactions
│   └── README.md            # Documentation for the Chrome extension
├── remote-server
│   ├── src
│   │   ├── server.py        # Implementation of the remote server
│   │   └── requirements.txt  # Python dependencies for the remote server
│   └── README.md            # Documentation for the remote server
├── client
│   ├── src
│   │   ├── client.py        # Implementation of the client application
│   │   └── requirements.txt  # Python dependencies for the client application
│   └── README.md            # Documentation for the client application
└── README.md                # Overall documentation for the project
```

## Installation

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd gesture-remote-control
   ```

2. **Set up the Chrome extension:**
   - Navigate to `chrome-extension/` and load the extension in Chrome by going to `chrome://extensions/`, enabling "Developer mode", and selecting "Load unpacked".

3. **Set up the remote server:**
   - Navigate to `remote-server/src/` and install the required dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the server:
     ```
     python server.py
     ```

4. **Set up the client application:**
   - Navigate to `client/src/` and install the required dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the client:
     ```
     python client.py
     ```

## Usage

- Once the Chrome extension is loaded, you can interact with it through the popup interface.
- The remote server will handle requests from the Chrome extension and communicate with the client application.
- Use hand gestures to control the Chrome extension remotely.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.