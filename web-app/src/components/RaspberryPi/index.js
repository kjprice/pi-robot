import { useParams } from "react-router-dom";
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { config } = serverReducers;
  const { webminPort } = config;

  return {
    webminPort
  };
};

const WebminLink = ({hostname, webminPort}) => {
  const link = `https://${hostname}:${webminPort}`;

  return <a href={link} target="_blank">webmin</a>;
}

function RaspberryPi(props) {
  const { webminPort } = props;
  let params = useParams();
  const { hostname } = params;

  console.log({props, params, hostname});
  return (
    <ul className="list-unstyled">
      <li><WebminLink hostname={hostname} webminPort={webminPort} /></li>
    </ul>
)
}

export default connect(mapStateToProps)(RaspberryPi);