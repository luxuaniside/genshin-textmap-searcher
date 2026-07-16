import { useState } from "react";
import "./index.css";
import columbina from "./assets/columbina.png";

const API_URL = "http://localhost:tre";

const RESULTS_PER_PAGE = 10;

function HighlightText({ text, highlight }) {
  if (!highlight.trim()) return text;

  const parts = text.split(
    new RegExp(`(${highlight})`, "gi")
  );

  return (
    <>
      {parts.map((part, index) =>
        part.toLowerCase() === highlight.toLowerCase() ? (
          <mark key={index}>{part}</mark>
        ) : (
          part
        )
      )}
    </>
  );
}

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  const [page, setPage] = useState(1);


  async function search(e) {
    e.preventDefault();

    if (!query.trim()) return;

    setLoading(true);
    setSearched(true);
    setPage(1);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/search/${encodeURIComponent(query)}`
      );

      const data = await response.json();

      // API returned an error or unexpected format
      if (!response.ok || !Array.isArray(data)) {
        throw new Error("Search failed.");
      }

      setResults(data);

    } catch (error) {
      console.error("Search failed:", error);

      setResults([]);
      setError("Search failed. Please try again.");

    } finally {
      setLoading(false);
    }
  }


  const totalPages = Math.ceil(
    results.length / RESULTS_PER_PAGE
  );

  const currentResults = results.slice(
    (page - 1) * RESULTS_PER_PAGE,
    page * RESULTS_PER_PAGE
  );


  return (
    <>
      <header>

        <img
          src={columbina}
          alt="Columbina"
          width={200}
          height={200}
          style={{ maxWidth: "100%" }}
        />


        <h1 className="luxuani-title">
          Luxuani's{" "}
          <span className="luxuani-subtitle">
            Textmap Searcher
          </span>
        </h1>


        <form onSubmit={search}>

          <input
            type="text"
            placeholder="Search..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />


          <button
            className="search-button"
            type="submit"
          >
            ⌕
          </button>

        </form>



        <div className="results-container">


          {loading && (
            <p className="loading-text">
              Loading data...
            </p>
          )}


          {!loading && error && (
            <p className="error-message">
              {error}
            </p>
          )}



          {!loading && searched && !error && results.length === 0 && (
            <p className="nothing-found">
              Nothing found
            </p>
          )}



          {currentResults.map((result) => (

            <div
              key={result.id}
              className="textmap-container"
            >

              <div className="tag-row">

                <span className="tag id-tag">
                  {result.id}
                </span>


                <span className="tag source-tag">
                  {result.source}
                </span>

              </div>



              <p className="textmap-text-main">

                <HighlightText
                  text={result.en}
                  highlight={query}
                />

              </p>



              <p className="textmap-text-chs">

                {result.chs}

              </p>


            </div>

          ))}



          {totalPages > 1 && (

            <div className="pagination">

              <button
                disabled={page === 1}
                onClick={() => setPage(page - 1)}
              >
                ←
              </button>


              <span>
                {page} / {totalPages}
              </span>


              <button
                disabled={page === totalPages}
                onClick={() => setPage(page + 1)}
              >
                →
              </button>

            </div>

          )}


        </div>

      </header>



      <footer>

        <h3>
          Live data from{" "}
          <a
            className="live-data-credits"
            href="https://gitlab.com/Dimbreath/animegamedata2"
            target="_blank"
            rel="noreferrer"
          >
            Dimbreath
          </a>
        </h3>

      </footer>

    </>
  );
}

export default App;