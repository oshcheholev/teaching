import { ACCESS_TOKEN } from '../constants';

export const isAuthenticated = () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (!token) return false;
    
    try {
        // Check if token is expired (JWT tokens have expiration)
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentTime = Date.now() / 1000;
        return payload.exp > currentTime;
    } catch (error) {
        console.error('Error parsing token:', error);
        return false;
    }
};

export const clearAuthTokens = () => {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
};

export const getAuthStatus = () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    const user = localStorage.getItem('user');
    
    return {
        hasToken: !!token,
        hasUser: !!user,
        isAuth: isAuthenticated(),
        token: token ? token.substring(0, 20) + '...' : null
    };
};
