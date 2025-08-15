import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../api';
import { getAuthStatus } from '../utils/auth';
import HeaderMenu from './HeaderMenu';
import '../styles/AdminCRUD.css';

function AdminCRUD({ 
    entityName, 
    apiEndpoint, 
    fields, 
    title,
    createFields 
}) {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showForm, setShowForm] = useState(false);
    const [editingItem, setEditingItem] = useState(null);
    const [formData, setFormData] = useState({});
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        // Check authentication status
        const authStatus = getAuthStatus();
        console.log('Auth status:', authStatus);
        
        if (!authStatus.isAuth) {
            console.warn('User not authenticated, redirecting to login...');
            navigate('/admin/login');
            return;
        }
        
        loadItems();
    }, [apiEndpoint, navigate]);

    const loadItems = async () => {
        try {
            setLoading(true);
            const response = await api.get(apiEndpoint);
            setItems(response.data);
        } catch (error) {
            console.error(`Failed to load ${entityName}:`, error);
            setError(`Failed to load ${entityName}`);
        } finally {
            setLoading(false);
        }
    };

    const handleCreate = () => {
        setEditingItem(null);
        setFormData({});
        setShowForm(true);
        setError('');
    };

    const handleEdit = (item) => {
        setEditingItem(item);
        setFormData(item);
        setShowForm(true);
        setError('');
    };

    const handleDelete = async (id) => {
        if (window.confirm(`Are you sure you want to delete this ${entityName.toLowerCase()}?`)) {
            try {
                await api.delete(`${apiEndpoint}${id}/delete/`);
                loadItems();
            } catch (error) {
                console.error('Delete failed:', error);
                setError(`Failed to delete ${entityName.toLowerCase()}`);
            }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Clean the form data - remove empty strings for optional fields
            const cleanedData = { ...formData };
            
            // Convert empty strings to null for optional foreign key fields, but preserve 0 values
            Object.keys(cleanedData).forEach(key => {
                if (cleanedData[key] === '' || cleanedData[key] === null || cleanedData[key] === undefined) {
                    delete cleanedData[key];
                }
                // Convert string numbers to actual numbers for numeric fields
                if (typeof cleanedData[key] === 'string' && !isNaN(cleanedData[key]) && cleanedData[key] !== '') {
                    const numValue = Number(cleanedData[key]);
                    if (!isNaN(numValue)) {
                        cleanedData[key] = numValue;
                    }
                }
            });

            console.log('Submitting course data:', cleanedData); // Debug log

            if (editingItem) {
                // For updates, use the update endpoint
                const response = await api.put(`${apiEndpoint}${editingItem.id}/update/`, cleanedData);
                console.log('Update response:', response);
            } else {
                // For creates, use the add endpoint
                const response = await api.post(`${apiEndpoint}add/`, cleanedData);
                console.log('Create response:', response);
            }
            
            setShowForm(false);
            setFormData({});
            setError(''); // Clear any previous errors
            loadItems();
        } catch (error) {
            console.error('Save failed:', error);
            
            // Extract detailed error message from response
            let errorMessage = `Failed to save ${entityName.toLowerCase()}`;
            if (error.response?.data) {
                if (typeof error.response.data === 'string') {
                    errorMessage = error.response.data;
                } else if (error.response.data.detail) {
                    errorMessage = error.response.data.detail;
                } else if (error.response.data.error) {
                    errorMessage = error.response.data.error;
                } else {
                    // Handle field-specific errors
                    const fieldErrors = [];
                    Object.keys(error.response.data).forEach(field => {
                        const fieldError = error.response.data[field];
                        if (Array.isArray(fieldError)) {
                            fieldErrors.push(`${field}: ${fieldError.join(', ')}`);
                        } else {
                            fieldErrors.push(`${field}: ${fieldError}`);
                        }
                    });
                    if (fieldErrors.length > 0) {
                        errorMessage = fieldErrors.join('; ');
                    }
                }
            }
            
            setError(errorMessage);
        }
    };

    const handleFormChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const renderField = (item, field) => {
        const value = item[field.key];
        
        if (field.type === 'boolean') {
            return value ? '✅ Yes' : '❌ No';
        }
        
        if (field.type === 'date') {
            return new Date(value).toLocaleDateString();
        }
        
        if (field.type === 'foreign_key' && value) {
            if (typeof value === 'object') {
                // Handle foreign key objects - prioritize common name fields
                return value.name || value.title || value.username || value.first_name || value.last_name || `ID: ${value.id}`;
            } else {
                // Handle foreign key IDs
                return `ID: ${value}`;
            }
        }
        
        // Handle any other objects that might slip through
        if (typeof value === 'object' && value !== null) {
            if (value.name) return value.name;
            if (value.title) return value.title;
            if (value.id) return `ID: ${value.id}`;
            return JSON.stringify(value); // Fallback for debugging
        }
        
        return value || '-';
    };

    const renderFormField = (field) => {
        const value = formData[field.key] || '';
        
        switch (field.type) {
            case 'text':
            case 'email':
                return (
                    <input
                        type={field.type}
                        value={value}
                        onChange={(e) => handleFormChange(field.key, e.target.value)}
                        placeholder={field.placeholder || `Enter ${field.label.toLowerCase()}`}
                        required={field.required}
                    />
                );
            case 'number':
                return (
                    <input
                        type="number"
                        value={value}
                        onChange={(e) => handleFormChange(field.key, e.target.value)}
                        placeholder={field.placeholder || `Enter ${field.label.toLowerCase()}`}
                        required={field.required}
                    />
                );
            case 'date':
                return (
                    <input
                        type="date"
                        value={value}
                        onChange={(e) => handleFormChange(field.key, e.target.value)}
                        required={field.required}
                    />
                );
            case 'textarea':
                return (
                    <textarea
                        value={value}
                        onChange={(e) => handleFormChange(field.key, e.target.value)}
                        placeholder={field.placeholder || `Enter ${field.label.toLowerCase()}`}
                        required={field.required}
                        rows={3}
                    />
                );
            case 'boolean':
                return (
                    <label className="checkbox-label">
                        <input
                            type="checkbox"
                            checked={value || false}
                            onChange={(e) => handleFormChange(field.key, e.target.checked)}
                        />
                        {field.label}
                    </label>
                );
            case 'select':
                return (
                    <select
                        value={value}
                        onChange={(e) => handleFormChange(field.key, e.target.value)}
                        required={field.required}
                    >
                        <option value="">Select {field.label}</option>
                        {field.options?.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                );
            default:
                return (
                    <input
                        type="text"
                        value={value}
                        onChange={(e) => handleFormChange(field.key, e.target.value)}
                        placeholder={field.placeholder || `Enter ${field.label.toLowerCase()}`}
                        required={field.required}
                    />
                );
        }
    };

    if (loading) {
        return (
            <div className="admin-crud loading">
                <div className="loading-spinner">Loading {entityName}...</div>
            </div>
        );
    }

    return (
        <div className="admin-crud">
            <HeaderMenu />
            <header className="crud-header">
                <div className="crud-title">
                    <button 
                        onClick={() => navigate('/admin/dashboard')}
                        className="back-btn"
                    >
                        ← Back to Dashboard
                    </button>
                    <h1>{title || `Manage ${entityName}`}</h1>
                </div>
                <button 
                    onClick={handleCreate}
                    className="btn btn-primary"
                >
                    Add New {entityName}
                </button>
            </header>

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {showForm && (
                <div className="form-modal">
                    <div className="form-container">
                        <h3>{editingItem ? `Edit ${entityName}` : `Add New ${entityName}`}</h3>
                        <form onSubmit={handleSubmit}>
                            {(createFields || fields).map(field => (
                                <div key={field.key} className="form-group">
                                    <label>{field.label}{field.required && ' *'}</label>
                                    {renderFormField(field)}
                                </div>
                            ))}
                            <div className="form-actions">
                                <button type="submit" className="btn btn-primary">
                                    {editingItem ? 'Update' : 'Create'}
                                </button>
                                <button 
                                    type="button" 
                                    onClick={() => setShowForm(false)}
                                    className="btn btn-secondary"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <div className="crud-table-container">
                <table className="crud-table">
                    <thead>
                        <tr>
                            {fields.map(field => (
                                <th key={field.key}>{field.label}</th>
                            ))}
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map(item => (
                            <tr key={item.id}>
                                {fields.map(field => (
                                    <td key={field.key}>
                                        {renderField(item, field)}
                                    </td>
                                ))}
                                <td>
                                    <div className="action-buttons">
                                        <button 
                                            onClick={() => handleEdit(item)}
                                            className="btn btn-sm btn-secondary"
                                        >
                                            Edit
                                        </button>
                                        <button 
                                            onClick={() => handleDelete(item.id)}
                                            className="btn btn-sm btn-danger"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {items.length === 0 && (
                    <div className="empty-state">
                        <p>No {entityName.toLowerCase()} found.</p>
                        <button 
                            onClick={handleCreate}
                            className="btn btn-primary"
                        >
                            Add the first {entityName.toLowerCase()}
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AdminCRUD;
