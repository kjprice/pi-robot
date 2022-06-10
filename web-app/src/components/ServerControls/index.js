import StartAllServersButton from './StartAllServersButton';
import StopAllServersButton from './StopAllServersButton';
import WaitBetweenImagesControl from './WaitBetweenImagesControl';
import ImageRecognitionDropdown from './ImageRecognitionDropdown';


export default function ServerControls() {
  return (
    <div className="row">
    <div className="col-8">
      <div className="row">
      <div className="btn-group">
          <StartAllServersButton/>
          <StartAllServersButton remote/>
          <StopAllServersButton/>
          <ImageRecognitionDropdown />
        </div>
      </div>
    </div>
    <div className="col-4">
      <WaitBetweenImagesControl />
    </div>
  </div>
  );
}