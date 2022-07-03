import { connect } from 'react-redux';
import { Route, Routes } from 'react-router-dom';

import './App.css';
import './api/setup-socket-connections';

import CameraRobot from './components/CameraRobot/';
import SecurityCamera from './components/SecurityCamera';

import RaspberryPi from './components/RaspberryPi'

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
            <Route path="/" element={<CameraRobot />} />
            <Route path="/security_camera" element={<SecurityCamera />} />
            <Route path="raspberry/:hostname" element={<RaspberryPi />} />
            <Route path="raspberry/:hostname/:additionalInfo/:processName" element={<RaspberryPi />} />
          </Routes>
      </div>
    </>
  );
}

export default connect(mapStateToProps)(App);