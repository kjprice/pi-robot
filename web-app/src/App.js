import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';

import './App.css';
import { setServerLoaded } from './redux/actions/server-actions';
import ServerControls from './components/ServerControls';
import ImageContainer from './components/ImageContainer';
import ServerOutput from './components/ServerOutput';


const mapStateToProps = (props) => {
  console.log('mapStateToProps', props);
  return props;
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ setServerLoaded }, dispatch)
}


function App(props) {
  return (
    <div className="container" id="main-container">
      <ServerControls />
      <ServerOutput />
      <ImageContainer />
    </div>
  );
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
