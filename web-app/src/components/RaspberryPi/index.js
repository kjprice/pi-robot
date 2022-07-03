import { useParams } from "react-router-dom";
import { connect } from 'react-redux';
import { SERVER_STATUSES } from '../../redux/constants/server-constants';
import ServerStatus from "../misc/ServerStatus";

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config, raspiStatusesByHostname } = serverReducers;
  const { ports, portsByProcess, processNames } = config;

  const { webminPort } = ports || {};
  const { nodeServerStatus, pythonHttpServer } = portsByProcess || {};

  return {
    webminPort,
    pythonHttpServer,
    nodeServerStatus,
    raspiStatusesByHostname,
    processNames,
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

const ServerStatusRecentLogLink = (props) => {
  return <ServerStatusLink {...props} endpoint="readLog/nodeServerStatus" />
}

const ProcessDetails = ({ activeProcesses, processName }) => {
  const processStatus = activeProcesses.includes(processName) ? SERVER_STATUSES.ONLINE : SERVER_STATUSES.OFFLINE;

  return (<li>
    {processName} <ServerStatus serverStatus={processStatus} />
  </li>);

}

const AllProcesses = ({ hostname, activeProcesses, processNames, status }) => {
  if (!processNames) {
    return '';
  }
  return (<ul className="list-unstyled">
    {processNames.map(processName => <ProcessDetails key={processName} activeProcesses={activeProcesses} processName={processName} />)}
  </ul>);
}

function RaspberryPi(props) {
  const { processNames, raspiStatusesByHostname, webminPort, pythonHttpServer, nodeServerStatus } = props;
  let params = useParams();
  const { hostname } = params;

  const raspiInfo = raspiStatusesByHostname[hostname] || {}
  const { status, processes = [] } = raspiInfo;

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
        <li><ServerStatusPingLink hostname={hostname} port={nodeServerStatus} /></li>
        <li><ServerStatusProcessesLink hostname={hostname} port={nodeServerStatus} /></li>
        <li><ServerStatusRecentLogLink hostname={hostname} port={nodeServerStatus} /></li>
      </ul>

      <h4>Processes</h4>
      <AllProcesses status={status} hostname={hostname} processNames={processNames} activeProcesses={processes} />
      
    </div>
)
}

export default connect(mapStateToProps)(RaspberryPi);