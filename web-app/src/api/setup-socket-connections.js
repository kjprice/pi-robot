import { bindActionCreators } from 'redux';

import {
  setServerInitialStatus,
  setServerOutputReceived,
  setServerProcessedImageReceived,
  setWebServerOffline,
  setWebServerConnected,
  setRaspiStatuses,
} from '../redux/actions/server-actions';

import { getImageSourceFromArrayBuffer } from '../utilities/image-utilities';

import store from '../redux/store';


function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    setServerInitialStatus,
    setServerOutputReceived,
    setServerProcessedImageReceived,
    setWebServerOffline,
    setWebServerConnected,
    setRaspiStatuses,
    }, dispatch);
}

const actions = mapDispatchToProps(store.dispatch);


const setupNewConnection = (socket => {
  // TODO: Move to socket.js
  socket.on('reconnect', () => {
    console.log('socket reconnect');
    actions.setWebServerConnected();
  });

  socket.on('disconnect', () => {
    console.log('socket disconnect');
    actions.setWebServerOffline();
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

  // TODO: Wire in action
  socket.on('raspi_status_changed', (server) => {
    console.log('raspi_status_changed', server);
    actions.setRaspiStatuses([server]);
  });

  // TODO: This is getting called twice
  socket.on('all_raspi_statuses', (servers) => {
    console.log('all_raspi_statuses', servers);
    actions.setRaspiStatuses(servers)
  });
});

export default setupNewConnection;