import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import TeacherInfo from './pages/TeacherInfo'
import CourseDetail from './pages/CourseDetail'
import About from './components/About'
import NotFound from './pages/NotFound'
import Login from './pages/Login'
import Register from './pages/Register'
import AdminLogin from './pages/AdminLogin'
import AdminDashboard from './pages/AdminDashboard'
import AdminCourses from './pages/AdminCourses'
import AdminTeachers from './pages/AdminTeachers'
import AdminCourseTypes from './pages/AdminCourseTypes'
import AdminInstitutes from './pages/AdminInstitutes'
import AdminDepartments from './pages/AdminDepartments'
import AdminStudyPrograms from './pages/AdminStudyPrograms'
import './styles/App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/teacher/:id" element={<TeacherInfo />} />
          <Route path="/courses/:id" element={<CourseDetail />} />
          
          {/* Authentication Routes */}
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          
          {/* Admin Routes */}
          <Route path="/admin/login" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/courses" element={<AdminCourses />} />
          <Route path="/admin/teachers" element={<AdminTeachers />} />
          <Route path="/admin/course-types" element={<AdminCourseTypes />} />
          <Route path="/admin/institutes" element={<AdminInstitutes />} />
          <Route path="/admin/departments" element={<AdminDepartments />} />
          <Route path="/admin/study-programs" element={<AdminStudyPrograms />} />
          
          {/* 404 Route */}
          <Route path="*" element={<NotFound />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App
