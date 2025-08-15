import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import '../styles/AdminDashboard.css';
import HeaderMenu from '../components/HeaderMenu';

function AdminDashboard() {
    const [user, setUser] = useState(null);
    const [stats, setStats] = useState({});
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        checkAdminStatus();
        loadDashboardStats();
    }, []);

    const checkAdminStatus = async () => {
        try {
            const response = await api.get('/api/auth/check-admin/');
            if (!response.data.is_admin) {
                navigate('/admin/login');
                return;
            }
            setUser(response.data);
        } catch (error) {
            console.error('Auth check failed:', error);
            navigate('/admin/login');
        }
    };

    const loadDashboardStats = async () => {
        try {
            const [courses, teachers, courseTypes, institutes, departments, studyPrograms] = await Promise.all([
                api.get('/api/courses/'),
                api.get('/api/teachers/'),
                api.get('/api/course-types/'),
                api.get('/api/institutes/'),
                api.get('/api/departments/'),
                api.get('/api/study-programs/')
            ]);

            setStats({
                courses: courses.data.length,
                teachers: teachers.data.length,
                courseTypes: courseTypes.data.length,
                institutes: institutes.data.length,
                departments: departments.data.length,
                studyPrograms: studyPrograms.data.length
            });
        } catch (error) {
            console.error('Failed to load stats:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('access');
        localStorage.removeItem('refresh');
        localStorage.removeItem('user');
        navigate('/admin/login');
    };

    const adminModules = [
        {
            title: 'Courses',
            count: stats.courses,
            // icon: '📚',
            path: '/admin/courses',
            description: 'Manage course listings and details'
        },
        {
            title: 'Teachers',
            count: stats.teachers,
            // icon: '👨‍🏫',
            path: '/admin/teachers',
            description: 'Manage teacher profiles and information'
        },
        {
            title: 'Course Types',
            count: stats.courseTypes,
            // icon: '📖',
            path: '/admin/course-types',
            description: 'Manage course categories and types'
        },
        {
            title: 'Institutes',
            count: stats.institutes,
            // icon: '🏛️',
            path: '/admin/institutes',
            description: 'Manage institute information'
        },
        {
            title: 'Departments',
            count: stats.departments,
            // icon: '🏢',
            path: '/admin/departments',
            description: 'Manage department details'
        },
        {
            title: 'Study Programs',
            count: stats.studyPrograms,
            // icon: '🎓',
            path: '/admin/study-programs',
            description: 'Manage study program information'
        }
    ];

    if (loading) {
        return (
            <div className="admin-dashboard loading">
                <div className="loading-spinner">Loading...</div>
            </div>
        );
    }

    return (
        <div className="admin-dashboard">
            <HeaderMenu />
            <header className="admin-header">
                <div className="admin-header-content">
                    <div className="admin-title">
                        <h1>Teaching Platform Admin</h1>
                        <p>Welcome back, {user?.username}</p>
                    </div>
                    <div className="admin-actions">
                        <button 
                            onClick={() => navigate('/')}
                            className="btn btn-secondary"
                        >
                            View Site
                        </button>
                        <button 
                            onClick={handleLogout}
                            className="btn btn-danger"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            </header>

            <main className="admin-main">
                <div className="admin-stats">
                    <h2>Dashboard Overview</h2>
                    <div className="stats-grid">
                        {adminModules.map((module, index) => (
                            <div 
                                key={index}
                                className="stat-card"
                                onClick={() => navigate(module.path)}
                            >
                                {/* <div className="stat-icon">{module.icon}</div> */}
                                <div className="stat-content">
                                    <h3>{module.title}</h3>
                                    <p className="stat-count">{module.count || 0}</p>
                                    <p className="stat-description">{module.description}</p>
                                </div>
                                <div className="stat-arrow">→</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* <div className="quick-actions">
                    <h2>Quick Actions</h2>
                    <div className="actions-grid">
                        <button 
                            className="action-btn"
                            onClick={() => navigate('/admin/courses/add')}
                        >
                           Add New Course
                        </button>
                        <button 
                            className="action-btn"
                            onClick={() => navigate('/admin/teachers/add')}
                        >
                            Add New Teacher
                        </button>
                        <button 
                            className="action-btn"
                            onClick={() => navigate('/admin/users')}
                        >
                            Manage Users
                        </button>
                        <button 
                            className="action-btn"
                            onClick={() => window.open('/admin/', '_blank')}
                        >
                            Django Admin
                        </button>
                    </div>
                </div> */}
            </main>
        </div>
    );
}

export default AdminDashboard;
