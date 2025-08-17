import React, { useState, useEffect } from 'react';
import api from '../api';
import '../styles/CourseList.css';
import CourseShort from './CourseShort';

function CourseList({ filters = { query: "", selectedTeachers: [] } }) {
	const [courses, setCourses] = useState([]);
	const [filteredCourses, setFilteredCourses] = useState([]);
	const [paginatedCourses, setPaginatedCourses] = useState([]);
	const [currentPage, setCurrentPage] = useState(1);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);
	
	const COURSES_PER_PAGE = 20;

	// Fetch courses from API
	useEffect(() => {
		fetchCourses();
	}, [filters]); // Add filters as dependency

	const fetchCourses = async () => {
		try {
			setLoading(true);
			setError(null);
			
			// Build query parameters from filters
			const params = new URLSearchParams();
			
			// Add search query
			if (filters.query && filters.query.trim()) {
				params.append('search', filters.query.trim());
			}
			
			// Add gender/diversity filter
			if (filters.genderDiversityFilter) {
				params.append('gender_diversity', 'true');
			}
			
			// Add semester filter
			if (filters.selectedSemesters && filters.selectedSemesters.length > 0) {
				params.append('semester_format', filters.selectedSemesters[0].name);
			}
			
			// Add teacher filter
			if (filters.selectedTeachers && filters.selectedTeachers.length > 0) {
				filters.selectedTeachers.forEach(teacher => {
					params.append('teacher', teacher.id);
				});
			}
			
			// Add course type filter
			if (filters.selectedCourseTypes && filters.selectedCourseTypes.length > 0) {
				filters.selectedCourseTypes.forEach(type => {
					params.append('type', type.id);
				});
			}
			
			// Add institute filter
			if (filters.selectedInstitutes && filters.selectedInstitutes.length > 0) {
				filters.selectedInstitutes.forEach(institute => {
					params.append('institute', institute.id);
				});
			}
			
			// Add department filter
			if (filters.selectedDepartments && filters.selectedDepartments.length > 0) {
				filters.selectedDepartments.forEach(dept => {
					params.append('department', dept.id);
				});
			}
			
			// Add study program filter
			if (filters.selectedStudyPrograms && filters.selectedStudyPrograms.length > 0) {
				filters.selectedStudyPrograms.forEach(program => {
					params.append('study_program', program.id);
				});
			}
			
			const queryString = params.toString();
			const url = queryString ? `/api/courses/?${queryString}` : '/api/courses/';
			
			console.log("Fetching courses with URL:", url);
			const response = await api.get(url);
			console.log("Courses response:", response.data);
			setCourses(response.data);
			setFilteredCourses(response.data); // Since filtering is done server-side
		} catch (err) {
			console.error("Error fetching courses:", err);
			setError(`Failed to fetch courses: ${err.message}`);
		} finally {
			setLoading(false);
		}
	};

	// Apply pagination when filtered courses or current page changes
	useEffect(() => {
		applyPagination();
	}, [filteredCourses, currentPage]);

	// Reset to first page when filters change
	useEffect(() => {
		setCurrentPage(1);
	}, [filters]);

	const applyPagination = () => {
		const startIndex = (currentPage - 1) * COURSES_PER_PAGE;
		const endIndex = startIndex + COURSES_PER_PAGE;
		const paginated = filteredCourses.slice(startIndex, endIndex);
		setPaginatedCourses(paginated);
	};

	const totalPages = Math.ceil(filteredCourses.length / COURSES_PER_PAGE);

	const handlePageChange = (page) => {
		setCurrentPage(page);
		// Scroll to top of course list when page changes
		window.scrollTo({ top: 0, behavior: 'smooth' });
	};

	const getPageNumbers = () => {
		const pageNumbers = [];
		const maxVisiblePages = 5;
		
		if (totalPages <= maxVisiblePages) {
			// Show all pages if total is small
			for (let i = 1; i <= totalPages; i++) {
				pageNumbers.push(i);
			}
		} else {
			// Show smart pagination with ellipsis
			if (currentPage <= 3) {
				// Show first pages
				for (let i = 1; i <= 4; i++) {
					pageNumbers.push(i);
				}
				pageNumbers.push('...');
				pageNumbers.push(totalPages);
			} else if (currentPage >= totalPages - 2) {
				// Show last pages
				pageNumbers.push(1);
				pageNumbers.push('...');
				for (let i = totalPages - 3; i <= totalPages; i++) {
					pageNumbers.push(i);
				}
			} else {
				// Show middle pages
				pageNumbers.push(1);
				pageNumbers.push('...');
				for (let i = currentPage - 1; i <= currentPage + 1; i++) {
					pageNumbers.push(i);
				}
				pageNumbers.push('...');
				pageNumbers.push(totalPages);
			}
		}
		
		return pageNumbers;
	};

	return (
		<div className="course-list-container">
			{loading && <p className="loading-message">Loading courses...</p>}
			
			{error && (
				<div className="error-message">
					<p>Error: {error}</p>
					<p>Note: Please check your connection and try again.</p>
				</div>
			)}
			
			{!loading && !error && (
				<>
					{/* Results summary */}
					<div className="results-summary">
						<p>
							Showing {paginatedCourses.length > 0 ? 
								`${(currentPage - 1) * COURSES_PER_PAGE + 1}-${Math.min(currentPage * COURSES_PER_PAGE, filteredCourses.length)}` : 
								'0'
							} of {filteredCourses.length} courses
							{filters.query && ` for "${filters.query}"`}
							{filters.selectedTeachers.length > 0 && 
								` filtered by ${filters.selectedTeachers.length} teacher${filters.selectedTeachers.length > 1 ? 's' : ''}`
							}
							{totalPages > 1 && ` (Page ${currentPage} of ${totalPages})`}
						</p>
						{/* Pagination */}
					{totalPages > 1 && (
						<div className="pagination-container">
							<div className="pagination">
								{/* Previous button */}
								<button 
									className={`pagination-btn ${currentPage === 1 ? 'disabled' : ''}`}
									onClick={() => handlePageChange(currentPage - 1)}
									disabled={currentPage === 1}
								>
									{"<<"}
									{/* Previous ‹ */}
								</button>

								{/* Page numbers */}
								{getPageNumbers().map((pageNum, index) => (
									pageNum === '...' ? (
										<span key={`ellipsis-${index}`} className="pagination-ellipsis">...</span>
									) : (
										<button
											key={pageNum}
											className={`pagination-btn ${currentPage === pageNum ? 'active' : ''}`}
											onClick={() => handlePageChange(pageNum)}
										>
											{pageNum}
										</button>
									)
								))}

								{/* Next button */}
								<button 
									className={`pagination-btn ${currentPage === totalPages ? 'disabled' : ''}`}
									onClick={() => handlePageChange(currentPage + 1)}
									disabled={currentPage === totalPages}
								>
									{">>"}
								</button>
							</div>

							{/* Page info */}
							<div className="pagination-info">
								<span>
									Go to page: 
									<input
										type="number"
										min="1"
										max={totalPages}
										value={currentPage}
										onChange={(e) => {
											const page = parseInt(e.target.value);
											if (page >= 1 && page <= totalPages) {
												handlePageChange(page);
											}
										}}
										className="page-input"
										aria-label="Go to page number"
										title="Enter page number to navigate"
										placeholder="Page"
									/>
								</span>
							</div>
						</div>
					)}
					</div>

					{/* Course list */}
					<ul className="course-list">
						{paginatedCourses.map((course) => (
							<CourseShort key={course.id} course={course} />
						))}
					</ul>

					
					
					{filteredCourses.length === 0 && courses.length > 0 && (
						<div className="no-results">
							<p>No courses match your current filters.</p>
							<p>Try adjusting your search criteria or removing some filters.</p>
						</div>
					)}
					
					{courses.length === 0 && (
						<p className="no-courses">No courses available.</p>
					)}
				</>
			)}
		</div>
	);
}

export default CourseList;
