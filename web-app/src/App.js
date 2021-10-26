import './App.css';
import './api/setup-socket-connections';
import ServerControls from './components/ServerControls';
import ImageContainer from './components/ImageContainer';
import ServerOutput from './components/ServerOutput';



export default function App() {
  return (
    <div className="container" id="main-container">
      <ServerControls />
      <ServerOutput />
      <ImageContainer />
    </div>
  );
}
