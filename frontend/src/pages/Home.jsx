import React, { useState, useCallback } from "react";
import Header from "../components/Header";
import CourseList from "../components/CourseList";
import SearchBar from "../components/SearchBar";
import "../styles/Home.css";

function Home() {
  const [filters, setFilters] = useState({
    query: "",
    selectedTeachers: []
  });

  const handleSearch = useCallback((query) => {
    setFilters(prev => ({ ...prev, query }));
  }, []);

  const handleFilterChange = useCallback((newFilters) => {
    setFilters(newFilters);
  }, []);

  return (
    <div className="home-page">
      <div className="header-container">
        <Header />
      </div>
      <div className="home-content">
      <div className="search-container">
        <SearchBar 
          onSearch={handleSearch}
          onFilterChange={handleFilterChange}
        />
      </div>
        <CourseList filters={filters} />
      </div>
    </div>
  );
}

export default Home;
