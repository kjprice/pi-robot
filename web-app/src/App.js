import './App.css';
import './api/setup-socket-connections';
import ImageContainer from './components/ImageContainer';
import ServerOutput from './components/ServerOutput';
import Header from './components/Header';



export default function App() {
  return (
    <div className="container" id="main-container">
      <Header />
      <ServerOutput />
      <ImageContainer />
    </div>
  );
}
