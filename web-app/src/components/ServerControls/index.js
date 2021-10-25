import { connect } from 'react-redux';
function ServerControls(props) {
  return (
    <div className="row">
    <div className="col-8">
      <div className="row">
        <div className="btn-group">
          <button id="start-all-servers-btn" type="button" className="btn btn-success">Start All Servers</button>
          <button id="stop-all-servers-btn" type="button" className="btn btn-warning disabled">Stop All Servers</button>
        </div>
      </div>
    </div>
    <div className="col-4">
      <div className="input-group mb-3">
        <label htmlFor="wait-time-between-images" className="input-group-text" id="basic-addon1">Delay</label>
        <input id="wait-time-between-images" type="number" className="form-control" placeholder="Delay (in seconds) between images" aria-label="Delay (in seconds) between images" aria-describedby="basic-addon1" value="1" />
      </div>
    </div>
    <div className="d-none" id="start-all-servers-output"></div>
  </div>
  );
}

export default connect()(ServerControls);