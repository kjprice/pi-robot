import { Link } from 'react-router-dom';

function SideBar() {
  return (
    <aside id="sidebar" className="p-3">
      <h3>Robot Web App</h3>
      <ul className="list-unstyled">
        <li><Link to="/">Camera Robot</Link></li>
      </ul>
    </aside>
  )
}

export default SideBar;