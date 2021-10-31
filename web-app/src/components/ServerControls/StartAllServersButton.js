import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import { setServerStartInit } from '../../redux/actions/server-actions';
import { SERVER_STATUSES } from '../../redux/constants/server-constants';
import { loadAllServers } from '../../api/handle-socket-connections';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { serversStatus, waitTimeBetweenImages } = serverReducers;
  return {
    serversStatus, waitTimeBetweenImages
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ setServerStartInit }, dispatch)
}

const buttonClassesBase = ['btn', 'btn-success'];
const buttonClassesDisabled = [...buttonClassesBase, 'disabled'];

const buttonClassesByServerStatus = {
  [SERVER_STATUSES.OFFLINE]: buttonClassesBase,
  [SERVER_STATUSES.STARTING]: buttonClassesDisabled,
  [SERVER_STATUSES.STOPPING]: buttonClassesDisabled,
  [SERVER_STATUSES.ONLINE]: buttonClassesDisabled,
};

function getClassName(serversStatus) {
  return buttonClassesByServerStatus[serversStatus].join(' ');
}

function loadAllServersClick(setServerStartInit, waitTimeBetweenImages, remote) {
  setServerStartInit();
  loadAllServers(waitTimeBetweenImages || 0, remote);
}

function getButtonText(remote) {
  if (remote) {
    return 'Start Remote Servers';
  }
  return 'Start Local Servers';
}

function StartAllServersButton(props) {
  const { setServerStartInit, serversStatus, waitTimeBetweenImages, remote=false } = props;
  return (<button
    onClick={() => loadAllServersClick(setServerStartInit, waitTimeBetweenImages, remote)}
    type="button"
    className={getClassName(serversStatus)}>
      {getButtonText(remote)}
    </button>);
}

export default connect(mapStateToProps, mapDispatchToProps)(StartAllServersButton);