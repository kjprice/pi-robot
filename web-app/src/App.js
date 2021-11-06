import './App.css';
import './api/setup-socket-connections';
import ServerControls from './components/ServerControls';
import ImageContainer from './components/ImageContainer';
import ServerOutput from './components/ServerOutput';
import ServerStatus from './components/ServerStatus';



export default function App() {
  return (
    <div className="container" id="main-container">
      <div className="row">
        <div className="col-1">
          <ServerStatus />
        </div>
        <div className="col-11">
          <ServerControls />
        </div>
      </div>
      <ServerOutput />
      <ImageContainer />
    </div>
  );
}
