import React from "react";
import SearchBar from "../components/SearchBar";

function HomeTest() {
  return (
    <div style={{ padding: "20px", backgroundColor: "lightgray", minHeight: "100vh" }}>
      <h1>Home Test Page</h1>
      <div style={{ margin: "20px 0", padding: "20px", backgroundColor: "white" }}>
        <h2>SearchBar Test:</h2>
        <SearchBar onSearch={(query) => console.log("Searching for:", query)} />
      </div>
    </div>
  );
}

export default HomeTest;
