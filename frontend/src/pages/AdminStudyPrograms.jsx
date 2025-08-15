import React, { useState, useEffect } from 'react';
import AdminCRUD from '../components/AdminCRUD';
import api from '../api';

function AdminStudyPrograms() {
    const [departments, setDepartments] = useState([]);
    const [loadingDepartments, setLoadingDepartments] = useState(true);

    const fields = [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'name', label: 'Name', type: 'text' },
        { key: 'description', label: 'Description', type: 'text' },
        { key: 'department', label: 'Department', type: 'foreign_key' },
        { key: 'year', label: 'Year', type: 'number' },
    ];

    // Fetch departments on component mount
    useEffect(() => {
        const fetchDepartments = async () => {
            try {
                const response = await api.get('/api/departments/');
                setDepartments(response.data);
            } catch (error) {
                console.error('Failed to fetch departments:', error);
            } finally {
                setLoadingDepartments(false);
            }
        };

        fetchDepartments();
    }, []);

    // Create fields with dynamic department options
    const createFields = [
        { key: 'name', label: 'Study Program Name', type: 'text', required: true },
        { key: 'description', label: 'Description', type: 'textarea' },
        { 
            key: 'department', 
            label: 'Department', 
            type: 'select', 
            required: true,
            options: departments.map(department => ({
                value: department.id,
                label: `${department.name}${department.institute ? ` (${department.institute.name})` : ''}`
            }))
        },
        { key: 'year', label: 'Year', type: 'number', required: true },
    ];

    return (
        <div>
            {loadingDepartments ? (
                <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#fff3cd', borderRadius: '5px' }}>
                    <p>Loading department options...</p>
                </div>
            ) : (
                <AdminCRUD
                    entityName="Study Program"
                    apiEndpoint="/api/study-programs/"
                    fields={fields}
                    createFields={createFields}
                    title="Manage Study Programs"
                />
            )}
        </div>
    );
}

export default AdminStudyPrograms;
