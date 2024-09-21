// src/components/Pexels.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Pexels.css'; // Import the CSS file

const PexelsVideos = () => {
  const [videos, setVideos] = useState([]);
  const [query, setQuery] = useState('nature'); // Default search term
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchVideos = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('https://localhost:443/app/video', {
        params: {
          query: query,
          per_page: 10, // You can adjust this as needed
        },
      });
      setVideos(response.data.videos || []); // Adjust based on the response structure
    } catch (error) {
      console.error('Error fetching videos:', error);
      setError('Failed to fetch videos');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVideos();
  }, []);

  const handleSearch = (event) => {
    event.preventDefault();
    fetchVideos();
  };

  return (
    <div className="container">
      <h1>Videos Generator</h1>
      <div className="search-container">
        <form onSubmit={handleSearch}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for videos..."
          />
          <button type="submit">Search</button>
        </form>
      </div>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>{error}</p>
      ) : (
        <div className="video-container">
          {videos.map((video) => (
            <div className="video-item" key={video.id}>
              <video controls>
                <source src={video.video_files[0].link} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PexelsVideos;
