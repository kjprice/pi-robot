window.onload = () => {
  window.socket = io(window.location.host);

  socket.on("connect", () => {
    console.log(socket.id);

    socket.emit("my_message", "world");
  });
}