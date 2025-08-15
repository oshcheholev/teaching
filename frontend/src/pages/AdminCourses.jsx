import React, { useState, useEffect } from 'react';
import AdminCRUD from '../components/AdminCRUD';
import api from '../api';

function AdminCourses() {
    const [teachers, setTeachers] = useState([]);
    const [courseTypes, setCourseTypes] = useState([]);
    const [institutes, setInstitutes] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [studyPrograms, setStudyPrograms] = useState([]);
    const [loading, setLoading] = useState(true);

    const fields = [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'title', label: 'Title', type: 'text' },
        { key: 'teacher', label: 'Teacher', type: 'foreign_key' },
        { key: 'type', label: 'Course Type', type: 'foreign_key' },
        { key: 'semester', label: 'Semester', type: 'text' },
        { key: 'year', label: 'Year', type: 'number' },
        { key: 'start_date', label: 'Start Date', type: 'date' },
        { key: 'end_date', label: 'End Date', type: 'date' },
        { key: 'credits', label: 'Credits', type: 'number' },
        { key: 'institute', label: 'Institute', type: 'foreign_key' },
        { key: 'department', label: 'Department', type: 'foreign_key' },
        { key: 'study_program', label: 'Study Program', type: 'foreign_key' },
        { key: 'gender_diversity', label: 'Gender Diversity', type: 'boolean' },
    ];

    // Fetch all related data on component mount
    useEffect(() => {
        const fetchAllData = async () => {
            try {
                const [teachersRes, courseTypesRes, institutesRes, departmentsRes, studyProgramsRes] = await Promise.all([
                    api.get('/api/teachers/'),
                    api.get('/api/course-types/'),
                    api.get('/api/institutes/'),
                    api.get('/api/departments/'),
                    api.get('/api/study-programs/')
                ]);

                setTeachers(teachersRes.data);
                setCourseTypes(courseTypesRes.data);
                setInstitutes(institutesRes.data);
                setDepartments(departmentsRes.data);
                setStudyPrograms(studyProgramsRes.data);
            } catch (error) {
                console.error('Failed to fetch related data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchAllData();
    }, []);

    // Create fields with dynamic dropdown options
    const createFields = [
        { key: 'title', label: 'Course Title', type: 'text', required: true },
        { key: 'description', label: 'Description', type: 'textarea' },
        { 
            key: 'teacher', 
            label: 'Teacher', 
            type: 'select', 
            required: true,
            options: loading ? [{ value: '', label: 'Loading teachers...' }] : teachers.map(teacher => ({
                value: teacher.id,
                label: `${teacher.name} (${teacher.subject})`
            }))
        },
        { 
            key: 'type', 
            label: 'Course Type', 
            type: 'select', 
            required: true,
            options: loading ? [{ value: '', label: 'Loading course types...' }] : courseTypes.map(type => ({
                value: type.id,
                label: type.name
            }))
        },
        { key: 'semester', label: 'Semester', type: 'text', required: true },
        { key: 'year', label: 'Year', type: 'number', required: true },
        { key: 'start_date', label: 'Start Date', type: 'date', required: true },
        { key: 'end_date', label: 'End Date', type: 'date', required: true },
        { key: 'credits', label: 'Credits', type: 'number', required: true },
        { 
            key: 'institute', 
            label: 'Institute', 
            type: 'select',
            options: loading ? [{ value: '', label: 'Loading institutes...' }] : [
                { value: '', label: 'Select Institute (Optional)' },
                ...institutes.map(institute => ({
                    value: institute.id,
                    label: institute.name
                }))
            ]
        },
        { 
            key: 'department', 
            label: 'Department', 
            type: 'select',
            options: loading ? [{ value: '', label: 'Loading departments...' }] : [
                { value: '', label: 'Select Department (Optional)' },
                ...departments.map(department => ({
                    value: department.id,
                    label: `${department.name}${department.institute ? ` (${department.institute.name})` : ''}`
                }))
            ]
        },
        { 
            key: 'study_program', 
            label: 'Study Program', 
            type: 'select',
            options: loading ? [{ value: '', label: 'Loading study programs...' }] : [
                { value: '', label: 'Select Study Program (Optional)' },
                ...studyPrograms.map(program => ({
                    value: program.id,
                    label: `${program.name}${program.department ? ` (${program.department.name})` : ''}`
                }))
            ]
        },
        { key: 'gender_diversity', label: 'Gender Diversity', type: 'boolean' },
    ];

    return (
        <AdminCRUD
            entityName="Course"
            apiEndpoint="/api/courses/"
            fields={fields}
            createFields={createFields}
            title="Manage Courses"
        />
    );
}

export default AdminCourses;
