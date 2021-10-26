import { connect } from 'react-redux';

import { SERVER_STATUSES } from '../../redux/constants/server-constants';
import { stopAllServers } from '../../api/handle-socket-connections';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { serversStatus } = serverReducers;
  return {
    serversStatus
  };
}

const buttonClassesBase = ['btn', 'btn-warning'];
const buttonClassesDisabled = [...buttonClassesBase, 'disabled'];

const buttonClassesByServerStatus = {
  [SERVER_STATUSES.OFFLINE]: buttonClassesDisabled,
  [SERVER_STATUSES.STARTING]: buttonClassesDisabled,
  [SERVER_STATUSES.STOPPING]: buttonClassesDisabled,
  [SERVER_STATUSES.ONLINE]: buttonClassesBase,
};

function getClassName(serversStatus) {
  return buttonClassesByServerStatus[serversStatus].join(' ');
}


function StopAllServersButton(props) {
  const { serversStatus } = props;
  return (<button onClick={stopAllServers} type="button" className={getClassName(serversStatus)}>Stop All Servers</button>);
}

export default connect(mapStateToProps)(StopAllServersButton);