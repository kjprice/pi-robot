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

function ServerStatusStdOut({serverOutputByProcessName}) {
  const serverNames = Object.keys(serverOutputByProcessName);
  const serverNamesCount = serverNames.length;

  const containerClass = getServerContainerColumnClass(serverNamesCount);

  // TODO: Refactor
  return (
    <div className="row server-output">
      {serverNames.map(serverName => {
        const statuses = serverOutputByProcessName[serverName];
        return (
          <div key={serverName} className={containerClass}>
            {statuses.map(stuatusMessage => {
              const { timestamp, message } = stuatusMessage;
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
            })}
          </div>
        )
      })}
    </div>
  );
}

export default connect(mapStateToProps)(ServerStatusStdOut);