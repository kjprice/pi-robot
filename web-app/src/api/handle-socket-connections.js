import { bindActionCreators } from 'redux';

import socket from './socket';
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

export function loadAllServers(delay, remote) {
  return new Promise((res, rej) => {
    socket.emit('load_all_servers', { delay, remote });
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

export function sendDelayChange(delay) {
  socket.emit('delay_change', delay);
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