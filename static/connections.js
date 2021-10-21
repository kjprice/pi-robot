window.onload = () => {
  const socket = io("http://kj-macbook.lan:5000/");

  socket.on("connect", () => {
    console.log(socket.id);

    socket.emit("my_message", "world");
  });
}