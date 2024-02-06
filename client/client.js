    console.log("client.js running...")

    const socket = io("http://127.0.0.1:5000")
    
    var shouldDisplayDiv = true; // Change this condition based on your logic


    socket.on("connect", () => {
        document.getElementById('conditionalDiv').innerHTML = "socket is connected";
        console.log("socket.connected"); 
    });

    socket.on("disconnect", () => {
        document.getElementById('conditionalDiv').innerHTML = "socket is disconnected";
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