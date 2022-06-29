import { io } from 'socket.io-client';

export const SOCKET_ROOM_NAME = 'browsers'
// TODO Move to config
const SOCKET_URI = 'kj-macbook.lan:9898/';
// const SOCKET_URI = 'desktop-u1e9rtd:9898/';

const socket = io(SOCKET_URI);

export default socket;