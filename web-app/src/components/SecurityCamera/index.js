import { connect } from 'react-redux';

const SECURITY_CAMERA_PROCESS_NAME = 'securityCamera';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { raspiStatusesByHostname } = serverReducers;

  return {
    raspiStatusesByHostname,
  };
};

const devicesRunningSecurityCamera = raspiStatusesByHostname => {
  const hostnames = Object.keys(raspiStatusesByHostname);

  return hostnames.filter(hostname => {
    const raspiInfo = raspiStatusesByHostname[hostname] || {};
    const { processes = [] } = raspiInfo;

    return processes.includes(SECURITY_CAMERA_PROCESS_NAME);
  })
}

function SecurityCamera(props) {
  const { raspiStatusesByHostname } = props;

  const hostnamesRunningSecurityCamera = devicesRunningSecurityCamera(raspiStatusesByHostname);

  return (
    <div>
      <h2>Devices Running Security Camera</h2>
      {hostnamesRunningSecurityCamera.map(hostname => <div key={hostname}>{hostname}</div>)}
    </div>
  );
}

export default connect(mapStateToProps)(SecurityCamera);