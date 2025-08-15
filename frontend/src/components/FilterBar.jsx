import React from 'react';
import '../styles/FilterBar.css';
	

function FilterBar({ filters, onFilterChange }) {
  const handleFilterChange = (event) => {
	const { name, value } = event.target;
	onFilterChange(name, value);
  };
  
  return (
	<div className="filter-bar">
	{/* <form  onSubmit={HandleSubmit}>
 */}

	
				  {/* <label>
		Filter by Category:
		<select name="category" value={filters.category} onChange={handleFilterChange}>
		  <option value="">All</option>
		  <option value="math">Math</option>
		  <option value="science">Science</option>
		  <option value="history">History</option>
		</select>
	  </label>
	  <label>
		Search:
		<input
		  type="text"
		  name="search"
		  value={filters.search}
		  onChange={handleFilterChange}
		/>
	  </label> */}
	</div>
  );
}

export default FilterBar;