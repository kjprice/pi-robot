import { bindActionCreators } from 'redux';

import {
  setServerInitialStatus,
  setServerOutputReceived,
  setServerProcessedImageReceived
} from '../redux/actions/server-actions';

import { getImageSourceFromArrayBuffer } from '../utilities/image-utilities';

import socket, { SOCKET_ROOM_NAME } from './socket';
import store from '../redux/store';


function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    setServerInitialStatus,
    setServerOutputReceived,
    setServerProcessedImageReceived
  }, dispatch);
}

const actions = mapDispatchToProps(store.dispatch);


socket.on('connect', () => {
  console.log(socket.id);
  socket.emit('set_socket_room', SOCKET_ROOM_NAME);
  socket.emit('get_server_statuses');
});

socket.on('reconnect', () => {
  console.log('socket reconnect');
});

socket.on('disconnect', () => {
  console.log('socket disconnect');
});

socket.on('browser_init_status', (data) => {
  console.log('browser_init_status', {data});
  actions.setServerInitialStatus(data);
});

function handleImageReceived(arrayBuffer) {
  const processedImage = getImageSourceFromArrayBuffer(arrayBuffer);
  actions.setServerProcessedImageReceived(processedImage);
}

socket.on('processed_image_finished', handleImageReceived);
socket.on('send_output', actions.setServerOutputReceived);
