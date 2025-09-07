import React, { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const res = await fetch(`http://localhost:5000/search?item=${query}`);
    const data = await res.json();
    setResults(data);
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Grocery Search</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter grocery item"
      />
      <button onClick={handleSearch}>Search</button>

      <ul>
        {results.map((item, idx) => (
          <li key={idx}>
            {item.name} — ${item.price} at {item.merchant}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
