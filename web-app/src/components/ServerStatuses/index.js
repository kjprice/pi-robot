import { connect } from 'react-redux';

import ServerStatus from "../ServerStatus";

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
    <ServerStatus key={serverName} serverStatus={serversStatuses[serverName]} />
  ));
}

export default connect(mapStateToProps)(ServerStatuses);