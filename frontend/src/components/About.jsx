
import HeaderMenu from "./HeaderMenu";
import Header from "./Header";
import "../styles/About.css";

function About() {
  return (
    <div className="about-page">
      {/* <HeaderMenu /> */}
      <Header />
      <div className="about">
        <h1>About This Project</h1>
        
        <div className="about-section university-info">
          <h2>Project Overview</h2>
          <p>This page is a recreation of the University of Applied Arts Vienna course management system.</p>
          <p>A comprehensive teaching application for browsing and managing university courses with advanced filtering capabilities.</p>
        </div>

        <div className="about-section">
          <h2>Technology Stack</h2>
          <div className="tech-stack">
            <div className="tech-item">
              <strong>Frontend</strong><br />
              React + Vite
            </div>
            <div className="tech-item">
              <strong>HTTP Client</strong><br />
              Axios
            </div>
            <div className="tech-item">
              <strong>Backend</strong><br />
              Django
            </div>
            <div className="tech-item">
              <strong>API</strong><br />
              Django REST Framework
            </div>
            <div className="tech-item">
              <strong>Database</strong><br />
              PostgreSQL
            </div>
            <div className="tech-item">
              <strong>Deployment</strong><br />
              Docker + Nginx
            </div>
          </div>
        </div>

        <div className="about-section">
          <h2>Features</h2>
          <p>• Multi-filter course search system</p>
          <p>• Gender/diversity course filtering</p>
          <p>• Responsive design with modern UI</p>
          <p>• Department, institute, and program filtering</p>
          <p>• Teacher and course type search capabilities</p>
        </div>

        <div className="about-section">
          <h2>Project Info</h2>
          <p><strong>Version Control:</strong> Git + GitHub</p>
          <p><strong>License:</strong> MIT License</p>
          <p><strong>Development:</strong> Full-stack web application</p>
        </div>

        <p className="made-with-love">Made with ❤️ by Oleksandr Shcheholev</p>

        <div className="contact-section">
          <h2>Get In Touch</h2>
          <p><strong>Email:</strong> <a href="mailto:hukaparya@gmail.com">hukaparya@gmail.com</a></p>
          <p><strong>GitHub:</strong> <a href="https://github.com/oshcheholev" target="_blank" rel="noopener noreferrer">github.com/oshcheholev</a></p>
        </div>
      </div>
    </div>
  );
}

export default About;