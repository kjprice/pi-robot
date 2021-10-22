window.addEventListener('load', () => {
  socketLoaded();
  window.socket = io(window.location.host);

  socket.on("connect", () => {
    console.log(socket.id);

    socket.emit("my_message", "world");
  });
});

function loadAllServers(statusCallback) {
  return new Promise((res, rej) => {
    window.socket.emit('load_all_servers');
    window.socket.on('all_servers_loading_status', (statusMessage) => {
      if (statusMessage.details == 'complete') {
        window.socket.off('all_servers_loading_status')
        return res();
      }
      statusCallback(statusMessage);
    });
  });
}

function stopAllServers() {
  return new Promise((res, rej) => {
    window.socket.emit('stop_all_servers');
    window.socket.on('all_servers_stopped_status', () => {
      window.socket.off('all_servers_stopped_status');
      res();
    }) ; 
  });
}