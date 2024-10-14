const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const io = require('socket.io')(server);

io.on('connection', (socket) => {
  console.log('A user connected');
  socket.on('message_esp32', (data) => {
    console.log('Received data from ESP32:', data);
    // Process the received data from the ESP32 here
    // For example, you might send a response back to the ESP32:
    socket.emit('response', 'Data received successfully');
  });
});

server.listen(3000,'192.168.8.250', () => {
  console.log('listening on *:3000');
});