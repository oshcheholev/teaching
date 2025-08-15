import React, { useState, useEffect } from 'react';
import AdminCRUD from '../components/AdminCRUD';
import api from '../api';

function AdminDepartments() {
    const [institutes, setInstitutes] = useState([]);
    const [loadingInstitutes, setLoadingInstitutes] = useState(true);

    const fields = [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'name', label: 'Name', type: 'text' },
        { key: 'institute', label: 'Institute', type: 'foreign_key' },
    ];

    // Fetch institutes on component mount
    useEffect(() => {
        const fetchInstitutes = async () => {
            try {
                const response = await api.get('/api/institutes/');
                setInstitutes(response.data);
            } catch (error) {
                console.error('Failed to fetch institutes:', error);
            } finally {
                setLoadingInstitutes(false);
            }
        };

        fetchInstitutes();
    }, []);

    // Create fields with dynamic institute options
    const createFields = [
        { key: 'name', label: 'Department Name', type: 'text', required: true },
        { 
            key: 'institute', 
            label: 'Institute', 
            type: 'select', 
            required: true,
            options: institutes.map(institute => ({
                value: institute.id,
                label: institute.name
            }))
        },
    ];

    return (
        <div>
            {loadingInstitutes ? (
                <div style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#fff3cd', borderRadius: '5px' }}>
                    <p>Loading institute options...</p>
                </div>
            ) : (
                <AdminCRUD
                    entityName="Department"
                    apiEndpoint="/api/departments/"
                    fields={fields}
                    createFields={createFields}
                    title="Manage Departments"
                />
            )}
        </div>
    );
}

export default AdminDepartments;
