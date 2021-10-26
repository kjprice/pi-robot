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

function loadAllServersClick(setServerStartInit, waitTimeBetweenImages) {
  setServerStartInit();
  loadAllServers(waitTimeBetweenImages || 0);
}

function StartAllServersButton(props) {
  const { setServerStartInit, serversStatus, waitTimeBetweenImages } = props;
  return (<button
    onClick={() => loadAllServersClick(setServerStartInit, waitTimeBetweenImages)}
    type="button"
    className={getClassName(serversStatus)}>
      Start All Servers
    </button>);
}

export default connect(mapStateToProps, mapDispatchToProps)(StartAllServersButton);