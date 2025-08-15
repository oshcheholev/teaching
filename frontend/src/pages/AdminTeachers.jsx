import React from 'react';
import AdminCRUD from '../components/AdminCRUD';

function AdminTeachers() {
    const fields = [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'name', label: 'Name', type: 'text' },
        { key: 'email', label: 'Email', type: 'email' },
        { key: 'subject', label: 'Subject', type: 'text' },
    ];

    const createFields = [
        { key: 'name', label: 'Teacher Name', type: 'text', required: true },
        { key: 'email', label: 'Email', type: 'email', required: true },
        { key: 'subject', label: 'Subject', type: 'text', required: true },
    ];

    return (
        <AdminCRUD
            entityName="Teacher"
            apiEndpoint="/api/teachers/"
            fields={fields}
            createFields={createFields}
            title="Manage Teachers"
        />
    );
}

export default AdminTeachers;
