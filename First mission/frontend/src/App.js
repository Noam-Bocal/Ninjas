import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = () => {
    axios.get(`http://localhost:3000/search?q=${searchQuery}`)
      .then(response => setSearchResults(response.data))
      .catch(error => {
        console.error(error);
        setSearchResults([]);
      });
  };

  useEffect(() => {
    handleSearch();
  }, []);

  return (
    <div >
      <h1>Search</h1>
      {/* fixing postion of search bar */}
      <div style={{display:"flex", justifyContent:"center", marginBottom:"20px"}}> 
      <input
        type="text"
        value={searchQuery}
        onChange={e => setSearchQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
      </div>
      {/* Table */}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>ID</th>
            <th>x_mitre_platforms</th>
            <th>x_mitre_detection</th>
            <th>phase_name</th>
          </tr>
        </thead>
        <tbody>
          {/* Render search results */}
          {searchResults.map(result => (
            <tr key={result.Id}>
              <td>{result.Name}</td>
              <td style={{ fontSize: '12px' }}>{result.Description}</td>
              <td>{result.Id}</td>
              <td>{result.x_mitre_platforms}</td>
              <td>{result.x_mitre_detection}</td>
              <td>{result.phase_name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
