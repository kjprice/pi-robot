const { exec } = require("child_process");

const readRecentLog = (processName) => {
  return new Promise((res, rej) => {
    const command = `~/Projects/pirobot/bin/logs/recent_log_path_by_process_name.sh ${processName}`
    exec(command, (error, stdout, stderr) => {
      console.log({error, stdout, stderr})
      if (error || stderr) {
        return rej(stderr || stdout || (error || {}).message);
      }
      return res(stdout);
    });
  });
};

module.exports = readRecentLog;