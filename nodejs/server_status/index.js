const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

const port = require('../../config.json')['healthStatusPort']

const log = (str) => {
  const date = new Date();
  console.log(`${date.toISOString()} \t ${str}`);
}

app.get('/ping', (req, res) => {
  const ip = req.socket.remoteAddress || req.ip || req.headers['x-real-ip'];
  const date = new Date();
  log(`hit "${req.method} ${req.url}" from ip: "${ip}"`);

  res.status(200).send('success');
})

io.on('connection', (socket) => {
  console.log('a user connected');
});

app.listen(port, () => {
  console.log(`app listening on port ${port}`);
})