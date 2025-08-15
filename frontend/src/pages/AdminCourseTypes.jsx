import React from 'react';
import AdminCRUD from '../components/AdminCRUD';

function AdminCourseTypes() {
    const fields = [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'name', label: 'Name', type: 'text' },
        { key: 'description', label: 'Description', type: 'text' },
    ];

    const createFields = [
        { key: 'name', label: 'Course Type Name', type: 'text', required: true },
        { key: 'description', label: 'Description', type: 'textarea', required: false },
    ];

    console.log('AdminCourseTypes createFields:', createFields); // Debug log

    return (
        <AdminCRUD
            entityName="Course Type"
            apiEndpoint="/api/course-types/"
            fields={fields}
            createFields={createFields}
            title="Manage Course Types"
        />
    );
}

export default AdminCourseTypes;
