import { connect } from 'react-redux';

import ServerStatus from "../ServerStatus";
import Tooltip from '../../misc/Tooltip';
import { SERVER_DESCRIPTIONS } from '../../../redux/constants/server-constants';

function mapStateToProps(state) {
  const { serverReducers } = state;
  const { serversStatuses } = serverReducers;
  return {
    serversStatuses
  };
}

function ServerStatuses(props) {
  const { serversStatuses } = props;
  const serverNames = Object.keys(serversStatuses);

  return serverNames.map(serverName => (
    <Tooltip key={serverName} message={SERVER_DESCRIPTIONS[serverName]}>
      <ServerStatus serverStatus={serversStatuses[serverName]} />
    </Tooltip>
  ));
}

export default connect(mapStateToProps)(ServerStatuses);