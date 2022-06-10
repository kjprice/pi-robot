import ServerControls from './ServerControls';
import ServerStatuses from './ServerStatuses';

function Header() {
  return (
    <div className="row">
      <div className="col-1">
        <ServerStatuses />
      </div>
      <div className="col-11">
        <ServerControls />
      </div>
    </div>
  );
}

export default Header;