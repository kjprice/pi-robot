const ROOM_NAME = 'browsers'

window.addEventListener('load', () => {
  socketLoaded();
  window.socket = io(window.location.host);

  socket.on('connect', () => {
    console.log(socket.id);
    socket.emit('set_socket_room', ROOM_NAME);
    socket.emit('get_server_statuses')
  });

  socket.on('reconnect', () => {
    console.log('socket reconnect');
  });

  socket.on('disconnect', () => {
    console.log('socket disconnect');
  });

  socket.on('browser_init_status', (data) => {
    setInitialState(data);
    console.log('browser_init_status', {data})
  });

  socket.on('processed_image_finished', loadNewImage);
  socket.on('send_output', handleServerOutput);
});

function loadAllServers(statusCallback) {
  return new Promise((res, rej) => {
    window.socket.emit('load_all_servers');
    window.socket.on('all_servers_loading_status', (statusMessage) => {
      if (statusMessage.details == 'complete') {
        window.socket.off('all_servers_loading_status');
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
    }); 
  });
}