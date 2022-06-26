const express = require('express');
const app = express();

const port = require('../../config.json')['health_status_port']

app.get('/ping', (req, res) => {
  res.send('success');
})

app.listen(port, () => {
  console.log(`app listening on port ${port}`);
})