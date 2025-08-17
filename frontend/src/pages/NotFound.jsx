import { useState } from 'react'
import { Link } from 'react-router-dom'
import '../styles/NotFound.css'

function NotFound() {
  const [errorMessage, setErrorMessage] = useState('The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.');

  return (
	<div className="not-found">
	  <div className="error-code animation-bounce">404</div>
	  <h1 className="error-title">Page Not Found</h1>
	  <p className="error-description">{errorMessage}</p>
	  
	  <Link to="/" className="back-home-btn">
		← Back to Home
	  </Link>

	  <div className="suggestions">
		<h3>The requested URL was not found on this server.</h3>
		<ul>
		  <li><Link to="/">Go to the homepage</Link></li>
		</ul>
	  </div>
	</div>
  );
}

export default NotFound;
