import "../styles/HeaderMenu.css";
import { Link } from "react-router-dom";

function HeaderMenu() {
  return (
    <div className="header-menu">
      <ul>
        <li>
          <Link to="/"><img src="/teaching.svg" alt="Teaching" />Teaching</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li>
          <Link to="/admin/login">Admin Login</Link>
        </li>
      </ul>
    </div>
  );
}
export default HeaderMenu;
