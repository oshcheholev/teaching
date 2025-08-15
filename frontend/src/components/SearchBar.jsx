import React, { useState, useEffect, useCallback, useRef } from "react";
import api from "../api";
import "../styles/SearchBar.css";

function SearchBar({ onSearch, onFilterChange }) {
  const [query, setQuery] = useState("");
  const [teachers, setTeachers] = useState([]);
  const [courseTypes, setCourseTypes] = useState([]);
  const [institutes, setInstitutes] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [studyPrograms, setStudyPrograms] = useState([]);
  
  const [selectedTeachers, setSelectedTeachers] = useState([]);
  const [selectedCourseTypes, setSelectedCourseTypes] = useState([]);
  const [selectedInstitutes, setSelectedInstitutes] = useState([]);
  const [selectedDepartments, setSelectedDepartments] = useState([]);
  const [selectedStudyPrograms, setSelectedStudyPrograms] = useState([]);
  const [genderDiversityFilter, setGenderDiversityFilter] = useState(false); // boolean: false = all, true = gender/diversity specific
  
  const [showTeacherDropdown, setShowTeacherDropdown] = useState(false);
  const [showCourseTypeDropdown, setShowCourseTypeDropdown] = useState(false);
  const [showInstituteDropdown, setShowInstituteDropdown] = useState(false);
  const [showDepartmentDropdown, setShowDepartmentDropdown] = useState(false);
  const [showStudyProgramDropdown, setShowStudyProgramDropdown] = useState(false);
  
  const [teacherSearchQuery, setTeacherSearchQuery] = useState("");
  const [courseTypeSearchQuery, setCourseTypeSearchQuery] = useState("");
  const [instituteSearchQuery, setInstituteSearchQuery] = useState("");
  const [departmentSearchQuery, setDepartmentSearchQuery] = useState("");
  const [studyProgramSearchQuery, setStudyProgramSearchQuery] = useState("");
  
  const [loading, setLoading] = useState(false);
  const isInitialMount = useRef(true);

  // Fetch teachers on component mount
  useEffect(() => {
    fetchTeachers();
    fetchCourseTypes();
    fetchInstitutes();
    fetchDepartments();
    fetchStudyPrograms();
  }, []);

  // Notify parent component when filters change (but not on initial mount)
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
      return;
    }
    
    if (onFilterChange) {
      onFilterChange({
        query,
        selectedTeachers,
        selectedCourseTypes,
        selectedInstitutes,
        selectedDepartments,
        selectedStudyPrograms,
        genderDiversityFilter
      });
    }
  }, [query, selectedTeachers, selectedCourseTypes, selectedInstitutes, selectedDepartments, selectedStudyPrograms, genderDiversityFilter, onFilterChange]);

  const fetchTeachers = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/teachers/');
      setTeachers(response.data);
      console.log("Fetched teachers:", response.data);
    } catch (error) {
      console.error("Error fetching teachers:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchCourseTypes = async () => {
    try {
      const response = await api.get('/api/course-types/');
      setCourseTypes(response.data);
    } catch (error) {
      console.error("Error fetching course types:", error);
    }
  };

  const fetchInstitutes = async () => {
    try {
      const response = await api.get('/api/institutes/');
      setInstitutes(response.data);
    } catch (error) {
      console.error("Error fetching institutes:", error);
    }
  };

  const fetchDepartments = async () => {
    try {
      const response = await api.get('/api/departments/');
      setDepartments(response.data);
    } catch (error) {
      console.error("Error fetching departments:", error);
    }
  };

  const fetchStudyPrograms = async () => {
    try {
      const response = await api.get('/api/study-programs/');
      setStudyPrograms(response.data);
    } catch (error) {
      console.error("Error fetching study programs:", error);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    console.log("Search submitted with query:", query); // Debug log
    if (onSearch) {
      onSearch(query);
    }
  };

  const handleTeacherSelect = (teacher) => {
    const isSelected = selectedTeachers.some(t => t.id === teacher.id);
    
    if (isSelected) {
      setSelectedTeachers(selectedTeachers.filter(t => t.id !== teacher.id));
    } else {
      setSelectedTeachers([...selectedTeachers, teacher]);
    }
  };

  const handleCourseTypeSelect = (courseType) => {
    const isSelected = selectedCourseTypes.some(ct => ct.id === courseType.id);
    
    if (isSelected) {
      setSelectedCourseTypes(selectedCourseTypes.filter(ct => ct.id !== courseType.id));
    } else {
      setSelectedCourseTypes([...selectedCourseTypes, courseType]);
    }
  };

  const handleInstituteSelect = (institute) => {
    const isSelected = selectedInstitutes.some(i => i.id === institute.id);
    
    if (isSelected) {
      setSelectedInstitutes(selectedInstitutes.filter(i => i.id !== institute.id));
    } else {
      setSelectedInstitutes([...selectedInstitutes, institute]);
    }
  };

  const handleDepartmentSelect = (department) => {
    const isSelected = selectedDepartments.some(d => d.id === department.id);
    
    if (isSelected) {
      setSelectedDepartments(selectedDepartments.filter(d => d.id !== department.id));
    } else {
      setSelectedDepartments([...selectedDepartments, department]);
    }
  };

  const handleStudyProgramSelect = (studyProgram) => {
    const isSelected = selectedStudyPrograms.some(sp => sp.id === studyProgram.id);
    
    if (isSelected) {
      setSelectedStudyPrograms(selectedStudyPrograms.filter(sp => sp.id !== studyProgram.id));
    } else {
      setSelectedStudyPrograms([...selectedStudyPrograms, studyProgram]);
    }
  };

  const removeTeacher = (teacherId) => {
    setSelectedTeachers(selectedTeachers.filter(t => t.id !== teacherId));
  };

  const removeCourseType = (courseTypeId) => {
    setSelectedCourseTypes(selectedCourseTypes.filter(ct => ct.id !== courseTypeId));
  };

  const removeInstitute = (instituteId) => {
    setSelectedInstitutes(selectedInstitutes.filter(i => i.id !== instituteId));
  };

  const removeDepartment = (departmentId) => {
    setSelectedDepartments(selectedDepartments.filter(d => d.id !== departmentId));
  };

  const removeStudyProgram = (studyProgramId) => {
    setSelectedStudyPrograms(selectedStudyPrograms.filter(sp => sp.id !== studyProgramId));
  };

  const clearAllTeachers = () => {
    setSelectedTeachers([]);
  };

  const clearAllCourseTypes = () => {
    setSelectedCourseTypes([]);
  };

  const clearAllInstitutes = () => {
    setSelectedInstitutes([]);
  };

  const clearAllDepartments = () => {
    setSelectedDepartments([]);
  };

  const clearAllStudyPrograms = () => {
    setSelectedStudyPrograms([]);
  };

  const clearAllFilters = () => {
    setSelectedTeachers([]);
    setSelectedCourseTypes([]);
    setSelectedInstitutes([]);
    setSelectedDepartments([]);
    setSelectedStudyPrograms([]);
    setGenderDiversityFilter(false);
  };

  // Filter data based on search queries
  const filteredTeachers = teachers.filter(teacher =>
    teacher.name.toLowerCase().includes(teacherSearchQuery.toLowerCase())
  );

  const filteredCourseTypes = courseTypes.filter(courseType =>
    courseType.name.toLowerCase().includes(courseTypeSearchQuery.toLowerCase())
  );

  const filteredInstitutes = institutes.filter(institute =>
    institute.name.toLowerCase().includes(instituteSearchQuery.toLowerCase())
  );

  const filteredDepartments = departments.filter(department =>
    department.name.toLowerCase().includes(departmentSearchQuery.toLowerCase())
  );

  const filteredStudyPrograms = studyPrograms.filter(studyProgram =>
    studyProgram.name.toLowerCase().includes(studyProgramSearchQuery.toLowerCase())
  );

  // Helper function to render multi-select filter
  const renderMultiSelectFilter = (
    label,
    selectedItems,
    items,
    searchQuery,
    setSearchQuery,
    showDropdown,
    setShowDropdown,
    handleSelect,
    removeItem,
    clearAll,
    loading = false
  ) => (
    <div className="filter-section">
      <div className="selected-items-container">
        <label className="filter-label">{label}:</label>
        
        {selectedItems.length > 0 && (
          <div className="selected-items">
            {selectedItems.map(item => (
              <span key={item.id} className="item-tag">
                {item.name}
                <button
                  type="button"
                  className="remove-item"
                  onClick={() => removeItem(item.id)}
                  aria-label={`Remove ${item.name}`}
                >
                  ×
                </button>
              </span>
            ))}
            <button
              type="button"
              className="clear-all-items"
              onClick={clearAll}
            >
              Clear All
            </button>
          </div>
        )}
      </div>

      <div className="filter-search-container">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onFocus={() => setShowDropdown(true)}
          placeholder={selectedItems.length > 0 ? `Add more ${label.toLowerCase()}...` : `All ${label.toLowerCase()}...`}
          className="filter-search-input"
        />
        
        {showDropdown && (
          <div className="filter-dropdown">
            {loading ? (
              <div className="dropdown-item loading">Loading {label.toLowerCase()}...</div>
            ) : items.length > 0 ? (
              items.map(item => {
                const isSelected = selectedItems.some(si => si.id === item.id);
                return (
                  <div
                    key={item.id}
                    className={`dropdown-item ${isSelected ? 'selected' : ''}`}
                    onClick={() => handleSelect(item)}
                  >
                    <span className="item-name">{item.name}</span>
                    {isSelected && <span className="checkmark">✓</span>}
                  </div>
                );
              })
            ) : (
              <div className="dropdown-item no-results">
                {searchQuery ? `No ${label.toLowerCase()} found` : `No ${label.toLowerCase()} available`}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="search-bar-container">
      <form onSubmit={handleSearch} className="search-bar">
        {/* Course Search Input */}
        <div className="search-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search courses..."
            className="course-search-input"
          />
          <button type="submit" className="search-button">Search</button>
        </div>

        {/* Filters Section */}
        <div className="filters-container">
          <div className="filters-row">
            {/* Teacher Filter */}
            {renderMultiSelectFilter(
              "Teachers",
              selectedTeachers,
              filteredTeachers,
              teacherSearchQuery,
              setTeacherSearchQuery,
              showTeacherDropdown,
              setShowTeacherDropdown,
              handleTeacherSelect,
              removeTeacher,
              clearAllTeachers,
              loading
            )}

            {/* Course Type Filter */}
            {renderMultiSelectFilter(
              "Course Types",
              selectedCourseTypes,
              filteredCourseTypes,
              courseTypeSearchQuery,
              setCourseTypeSearchQuery,
              showCourseTypeDropdown,
              setShowCourseTypeDropdown,
              handleCourseTypeSelect,
              removeCourseType,
              clearAllCourseTypes
            )}

            {/* Institute Filter */}
            {renderMultiSelectFilter(
              "Institutes",
              selectedInstitutes,
              filteredInstitutes,
              instituteSearchQuery,
              setInstituteSearchQuery,
              showInstituteDropdown,
              setShowInstituteDropdown,
              handleInstituteSelect,
              removeInstitute,
              clearAllInstitutes
            )}
          </div>

          <div className="filters-row">
            {/* Department Filter */}
            {renderMultiSelectFilter(
              "Departments",
              selectedDepartments,
              filteredDepartments,
              departmentSearchQuery,
              setDepartmentSearchQuery,
              showDepartmentDropdown,
              setShowDepartmentDropdown,
              handleDepartmentSelect,
              removeDepartment,
              clearAllDepartments
            )}

            {/* Study Program Filter */}
            {renderMultiSelectFilter(
              "Study Programs",
              selectedStudyPrograms,
              filteredStudyPrograms,
              studyProgramSearchQuery,
              setStudyProgramSearchQuery,
              showStudyProgramDropdown,
              setShowStudyProgramDropdown,
              handleStudyProgramSelect,
              removeStudyProgram,
              clearAllStudyPrograms
            )}

            {/* Gender/Diversity Filter */}
            <div className="filter-section">
              <label className="filter-label">Gender/Diversity:</label>
              <div className="checkbox-container">
                <label className="checkbox-option">
                  <input
                    type="checkbox"
                    checked={genderDiversityFilter}
                    onChange={(e) => setGenderDiversityFilter(e.target.checked)}
                  />
                  <span className="checkbox-label">Show only Gender/Diversity specific courses</span>
                </label>
              </div>
            </div>
          </div>

          {/* Clear All Filters Button */}
          <div className="clear-all-container">
            <button
              type="button"
              className="clear-all-filters"
              onClick={clearAllFilters}
            >
              Clear All Filters
            </button>
          </div>
        </div>
      </form>

      {/* Overlays to close dropdowns when clicking outside */}
      {(showTeacherDropdown || showCourseTypeDropdown || showInstituteDropdown || 
        showDepartmentDropdown || showStudyProgramDropdown) && (
        <div 
          className="dropdown-overlay"
          onClick={() => {
            setShowTeacherDropdown(false);
            setShowCourseTypeDropdown(false);
            setShowInstituteDropdown(false);
            setShowDepartmentDropdown(false);
            setShowStudyProgramDropdown(false);
          }}
        />
      )}
    </div>
  );
}
export default SearchBar;