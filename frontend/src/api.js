import axios from 'axios';
import {  ACCESS_TOKEN } from './constants';

// Use localhost:8000 for backend API
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
   baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
});

// Helper function to check if token is valid
const isTokenValid = (token) => {
    if (!token) return false;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentTime = Date.now() / 1000;
        return payload.exp > currentTime;
    } catch (error) {
        return false;
    }
};

api.interceptors.request.use(
	config => {
		const token = localStorage.getItem(ACCESS_TOKEN);
		if (token && isTokenValid(token)) {
			config.headers.Authorization = `Bearer ${token}`;
		} else if (token && !isTokenValid(token)) {
			// Remove invalid token
			localStorage.removeItem(ACCESS_TOKEN);
			localStorage.removeItem('refresh_token');
			localStorage.removeItem('user');
		}
		return config;
	},
	error => {
		return Promise.reject(error);
	}
);
export default api;
