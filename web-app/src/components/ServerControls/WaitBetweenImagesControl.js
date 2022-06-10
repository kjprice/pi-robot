import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import { setWaitBetweenImages } from '../../redux/actions/server-actions';
import { sendDelayChange } from '../../api/handle-socket-connections';


const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { waitTimeBetweenImages } = serverReducers;
  return {
    waitTimeBetweenImages
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ setWaitBetweenImages }, dispatch)
}

function waitTimeBetweenImagesInputChange(event, setWaitBetweenImages) {
  const newDelay = event.target.value;

  setWaitBetweenImages(newDelay);
  const newDelayNumber = Number(newDelay);
  if (!Number.isNaN(newDelayNumber)) {
    sendDelayChange(newDelayNumber);
  }
}

function WaitBetweenImagesControl(props) {
  const { waitTimeBetweenImages, setWaitBetweenImages } = props;
  return (
    <div className="input-group mb-3">
      <label htmlFor="wait-time-between-images" className="input-group-text" id="basic-addon1">Delay</label>
      <input onChange={(event) => waitTimeBetweenImagesInputChange(event, setWaitBetweenImages)} id="wait-time-between-images" type="number" className="form-control" placeholder="Delay (in seconds) between images" aria-label="Delay (in seconds) between images" aria-describedby="basic-addon1" value={waitTimeBetweenImages} />
    </div>
  );
}

export default connect(mapStateToProps, mapDispatchToProps)(WaitBetweenImagesControl);