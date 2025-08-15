import "../styles/CourseShort.css";
import TeacherInfo from "./TeacherInfo";
import React from "react";

function CourseShortWithModal({ course }) {
	const [showTeacherModal, setShowTeacherModal] = React.useState(false);

	return (
		<div className="course-short">
			<h3>{course.title}</h3>
			<a href={`/courses/${course.id}`}>View Details</a>
			
			<div className="course-teacher">
				<span>Teacher: </span>
				<button 
					onClick={() => setShowTeacherModal(true)}
					className="teacher-name-btn"
				>
					{course.teacher?.name || 'No teacher assigned'}
				</button>
			</div>
			
			{/* Modal */}
			{showTeacherModal && (
				<div className="modal-overlay" onClick={() => setShowTeacherModal(false)}>
					<div className="modal-content" onClick={(e) => e.stopPropagation()}>
						<div className="modal-header">
							<h3>Teacher Information</h3>
							<button 
								onClick={() => setShowTeacherModal(false)}
								className="modal-close"
							>
								×
							</button>
						</div>
						<TeacherInfo teacher={course.teacher} compact={false} />
					</div>
				</div>
			)}
			
			<p>{course.description.substring(0, 100)}...</p>
			<p>Credits: {course.credits}</p>
			<p>Semester: {course.semester} {course.year}</p>
		</div>
	);
}

export default CourseShortWithModal;
