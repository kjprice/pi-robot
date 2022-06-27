const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

const port = require('../../config.json')['healthStatusPort']

app.get('/ping', (req, res) => {
  res.send('success');
})

io.on('connection', (socket) => {
  console.log('a user connected');
});

app.listen(port, () => {
  console.log(`app listening on port ${port}`);
})