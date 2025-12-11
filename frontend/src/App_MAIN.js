import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Image Caption Generator</h1>
        <p>A professional tool for generating image captions.</p>
      </header>
      <main className="App-main">
        <div className="image-upload-container">
          <div className="image-upload-box">
            <div className="upload-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21.2 15c.7-1.2 1-2.5.7-3.9-.6-2.4-2.4-4.2-4.8-4.8-1.4-.3-2.7 0-3.9.7L12 8l-1.2-1.1c-1.2-.7-2.5-1-3.9-.7-2.4.6-4.2 2.4-4.8 4.8-.3 1.4 0 2.7.7 3.9L4 16.5V19a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2.5l-1.2-1.5z"/>
                <path d="M12 13.5V8.5"/>
                <path d="M14.5 11H9.5"/>
              </svg>
            </div>
            <p>Drag & drop an image here, or click to select a file</p>
            <button className="upload-button">Select File</button>
          </div>
        </div>
        <div className="caption-display-container">
          <h2>Generated Caption</h2>
          <div className="caption-display-box">
            <p className="placeholder">Your generated caption will appear here...</p>
          </div>
          <div className="icon-buttons">
            <button className="icon-button" aria-label="Copy caption">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </button>
            <button className="icon-button" aria-label="Download image with caption">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;