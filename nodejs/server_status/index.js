const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const cors = require('cors');

const getProcesses = require('./tools/getProcesses');
const readRecentLog = require('./tools/readRecentLog');

const app = express();
app.use(cors());
const server = http.createServer(app);
const io = new Server(server);

const port = require('../../config.json')['portsByProcess']['nodeServerStatus'];

const log = (str) => {
  const date = new Date();
  console.log(`${date.toISOString()} \t ${str}`);
}

app.get('/ping', (req, res) => {
  const ip = req.socket.remoteAddress || req.ip || req.headers['x-real-ip'];

  log(`hit "${req.method} ${req.url}" from ip: "${ip}"`);

  res.status(200).send('success');
});

app.get('/processes', (req, res) => {
  const ip = req.socket.remoteAddress || req.ip || req.headers['x-real-ip'];
  log(`hit "${req.method} ${req.url}" from ip: "${ip}"`);

  getProcesses().then(processes => {
    const processNames = Object.keys(processes);
    res.status(200).send(processNames);
  });
});

app.get('/readLog/:processName', (req, res) => {
  const ip = req.socket.remoteAddress || req.ip || req.headers['x-real-ip'];
  log(`hit "${req.method} ${req.url}" from ip: "${ip}"`);

  // res.send(req.params.processName);
  readRecentLog(req.params.processName)
  .then(log => res.send(log))
  .catch(err => res.status(404).send(err));

  // getProcesses().then(processes => {
  //   const processNames = Object.keys(processes);
  //   res.status(200).send(processNames);
  // });
})

io.on('connection', (socket) => {
  console.log('a user connected');
});

app.listen(port, () => {
  console.log(`app listening on port ${port}`);
})