import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config } = serverReducers;
  const { serverHostnames } = config;

  return {
    serverHostnames
  };
};

const ServerStatuses = (props) => {
  const { serverHostnames } = props;

  if (!serverHostnames) {
    return null;
  }
  
  return serverHostnames.map(hostname => (
    <li key={hostname}>{hostname}</li>
  ))
}

function SideBar(props) {
  return (
    <aside id="sidebar" className="p-3">
      <h3>Robot Web App</h3>
      <ul className="list-unstyled">
        <li><Link to="/">Camera Robot</Link></li>
        <li><Link to="/security_camera">Security Camera</Link></li>
      </ul>
      <h5>Raspberry Pis</h5>
      <ul className="list-unstyled">
        {ServerStatuses(props)}
      </ul>
    </aside>
  )
}

export default connect(mapStateToProps)(SideBar);