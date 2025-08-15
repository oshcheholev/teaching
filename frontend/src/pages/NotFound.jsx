import { useState } from 'react'

function NotFound() {
  const [errorMessage, setErrorMessage] = useState('Page not found');

  return (
	<div className="not-found">
	  <h1>404 - Not Found</h1>
	  <p>{errorMessage}</p>
	</div>
  );
}
export default NotFound;
