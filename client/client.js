/**
 * client.js
 * This file contains the logic  for the frontend client.
 * The code displays different html elements according to the socket route used. 
 */

console.log("client.js running...")

    const socket = io("http://127.0.0.1:5000")
    var statusTextElement = document.getElementById("statusText");

    socket.on("connect", () => {
        statusTextElement.textContent = "connected"
        console.log("socket.connected"); 
    });

    socket.on("disconnect", () => {
       
        statusTextElement.textContent = "disconnected"
        console.log("disconnected"); 
    });

    socket.on('moves', data =>{
        document.getElementById('moves').innerHTML = JSON.stringify(data, null, 2);
    });

    socket.on("analysis", data =>{
        lines = data
        document.getElementById('line1').innerHTML = lines[0]
        document.getElementById('line2').innerHTML = lines[1]
        document.getElementById('line3').innerHTML = lines[2]

    });

    socket.on("gameover", data =>{
      document.getElementById('line1').innerHTML = "game over"
      document.getElementById('line2').innerHTML = ""
      document.getElementById('line3').innerHTML = ""
    })