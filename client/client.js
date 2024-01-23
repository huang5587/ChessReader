    console.log("client.js running...")

    fetch('http://127.0.0.1:5000')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Returns a Promise
    })
    .then(data => {
      console.log(data); // Process the fetched JSON data
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });
  
    const socket = io("http://127.0.0.1:5000")
    

    socket.on("connect", () => {
        console.log("socket.connected"); // true
    });

    socket.on("disconnect", () => {
        console.log("disconnected"); // true
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