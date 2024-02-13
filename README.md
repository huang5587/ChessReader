# ChessReader
This repository contains an app that reads and parses chess.com moves and provides real-time analysis and move recommendations. Chess.com moves are scraped by a firefox extension, which then sends the moves to a chess engine upon a local server. The moves are then analyzed and the ideal moves are returned to the user as a webpage.

## Demo
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/U1E2Z1X8KIE?si=KbuIqRnzBvUAbaN_/0.jpg)](https://www.youtube.com/watch?v=U1E2Z1X8KIE?si=KbuIqRnzBvUAbaN_)
<iframe width="560" height="315" src="https://www.youtube.com/embed/U1E2Z1X8KIE?si=KbuIqRnzBvUAbaN_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Installation

ChessReader is deployed and maintained with docker. Installation instructions can be found here: 
> https://docs.docker.com/engine/install/

## Usage
To run ChessReader, run `docker-compose up` from the parent directory (containing docker-compose.yml). This will install necessary dependencies and run all of the components of ChessReader.

Once running you can reach the frontend client at `http://localhost:5050/` from your web browser. 

In order to use ChessReader one must first load the web extension into the browser, and start the server and client interface via command line. 

Using firefox, enter about:debugging into your URL bar. Click on the ThisFirefox tab and then Load Temporary Add-on and load manifest.json. At this point the extension is loaded. Further clarification can be found here: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension#trying_it_out

ChessReader is ready to be used. Login to your chess.com account, get into a game and recieve analysis on the fly!


