import '../styles/TeacherInfo.css';
import api from '../api';
import Header from '../components/Header';
import BackButton from '../components/BackButton';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function TeacherInfo() {
	const { id } = useParams(); // Get the teacher ID from URL parameters
	const [teacher, setTeacher] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		fetchTeacher();
	}, [id]);

	const fetchTeacher = async () => {
		try {
			setLoading(true);
			setError(null);
			const response = await api.get(`/api/teachers/${id}/`);
			setTeacher(response.data);
		} catch (err) {
			setError(`Failed to fetch teacher: ${err.message}`);
		} finally {
			setLoading(false);
		}
	};

	if (loading) return (
		<div>
			<div className="header-container">
				<Header />
			</div>
			<div className="teacher-info-page">
				<div className="content-container">
					<p>Loading teacher information...</p>
				</div>
			</div>
		</div>
	);
	
	if (error) return (
		<div>
			<div className="header-container">
				<Header />
			</div>
			<div className="teacher-info-page">
				<div className="content-container">
					<p style={{ color: 'red' }}>{error}</p>
				</div>
			</div>
		</div>
	);

	return (
		<div>
			<div className="header-container">
				<Header />
			</div>
			<div className="teacher-info-page">
				<div className="content-container">
					<BackButton />
					<div className="teacher-info-detailed">
						<h1>{teacher.name}</h1>
						<div className="teacher-details">
							<div className="teacher-detail-item">
								<strong>Email:</strong> 
								<a href={`mailto:${teacher.email}`} className="teacher-email">
									{teacher.email}
								</a>
							</div>
							<div className="teacher-detail-item">
								<strong>Subject:</strong> {teacher.subject}
							</div>
						</div>
						<div className="teacher-actions">
							<a href={`mailto:${teacher.email}`} className="contact-btn">
								Contact Teacher
							</a>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default TeacherInfo;