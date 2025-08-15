import '../styles/DepartmentDetail.css';
import api from '../api';
import Header from '../components/Header';
import BackButton from '../components/BackButton';
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function DepartmentDetail() {
	const { id } = useParams();
	const [department, setDepartment] = useState(null);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		fetchDepartment();
	}, [id]);

	const fetchDepartment = async () => {
		try {
			setLoading(true);
			setError(null);
			const response = await api.get(`/api/departments/${id}/`);
			setDepartment(response.data);
		} catch (err) {
			setError(`Failed to fetch department: ${err.message}`);
		} finally {
			setLoading(false);
		}
	};

	if (loading) return (
		<div>
			<div className="header-container">
				<Header />
			</div>
			<div className="department-detail-page">
				<div className="content-container">
					<BackButton />
					<p>Loading department information...</p>
				</div>
			</div>
		</div>
	);
	
	if (error) return (
		<div>
			<div className="header-container">
				<Header />
			</div>
			<div className="department-detail-page">
				<div className="content-container">
					<BackButton />
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
			<div className="department-detail-page">
				<div className="content-container">
					<BackButton />
					<div className="department-detail-card">
						<h1>{department.name}</h1>
						<div className="department-details">
							{department.institute && (
								<div className="department-detail-item">
									<strong>Institute:</strong> {department.institute.name}
								</div>
							)}
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default DepartmentDetail;
