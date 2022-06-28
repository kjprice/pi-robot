import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import ServerStatus from "./misc/ServerStatus";
import { SERVER_STATUSES } from '../redux/constants/server-constants';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config, raspiStatusesByHostname } = serverReducers;
  const { serverHostnames } = config;

  return {
    serverHostnames,
    raspiStatusesByHostname
  };
};

const RaspiTextItem = props => {
  const { hostname, serverStatus} = props;

  if (serverStatus == SERVER_STATUSES.OFFLINE) {
    return hostname;
  }

  return <Link to={`/raspberry/${hostname}`}>{hostname}</Link>
}

const ServerStatuses = (props) => {
  const { serverHostnames, raspiStatusesByHostname } = props;

  if (!serverHostnames) {
    return null;
  }
  
  return serverHostnames.map(hostname => {
    const serverStatus = raspiStatusesByHostname[hostname] || SERVER_STATUSES.OFFLINE
    return (
      <li key={hostname}>
        <RaspiTextItem hostname={hostname} serverStatus={serverStatus} /> <ServerStatus serverStatus={serverStatus} />
      </li>
    )
})
}

function SideBar(props) {
  return (
    <aside id="sidebar" className="p-3">
      <h3>Robot Web App</h3>
      <ul className="list-unstyled">
        <li><Link to="/">Camera Robot</Link></li>
        <li><Link to="/security_camera">Security Camera</Link></li>
      </ul>
      <h5>Raspberry Pis</h5>
      <ul className="list-unstyled">
        {ServerStatuses(props)}
      </ul>
    </aside>
  )
}

export default connect(mapStateToProps)(SideBar);