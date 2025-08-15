
import LoginRegisterForm from '../components/LoginRegisterForm';

function Login() {
  return (
    <div>
      <LoginRegisterForm route="/api/auth/admin-login/" method="login" />
    </div>
  );
}
export default Login;