import { connect } from 'react-redux';

import OfflineIcon from './StatusIcons/OfflineIcon';
import WaitingIcon from './StatusIcons/WaitingIcon';
import OnlineIcon from './StatusIcons/OnlineIcon';
import { SERVER_STATUSES } from '../../redux/constants/server-constants';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { serversStatuses } = serverReducers;
  return {
    serversStatuses
  };
}


function ServerStatus(props) {
  const { serversStatuses } = props;

  switch(serversStatuses.allServersStatus) {
    case SERVER_STATUSES.OFFLINE:
      return <OfflineIcon />;
    case SERVER_STATUSES.STARTING:
    case SERVER_STATUSES.STOPPING:
      return <WaitingIcon />
    case SERVER_STATUSES.ONLINE:
      return <OnlineIcon />;
    default:
      throw new Error('Unknown Server Status')
  }
}

export default connect(mapStateToProps)(ServerStatus);