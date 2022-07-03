const fs = require('fs');

const getProcesses = () => {
  return new Promise((res) => {
    // TODO: Move filepath to config
    fs.readFile('../../data/processes.json', 'utf8', function (err, data) {
      if (err) {
        return res({})
      }
      obj = JSON.parse(data);
      res(obj);
    });
  });
}

module.exports = getProcesses;