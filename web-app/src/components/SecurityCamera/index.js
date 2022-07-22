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
const STREAM_URL = 'http://pi3misc2:8999/data/security_videos/stream/stream.m3u8';

let videoStarted = false;

const startHls = () => {
  console.log('starting video')

  console.log(global)
  if ( global.Hls.isSupported() ) {
    console.log('settup hls')
    var video = document.getElementById('video');
    var hls = new global.Hls();
    hls.loadSource(STREAM_URL);
    hls.attachMedia(video);
  }
}

const startVideo = () => {
  if (videoStarted) {
    console.log('video already started')
    return;
  }

  videoStarted = true;

  setTimeout(startHls, 1000);

}

function SecurityCamera(props) {
  const { raspiStatusesByHostname } = props;

  const hostnamesRunningSecurityCamera = devicesRunningSecurityCamera(raspiStatusesByHostname);

  startVideo();
  return (
    <div>
      <h2>Devices Running Security Camera</h2>
      {hostnamesRunningSecurityCamera.map(hostname => <div key={hostname}>{hostname}</div>)}
      <div>
        Video Source: <a href={STREAM_URL}>{STREAM_URL}</a>
      </div>
      <video id="video" crossOrigin="use-credentials" autoPlay controls>
        {/* <source src="http://pi3misc2:8999/stream.m3u8" type="application/x-mpegURL" /> */}
        <source src={STREAM_URL} type="application/x-mpegURL" />
        {/* <source src="http://pi3misc2:8000/stream.m3u8" type="application/x-mpegURL" /> */}
      </video>
    </div>
  );
}

export default connect(mapStateToProps)(SecurityCamera);