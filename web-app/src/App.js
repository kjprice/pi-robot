import { connect } from 'react-redux';
import { Route, Routes } from 'react-router-dom';

import './App.css';
import './api/setup-socket-connections';
import ImageContainer from './components/CameraRobot/ImageContainer';
import ServerOutput from './components/CameraRobot/ServerOutput';
import Header from './components/CameraRobot/Header';
import { SERVER_STATUSES } from './redux/constants/server-constants';
import LoadingPage from './components/LoadingPage';
import SideBar from './components/SideBar';


function mapStateToProps(state) {
  const { serverReducers } = state;
  const { serversStatuses } = serverReducers;
  return {
    serversStatuses
  };
}

function RobotWebApp() {
return (
  <>
    <Header />
    <ServerOutput />
    <ImageContainer />
  </>
);
}

function App(props) {
  const { serversStatuses } = props;
  if (serversStatuses.webApp === SERVER_STATUSES.OFFLINE) {
    return <LoadingPage />;
  }

  return (
    <>
      <SideBar />
      <div className="container" id="main-container">
          <Routes>
            <Route path="/"  element={<RobotWebApp />} />
          </Routes>
      </div>
    </>
  );
}

export default connect(mapStateToProps)(App);