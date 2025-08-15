import React from 'react';
import LoginRegisterForm from '../components/LoginRegisterForm';

function Register() {
  return (
	<div>
		{/* <h2>Register</h2> */}
		<LoginRegisterForm route="/api/auth/register/" method="register" />
  </div>
  );
}

export default Register;
