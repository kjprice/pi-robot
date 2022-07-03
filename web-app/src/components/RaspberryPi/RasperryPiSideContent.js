import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import { connect } from 'react-redux';


const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config } = serverReducers;
  const { portsByProcess } = config;

  const { nodeServerStatus } = portsByProcess || {};

  return {
    nodeServerStatusPort: nodeServerStatus,
  };
};

const getLinkForMostRecentLog = (hostname, processName, nodeServerStatusPort) => {
  // TOOD: Should be in a helper function probably as this might be needed other places
  return `http://${hostname}:${nodeServerStatusPort}/readLog/${processName}`;
}

const getMostRecentLog = (hostname, processName, nodeServerStatusPort) => {
  const link = getLinkForMostRecentLog(hostname, processName, nodeServerStatusPort);

  return fetch(link, {
    mode: 'cors'
  })
  .then(res => {
    return res.text().then(txt => {
      if (!res.ok) {
        throw new Error(txt);
      }

      return txt;
    });
  });
}

const FormattedLog = ({ logString }) => {
  return logString.split('\n').map((logLine, i) => <div key={`${i}{logLine}`}>
    <code>{logLine}</code>
  </div>);
}

const DisplayMostRecentLog = props => {
  const { nodeServerStatusPort } = props;

  let params = useParams();
  const { hostname, processName } = params;

  const [recentLogByProcess, setRecentLog] = useState({});

  const fetchAndSetLog = () => {
    return getMostRecentLog(hostname, processName, nodeServerStatusPort)
    .catch(txt => {
      return txt.message || txt;
    })
    .then(txt => {
      setRecentLog({...recentLogByProcess, [processName]: txt});
    });
  }

  useEffect(() => {
    if (!recentLogByProcess[processName] && nodeServerStatusPort) {
      fetchAndSetLog();
    };
  })
  

  if (!recentLogByProcess[processName]) {
    return '';
  }

  return <div>
    <h4>Newest Log For Process "{processName}"</h4>
    <div><button className='btn' type='button' onClick={fetchAndSetLog}>Refresh</button></div>
    <div><FormattedLog logString={recentLogByProcess[processName]} /></div>
  </div>;
}

const RasperryPiSideContent = props => {
  const { nodeServerStatusPort } = props;
  let params = useParams();
  const { additionalInfo } = params;

  switch (additionalInfo) {
    case 'readLog':
      return <DisplayMostRecentLog nodeServerStatusPort={nodeServerStatusPort} />
    default:
      return '';
  }
}


export default connect(mapStateToProps)(RasperryPiSideContent);