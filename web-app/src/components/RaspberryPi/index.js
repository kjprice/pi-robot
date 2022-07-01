import { useParams } from "react-router-dom";
import { connect } from 'react-redux';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config, raspiStatusesByHostname } = serverReducers;
  const { ports } = config;

  const { webminPort, pythonHttpServer, healthStatusPort } = ports || {};

  return {
    webminPort,
    pythonHttpServer,
    healthStatusPort,
    raspiStatusesByHostname,
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

const ActiveProcesses = ({ hostname, processes }) => {
  if (processes.length === 0) {
    return 'No active processes found'
  }

  return (<ul className="list-unstyled">
    {processes.map(process => <li key={process}>{process}</li>)}
  </ul>);
}

function RaspberryPi(props) {
  const { raspiStatusesByHostname, webminPort, pythonHttpServer, healthStatusPort } = props;
  let params = useParams();
  const { hostname } = params;

  const raspiInfo = raspiStatusesByHostname[hostname] || {}
  const { processes = [] } = raspiInfo;

  return (
    <div>
      <h2>{hostname}</h2>

      <h4>Internal Links</h4>
      <ul className="list-unstyled">
        <li><WebminLink hostname={hostname} port={webminPort} /></li>
        <li><DataDirectoryLink hostname={hostname} port={pythonHttpServer} /></li>
      </ul>

      <h4>Server Status Links</h4>
      <ul className="list-unstyled">
        <li><ServerStatusPingLink hostname={hostname} port={healthStatusPort} /></li>
        <li><ServerStatusProcessesLink hostname={hostname} port={healthStatusPort} /></li>
      </ul>

      <h4>Active Processes</h4>
      <ActiveProcesses hostname={hostname} processes={processes} />
      
    </div>
)
}

export default connect(mapStateToProps)(RaspberryPi);