# ChessReader
This repository contains an app that reads and parses chess.com moves and provides real-time analysis and move recommendations. Chess.com moves are scraped by a firefox extension, which then sends the moves to a chess engine upon a local server. The moves are then analyzed and the ideal moves are returned to the user as a webpage. Once the game ends, the frontend will send a signal for the backend to automatically save the game into a local database. This way a complete record of games is saved for later use. 

## Demo
https://github.com/huang5587/ChessReader/assets/65338691/fcdf6989-68fa-4436-aeec-c8fd0b50abda

## Installation

ChessReader is deployed and maintained with docker. Installation instructions can be found here: 
> https://docs.docker.com/engine/install/

## Usage
To run ChessReader, run `docker-compose up` from the parent directory (containing docker-compose.yml). This will install necessary dependencies all the components of ChessReader (frontend, backend and database).

Once running you can access the frontend client at `http://localhost:5050/` from your web browser. 

In a new window, open up Chess.com and start a new game against a computer.

Next, in a new tab, open `about:debugging` in your browser, click on the ThisFirefox tab, then Load Temporary Add-on and load manifest.json contained in the extension directory. The web extension should now be loaded. If you can see a green border outlining your screen whilst on chess.com you are good to go. 

At this point you may begin playing and the optimal moves should be automatically displayed on the front end client. 

Note: if you use `docker-compose down` to spin down the container, the database will be wiped. If you wish for your game storage to persist be sure to avoid this.
