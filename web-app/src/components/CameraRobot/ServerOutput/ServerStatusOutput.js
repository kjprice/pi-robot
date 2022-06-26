import { connect } from 'react-redux';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { serverStatusInitMessages } = serverReducers;
  return {
    serverStatusInitMessages
  };
};

function ServerStatusOutputMessages({ statusMessage }) {
  return (<li><b>Step: {statusMessage.step}</b> {statusMessage.details}</li>);
}

function displayServerStatusOutputMessages(messageObject) {
  return <ServerStatusOutputMessages key={messageObject.timestamp} statusMessage={messageObject.statusMessage}/>
}
function ServerStatusOutput({serverStatusInitMessages}) {
  return (
    <ul>
      {serverStatusInitMessages.map(displayServerStatusOutputMessages)}
    </ul>
  );
}

export default connect(mapStateToProps)(ServerStatusOutput);