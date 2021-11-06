import ServerControls from './ServerControls';
import ServerStatus from './ServerStatus';

function Header() {
  return (
    <div className="row">
      <div className="col-1">
        <ServerStatus />
      </div>
      <div className="col-11">
        <ServerControls />
      </div>
    </div>
  );
}

export default Header;