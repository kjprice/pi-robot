import { useParams } from "react-router-dom";
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBoxArchive, faPlay, faXmark } from '@fortawesome/free-solid-svg-icons'

import RasperryPiSideContent from './RasperryPiSideContent';
import { startProcess, stopProcess } from '../../api/handle-socket-connections';
import { SERVER_STATUSES } from '../../redux/constants/server-constants';
import ServerStatus from "../misc/ServerStatus";
import Tooltip from '../misc/Tooltip';

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

const RecentLogLink = ({ processName }) => {
  let params = useParams();
  const { hostname } = params;

  return (
    <Tooltip message={"Read most recent log"}>
      <Link to={`/raspberry/${hostname}/readLog/${processName}`}>
        <FontAwesomeIcon icon={faBoxArchive} />
      </Link>
    </Tooltip>
  );
}

const StartProcessLink = ({ processName }) => {
  let params = useParams();
  const { hostname } = params;

  return (
    <Tooltip message={"Start Process"}>
      <button onClick={() => {startProcess(hostname, processName)}} type='button' className="btn">
        <FontAwesomeIcon icon={faPlay} />
      </button>
    </Tooltip>
  );
}

const StopProcessLink = ({ processName }) => {
  let params = useParams();
  const { hostname } = params;

  return (
    <Tooltip message={"Stop Process"}>
      <button onClick={() => {stopProcess(hostname, processName)}} type='button' className="btn">
        <FontAwesomeIcon icon={faXmark} />
      </button>
    </Tooltip>
  );
}

const UpdateProcessStatusButton = ({ processStatus, processName }) => {
  if (processStatus === SERVER_STATUSES.ONLINE) {
    return <StopProcessLink processName={processName} />
  } else {
    return <StartProcessLink processName={processName} />
  }
}

const ProcessDetails = ({ activeProcesses, processName }) => {
  const processStatus = activeProcesses.includes(processName) ? SERVER_STATUSES.ONLINE : SERVER_STATUSES.OFFLINE;

  return (
  <li>
    {processName} <ServerStatus serverStatus={processStatus} />&nbsp;
    <RecentLogLink processName={processName} />
    <UpdateProcessStatusButton processName={processName}  processStatus={processStatus} />
  </li>
  );

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
    <div className="container">
      <div className="row">
        <div className="col-md-3">
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
        <div className="col-md-7">
          <RasperryPiSideContent {...props} />
        </div>
      </div>
    </div>
  );
}

export default connect(mapStateToProps)(RaspberryPi);