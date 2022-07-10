import { bindActionCreators } from 'redux';
import { io } from 'socket.io-client';

import {
  setWebServerConnected,
} from '../redux/actions/server-actions';

import store from '../redux/store';

function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    setWebServerConnected,
    }, dispatch);
}

const actions = mapDispatchToProps(store.dispatch);

// TODO Move to config
export const SOCKET_ROOM_NAME = 'browsers'

// TODO: Move to config
const SOCKET_HOSTNAMES = [
  'kj-macbook.lan',
  'localhost',
  'desktop-u1e9rtd',
];

// TODO: Move to config
const SOCKET_PORT = '9898';

const getFirstAvailableSocket = () => {
  return new Promise((res, rej) => {
    SOCKET_HOSTNAMES.forEach(socketHostname => {
      const socketUri = `${socketHostname}:${SOCKET_PORT}/`;
      const socket = io(socketUri);

      const timeout = setTimeout(() => {
        console.log(`Could not connect to ${socketHostname}, giving up.`)
        socket.close();
      }, 3000);
      
      socket.on('connect', () => {
          actions.setWebServerConnected();
          console.log(`Connected to ${socketHostname}`)
          socket.emit('set_socket_room', SOCKET_ROOM_NAME);
          socket.emit('get_server_statuses');
          clearTimeout(timeout);
          res(socket);
      });
    })
  })
}

let socketPromise = null;
let socket = null;
const getSocket = () => {
  if (socket) {
    return Promise.resolve(socket);
  }
  if (socketPromise) {
    return socketPromise;
  }

  socketPromise = new Promise((res, rej) => {
    return getFirstAvailableSocket()
    .then((socketFound) => {  
      socket = socketFound;
      res(socketFound);
    });
  });

  return socketPromise;
}

export default getSocket;