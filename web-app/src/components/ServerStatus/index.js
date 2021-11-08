
import OfflineIcon from './StatusIcons/OfflineIcon';
import WaitingIcon from './StatusIcons/WaitingIcon';
import OnlineIcon from './StatusIcons/OnlineIcon';
import { SERVER_STATUSES } from '../../redux/constants/server-constants';

function ServerStatus(props) {
  const { serverStatus } = props;

  switch(serverStatus) {
    case SERVER_STATUSES.OFFLINE:
      return <OfflineIcon />;
    case SERVER_STATUSES.STARTING:
    case SERVER_STATUSES.STOPPING:
      return <WaitingIcon />
    case SERVER_STATUSES.ONLINE:
      return <OnlineIcon />;
    default:
      throw new Error(`Unknown Server Status: ${serverStatus}`)
  }
}

export default ServerStatus;