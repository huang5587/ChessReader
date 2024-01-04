console.log("client.js init")
const socket = io("http://127.0.0.1:5050")

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