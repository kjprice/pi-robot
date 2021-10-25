import { connect } from 'react-redux';
function ImageContainer(props) {
  return (
    <div id="image-processed-container">
      <img id="image-processed" alt="processed" data-src="/static/images/test-face-image.jpg" />
    </div>
  );
}

export default connect()(ImageContainer);