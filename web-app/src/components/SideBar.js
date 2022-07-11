import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import ServerStatus from "./misc/ServerStatus";
import { SERVER_STATUSES } from '../redux/constants/server-constants';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config, raspiStatusesByHostname, webAppServerHostname } = serverReducers;
  const { serverHostnames } = config;

  return {
    serverHostnames,
    raspiStatusesByHostname,
    webAppServerHostname
  };
};

const RaspiTextItem = props => {
  const { hostname} = props;

  return <Link to={`/raspberry/${hostname}`}>{hostname}</Link>
}

const ServerStatuses = (props) => {
  const { serverHostnames, raspiStatusesByHostname } = props;

  if (!serverHostnames) {
    return null;
  }
  
  return serverHostnames.map(hostname => {
    const raspiInfo = raspiStatusesByHostname[hostname] || {};
    const { status } = raspiInfo;
    const serverStatus = status || SERVER_STATUSES.OFFLINE
    return (
      <li key={hostname}>
        <RaspiTextItem hostname={hostname} /> <ServerStatus serverStatus={serverStatus} />
      </li>
    )
  });
}

const WebAppServerStatus = (props) => {
  const { webAppServerHostname } = props;
  return <>
    <h5>Web App Server</h5>
    <div>Connected to:</div>
    <div>{webAppServerHostname}</div>
  </>
}

function SideBar(props) {
  const { webAppServerHostname } = props;

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
      <WebAppServerStatus webAppServerHostname={webAppServerHostname} />
    </aside>
  )
}

export default connect(mapStateToProps)(SideBar);