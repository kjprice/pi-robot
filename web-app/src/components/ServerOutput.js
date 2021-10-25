import { connect } from 'react-redux';
function ServerOutput(props) {
  return (
    <div className="row server-output">
      <div className="col-6" id="image-processing-server-output"></div>
      <div className="col-6" id="camera-head-server-output"></div>
    </div>
  );
}

export default connect()(ServerOutput);