import { useParams } from "react-router-dom";
import { connect } from 'react-redux';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config } = serverReducers;
  const { ports } = config;

  const { webminPort, pythonFileSystemServerPort } = ports || {};

  return {
    webminPort,
    pythonFileSystemServerPort,
  };
};

const WebminLink = ({hostname, port}) => {
  const link = `https://${hostname}:${port}`;

  return <a href={link} rel="noreferrer" target="_blank">webmin</a>;
}

const DataDirectoryLink = ({hostname, port}) => {
  const link = `http://${hostname}:${port}`;

  return <a href={link} rel="noreferrer" target="_blank">Data Directory</a>;
}

function RaspberryPi(props) {
  const { webminPort, pythonFileSystemServerPort } = props;
  let params = useParams();
  const { hostname } = params;

  console.log({props, params, hostname});
  return (
    <ul className="list-unstyled">
      <li><WebminLink hostname={hostname} port={webminPort} /></li>
      <li><DataDirectoryLink hostname={hostname} port={pythonFileSystemServerPort} /></li>
    </ul>
)
}

export default connect(mapStateToProps)(RaspberryPi);