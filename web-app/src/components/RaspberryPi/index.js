import { useParams } from "react-router-dom";
import { connect } from 'react-redux';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config } = serverReducers;
  const { ports } = config;

  const { webminPort, pythonFileSystemServerPort, healthStatusPort } = ports || {};

  return {
    webminPort,
    pythonFileSystemServerPort,
    healthStatusPort,
  };
};

const WebminLink = ({hostname, port}) => {
  const link = `https://${hostname}:${port}`;

  return <a href={link} rel="noreferrer" target="_blank">webmin</a>;
}

const DataDirectoryLink = ({hostname, port}) => {
  const link = `http://${hostname}:${port}`;

  return <a href={link} rel="noreferrer" target="_blank">Data Directory</a>;
}

const ServerStatusLink = ({hostname, port, endpoint}) => {
  const link = `http://${hostname}:${port}/${endpoint}`;

  return <a href={link} rel="noreferrer" target="_blank">{endpoint}</a>;
}

const ServerStatusPingLink = (props) => {
  return <ServerStatusLink {...props} endpoint="ping" />
}

const ServerStatusProcessesLink = (props) => {
  return <ServerStatusLink {...props} endpoint="processes" />
}

function RaspberryPi(props) {
  const { webminPort, pythonFileSystemServerPort, healthStatusPort } = props;
  let params = useParams();
  const { hostname } = params;

  console.log({props, params, hostname});
  return (
    <div>
      <h2>{hostname}</h2>

      <h4>Internal Links</h4>
      <ul className="list-unstyled">
        <li><WebminLink hostname={hostname} port={webminPort} /></li>
        <li><DataDirectoryLink hostname={hostname} port={pythonFileSystemServerPort} /></li>
      </ul>

      <h4>Server Status Links</h4>
      <ul className="list-unstyled">
        <li><ServerStatusPingLink hostname={hostname} port={healthStatusPort} /></li>
        <li><ServerStatusProcessesLink hostname={hostname} port={healthStatusPort} /></li>
      </ul>
      
    </div>
)
}

export default connect(mapStateToProps)(RaspberryPi);