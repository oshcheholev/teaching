
import api from "../api";
import "../styles/Header.css";
import HeaderMenu from "./HeaderMenu";

function Header() {

	return (
		<div className="header">
			<div className="logo">
			<h2>base </h2>
			</div>
			<div className="header-menu-container">
				<HeaderMenu />
			</div>
			
		</div>
    );
}
export default Header;