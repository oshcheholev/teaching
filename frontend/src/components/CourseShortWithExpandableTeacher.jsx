import "../styles/CourseShort.css";
import TeacherInfo from "./TeacherInfo";
import React from "react";

function CourseShortWithExpandableTeacher({ course }) {
	const [showTeacherDetails, setShowTeacherDetails] = React.useState(false);

	return (
		<div className="course-short">
			<h3>{course.title}</h3>
			<a href={`/courses/${course.id}`}>View Details</a>
			
			<div className="course-teacher">
				<span>Teacher: </span>
				<TeacherInfo teacher={course.teacher} compact={true} />
				<button 
					onClick={() => setShowTeacherDetails(!showTeacherDetails)}
					className="teacher-toggle-btn"
				>
					{showTeacherDetails ? 'Hide' : 'Show'} Details
				</button>
			</div>
			
			{showTeacherDetails && (
				<div className="teacher-details-expanded">
					<TeacherInfo teacher={course.teacher} compact={false} />
				</div>
			)}
			
			<p>{course.description.substring(0, 100)}...</p>
			<p>Credits: {course.credits}</p>
			<p>Semester: {course.semester} {course.year}</p>
		</div>
	);
}

export default CourseShortWithExpandableTeacher;
