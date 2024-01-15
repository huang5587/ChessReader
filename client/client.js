    console.log("client.js init 8080?")

    fetch('http://server:8080')
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
  
    const socket = io("http://server:8080")

    socket.on("connect", () => {
        console.log("socket.connected"); // true
    });

    socket.on("disconnect", () => {
        console.log("disconnected"); // true
    });

    socket.on('moves', data =>{
        console.log("Recieving Moves from server", data)
        document.getElementById('moves').innerHTML = JSON.stringify(data, null, 2);
    });

    socket.on("analysis", data =>{
        console.log("Recieving info from server", data)
        test = JSON.stringify(data, null, 2);
        console.log("test", test)
        lines = data
        document.getElementById('line1').innerHTML = lines[0]
        document.getElementById('line2').innerHTML = lines[1]
        document.getElementById('line3').innerHTML = lines[2]

    });