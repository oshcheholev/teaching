import React from 'react';
import AdminCRUD from '../components/AdminCRUD';

function AdminInstitutes() {
    const fields = [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'name', label: 'Name', type: 'text' },
        { key: 'description', label: 'Description', type: 'text' },
    ];

    const createFields = [
        { key: 'name', label: 'Institute Name', type: 'text', required: true },
        { key: 'description', label: 'Description', type: 'textarea' },
    ];

    return (
        <AdminCRUD
            entityName="Institute"
            apiEndpoint="/api/institutes/"
            fields={fields}
            createFields={createFields}
            title="Manage Institutes"
        />
    );
}

export default AdminInstitutes;
