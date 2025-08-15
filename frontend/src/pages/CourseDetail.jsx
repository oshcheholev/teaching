import '../styles/CourseDetail.css';
import api from '../api';
import Header from '../components/Header';
import BackButton from '../components/BackButton';
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function CourseDetail() {
	const { id } = useParams();
	const [course, setCourse] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		fetchCourse();
	}, [id]);

	const fetchCourse = async () => {
		try {
			setLoading(true);
			setError(null);
			const response = await api.get(`/api/courses/${id}/`);
			setCourse(response.data);
		} catch (err) {
			setError(`Failed to fetch course: ${err.message}`);
		} finally {
			setLoading(false);
		}
	};

	if (loading) return (
		<div>
			<div className="header-container">
				<Header />
			</div>
			<div className="course-detail-page">
				<div className="content-container">
					<p>Loading course information...</p>
				</div>
			</div>
		</div>
	);
	
	if (error) return (
		<div>
			<div className="header-container">
				<Header />
			</div>
			<div className="course-detail-page">
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
			<div className="course-detail-page">
				<div className="content-container">
					<BackButton />
					<div className="course-detail-card">
						<h2>{course.title}</h2>
						<div className="course-details">
							{course.teacher && (
								<div className="course-detail-item">
									{/* <strong>Teacher:</strong>  */}
									<Link to={`/teacher/${course.teacher.id}`} className="teacher-link">
										{course.teacher.name}
									</Link>
								</div>
							)}
							<div className="course-detail-item">
								{/* <strong>Description:</strong>  */}
								{course.institute && (
									<span>{course.institute.name}</span>
								)}
							</div>
							<div className="course-detail-item">
								{/* <strong>Description:</strong>  */}
								{course.description}
							</div>
							{/* <div className="course-detail-item">
								<strong>Credits:</strong> {course.credits}
							</div> */}
							<div className="course-detail-item">
								<strong>Semester:</strong> {course.semester} {course.year}
							</div>
							<div className="course-detail-item">
								<strong>Course enrollment:</strong> {new Date(course.start_date).toLocaleDateString()}
								<p>Via online registration</p>
							</div>
							{/* <div className="course-detail-item">
								<strong>End Date:</strong> {new Date(course.end_date).toLocaleDateString()}
							</div> */}
							{course.type && (
								<div className="course-detail-item">
									<strong>Type:</strong> {course.type.name}
								</div>
							)}
							{/* <div className="course-detail-item">
								<strong>Gender Diversity:</strong> {course.gender_diversity ? 'Yes' : 'No'}
							</div> */}
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default CourseDetail;
