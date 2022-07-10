import { bindActionCreators } from 'redux';

import getSocket from './socket';
import store from '../redux/store';
import {
  setServerStartComplete,
  setServerStartUpdateStatus,
  setServerStopInit,
  setServerStopComplete
 } from '../redux/actions/server-actions';

function mapDispatchToProps(dispatch) {
  return bindActionCreators({
    setServerStartComplete,
    setServerStartUpdateStatus,
    setServerStopInit,
    setServerStopComplete
  }, dispatch);
}

const actions = mapDispatchToProps(store.dispatch);

let socket = null;
getSocket().then(foundSocket => {
  socket = foundSocket;
});

export function loadAllServers(delay, remote, classificationModel) {
  return new Promise((res, rej) => {
    socket.emit('load_all_servers', { delay, remote, classification_model: classificationModel });
    socket.on('all_servers_loading_status', (statusMessage) => {
      if (statusMessage.details === 'complete') {
        actions.setServerStartComplete();
        socket.off('all_servers_loading_status');
        return res();
      }
      actions.setServerStartUpdateStatus(statusMessage);
    });
  });
}

export function startProcess(hostname, processName) {
  socket.emit('start_process', { hostname, processName });
}

export function stopProcess(hostname, processName) {
  socket.emit('stop_process', { hostname, processName });
}

export function sendDelayChange(delay) {
  socket.emit('delay_change', delay);
}

export function sendNewClassificationModel(modelName) {
  socket.emit('change_classification_model', modelName)
}

export function stopAllServers() {
  return new Promise((res, rej) => {
    actions.setServerStopInit();
    socket.emit('stop_all_servers');
    socket.on('all_servers_stopped_status', () => {
      actions.setServerStopComplete();
      socket.off('all_servers_stopped_status');
      res();
    }); 
  });
}