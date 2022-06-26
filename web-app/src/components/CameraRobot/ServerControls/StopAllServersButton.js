import { connect } from 'react-redux';

import { SERVER_STATUSES } from '../../../redux/constants/server-constants';
import { stopAllServers } from '../../../api/handle-socket-connections';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { serversStatuses } = serverReducers;
  return {
    serversStatuses
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

function getClassName(serversStatuses) {
  return buttonClassesByServerStatus[serversStatuses.allServers].join(' ');
}


function StopAllServersButton(props) {
  const { serversStatuses } = props;
  return (<button onClick={stopAllServers} type="button" className={getClassName(serversStatuses)}>Stop All Servers</button>);
}

export default connect(mapStateToProps)(StopAllServersButton);