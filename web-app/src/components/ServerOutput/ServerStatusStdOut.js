import { connect } from 'react-redux';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { serverOutputByProcessName } = serverReducers;
  return {
    serverOutputByProcessName
  };
};

function getServerContainerColumnClass(serverNamesCount) {
  const colSize = 12 / serverNamesCount;

  return `col-${colSize}`;
}

function Message(props) {
  const { statusMessage } = props;
  const { timestamp, message } = statusMessage;
  return (
    <code key={timestamp}>
      <div className="row">
        <div className="col">
          {timestamp}
        </div>
        <div className="col">
          {message}
        </div>
      </div>
    </code>      
  );
}

function ServerOutputContainer(props) {
  const { serverName, containerClass, statuses, } = props;
  return (
    <div key={serverName} className={containerClass}>
      {statuses.map(statusMessage => {
        const { timestamp } = statusMessage;
        return <Message key={timestamp} statusMessage={statusMessage} />
      })}
    </div>
  )
}

function ServerOutputHeader(props) {
  const { serverName, containerClass } = props;
  return (<div className={containerClass}><h4>{serverName.replaceAll('_', ' ')}</h4></div>)
}

function ServerStatusStdOut({serverOutputByProcessName}) {
  const serverNames = Object.keys(serverOutputByProcessName);
  const serverNamesCount = serverNames.length;

  const containerClass = getServerContainerColumnClass(serverNamesCount);

  return (
    <div className="row server-output">
      <div className="row">
        {serverNames.map(serverName => <ServerOutputHeader key={serverName} serverName={serverName} containerClass={containerClass}/>)}
      </div>
      {serverNames.map(serverName => {
        const statuses = serverOutputByProcessName[serverName];

        return <ServerOutputContainer
          key={serverName}
          serverName={serverName}
          containerClass={containerClass}
          statuses={statuses}
        />
      })}
    </div>
  );
}

export default connect(mapStateToProps)(ServerStatusStdOut);