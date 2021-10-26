import { connect } from 'react-redux';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { processedImage } = serverReducers;
  return {
    processedImage
  };
};

function ImageContainer(props) {
  const { processedImage } = props;
  if (!processedImage) {
    return null;
  }
  return (
    <div id="image-processed-container">
      <img id="image-processed" alt="processed" src={processedImage} />
    </div>
  );
}

export default connect(mapStateToProps)(ImageContainer);