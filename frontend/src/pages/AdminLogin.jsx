import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants';
import '../styles/AdminLogin.css';
import LoadingIndicator from '../components/LoadingIndicator';
import HeaderMenu from '../components/HeaderMenu';

function AdminLogin() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await api.post('/api/auth/admin-login/', {
                username,
                password
            });

            // Store tokens
            localStorage.setItem(ACCESS_TOKEN, response.data.access);
            localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
            
            // Store user info
            localStorage.setItem('user', JSON.stringify(response.data.user));

            // Redirect to admin dashboard
            navigate('/admin/dashboard');
        } catch (error) {
            console.error('Login error:', error);
            setError(
                error.response?.data?.error || 
                'Login failed. Please check your credentials.'
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="admin-login-container">
            <HeaderMenu />
            <div className="admin-login-card">
                <div className="admin-login-header">
                    <h2>Admin Login</h2>
                    <p>Please enter your admin credentials</p>
                </div>
                
                <form onSubmit={handleSubmit} className="admin-login-form">
                    {error && (
                        <div className="error-message">
                            {error}
                        </div>
                    )}
                    
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            type="text"
                            id="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            required
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                        />
                    </div>
                    
                    <button 
                        type="submit" 
                        className="admin-login-button"
                        disabled={loading}
                    >
                        {loading ? <LoadingIndicator /> : 'Login as Admin'}
                    </button>
                </form>
                
                <div className="admin-login-footer">
                    <p>
                        <a href="/" className="back-link">← Back to Main Site</a>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default AdminLogin;
