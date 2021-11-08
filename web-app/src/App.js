import { connect } from 'react-redux';

import './App.css';
import './api/setup-socket-connections';
import ImageContainer from './components/ImageContainer';
import ServerOutput from './components/ServerOutput';
import LoadingPage from './components/LoadingPage';
import Header from './components/Header';
import { SERVER_STATUSES } from './redux/constants/server-constants';


function mapStateToProps(state) {
  const { serverReducers } = state;
  const { serversStatuses } = serverReducers;
  return {
    serversStatuses
  };
}

function App(props) {
  const { serversStatuses } = props;
  if (serversStatuses.webApp === SERVER_STATUSES.OFFLINE) {
    return <LoadingPage />;
  }

  return (
    <div className="container" id="main-container">
      <Header />
      <ServerOutput />
      <ImageContainer />
    </div>
  );
}

export default connect(mapStateToProps)(App);