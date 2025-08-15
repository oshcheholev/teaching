import "../styles/CourseShort.css";
import TeacherInfo from "./TeacherInfo";
import { Link } from 'react-router-dom';

function CourseShort({ course }) {
	return (
		<div className="course-short">
			<Link to={`/courses/${course.id}`} className="course-detail-link">
				<h3>{course.title}</h3>
			</Link>
			<div className="course-teacher">
				{/* <span></span> */}
				{course.teacher ? (
					<Link to={`/teacher/${course.teacher.id}`} className="teacher-link">
						{course.teacher.name}
					</Link>
				) : (
					<span>No teacher assigned</span>
				)}
			</div>
			{/* <p>{course.description}</p> */}
			<p>{course.description.substring(0, 300)}...</p>
			{/* <p>Credits: {course.credits}</p> */}
			<p>Semester: {course.semester} </p>
		</div>
	);
}

export default CourseShort;
