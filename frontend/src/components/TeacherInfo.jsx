import React from "react";
import "../styles/TeacherInfo.css";

function TeacherInfo({ teacher, compact = false }) {
  if (!teacher) {
    return <span className="teacher-info no-teacher">No teacher assigned</span>;
  }

  if (compact) {
    return (
      <span className="teacher-info compact">
        <a href={`/teacher/${teacher.id}`} className="teacher-link">
          {teacher.name}
        </a>
      </span>
    );
  }

  return (
    <div className="teacher-info full">
      <div className="teacher-header">
        <h4 className="teacher-name">
          <a href={`/teacher/${teacher.id}`} className="teacher-link">
            {teacher.name}
          </a>
        </h4>
        {teacher.subject && (
          <span className="teacher-subject">{teacher.subject}</span>
        )}
      </div>
      {teacher.email && (
        <a href={`mailto:${teacher.email}`} className="teacher-email">
          {teacher.email}
        </a>
      )}
    </div>
  );
}

export default TeacherInfo;
