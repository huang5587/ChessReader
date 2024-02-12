# ChessReader
This repository contains an app that reads and parses chess.com moves and provides real-time analysis and move recommendations. Chess.com moves are scraped by a firefox extension, which then sends the moves to a chess engine upon a local server. The moves are then analyzed and the ideal moves are returned to the user as a webpage.

## Installation

ChessReader is deployed and maintained with docker. Installation instructions can be found here: > https://docs.docker.com/engine/install/

#### pyChess 
pyChess is used to conduct engine analysis and also allows for many convenient chess related functions. Installation instructions can be found here: https://pychess.github.io/download/

### Flask-SocketIO
Flask-SocketIO is used to send and recieve data from server and client. Installation can be found here: https://flask-socketio.readthedocs.io/en/latest/intro.html

### Flask
Flask is used to host the server itself. Installation instructions can be found here: https://flask.palletsprojects.com/en/2.3.x/installation/#

## Usage
In order to use ChessReader one must first load the web extension into the browser, and start the server and client interface via command line. 

Using firefox, enter about:debugging into your URL bar. Click on the ThisFirefox tab and then Load Temporary Add-on and load manifest.json. At this point the extension is loaded. Further clarification can be found here: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension#trying_it_out

The server can be hosted by running the following from the root directiory: 
```
python server.py
```

Then navigate to the client directory and start the client interface by running the following:
```
python -m http.server
```

Access the client interface with your browser at ```localhost:8000 ```

ChessReader is ready to be used. Login to your chess.com account, get into a game and recieve analysis on the fly!


