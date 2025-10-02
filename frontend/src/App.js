import React, { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/search?item=${query}`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      console.log(data); // see if items come back
      setResults(data);
    } catch (error) {
      console.error("Fetch error:", error);
    }
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