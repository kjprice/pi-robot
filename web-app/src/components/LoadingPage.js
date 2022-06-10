import Spinner from 'react-bootstrap/Spinner';

function LoadingPage() {
  return (
    <div>
      <Spinner
        as="span"
        animation="border"
        size="sm"
        role="status"
        aria-hidden="true"
      />
      &nbsp;Waiting to connect with Web App Server.
    </div>
  );
}

export default LoadingPage;