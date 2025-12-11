import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [caption, setCaption] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);
  const fileInputRef = useRef(null);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setCaption('');
      setError('');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setCaption('');
      setError('');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const generateCaption = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await fetch('http://localhost:8000/api/v1/caption', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate caption');
      }
      
      const data = await response.json();
      setCaption(data.caption);
    } catch (err) {
      setError('Failed to generate caption. Make sure the backend is running on port 8000.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setCaption('');
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const copyCaption = () => {
    navigator.clipboard.writeText(caption);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="app">
      <div className="background-grid"></div>
      <div className="background-gradient"></div>

      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon-wrapper">
              <span className="logo-icon">✨</span>
            </div>
            <div className="logo-text">
              <h1 className="logo-title">CaptionAI</h1>
              <span className="logo-subtitle">Professional Edition</span>
            </div>
          </div>
          <div className="header-actions">
            <button className="header-btn">
              <span>ℹ️</span>
              <span>About</span>
            </button>
          </div>
        </div>
      </header>

      <main className="workspace">
        <div className="workspace-container">
          
          <div className="panel panel-upload">
            <div className="panel-header">
              <h2 className="panel-title">Image Upload</h2>
              <span className="panel-badge">Step 1</span>
            </div>

            <div className="panel-content">
              {!previewUrl ? (
                <div 
                  className="upload-zone"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}
                >
                  <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleImageSelect}
                    accept="image/*"
                    className="file-input"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="upload-label">
                    <div className="upload-icon-container">
                      <span className="upload-icon">📤</span>
                    </div>
                    <h3 className="upload-title">Drop your image here</h3>
                    <p className="upload-subtitle">or click to browse files</p>
                    <div className="upload-formats">
                      <span className="format-tag">PNG</span>
                      <span className="format-tag">JPG</span>
                      <span className="format-tag">JPEG</span>
                    </div>
                    <p className="upload-limit">Maximum file size: 10MB</p>
                  </label>
                </div>
              ) : (
                <div className="image-preview-container">
                  <div className="image-preview-wrapper">
                    <img src={previewUrl} alt="Preview" className="image-preview" />
                    <button className="btn-remove" onClick={clearImage}>✕</button>
                  </div>
                  <div className="image-info">
                    <span>🖼️</span>
                    <span>Image loaded successfully</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="panel panel-output">
            <div className="panel-header">
              <h2 className="panel-title">Generated Caption</h2>
              <span className="panel-badge">Step 2</span>
            </div>

            <div className="panel-content">
              {!previewUrl ? (
                <div className="empty-state">
                  <div className="empty-icon">
                    <span>✨</span>
                  </div>
                  <h3 className="empty-title">No image uploaded yet</h3>
                  <p className="empty-description">
                    Upload an image to generate an AI-powered caption
                  </p>
                </div>
              ) : (
                <>
                  <button
                    className="btn-generate"
                    onClick={generateCaption}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="btn-icon spinning">⏳</span>
                        <span>Analyzing image...</span>
                      </>
                    ) : (
                      <>
                        <span className="btn-icon">⚡</span>
                        <span>Generate Caption</span>
                      </>
                    )}
                  </button>

                  {caption && (
                    <div className="caption-output">
                      <div className="caption-label">
                        <span>✨</span>
                        <span>AI Generated Caption</span>
                      </div>
                      <div className="caption-content">
                        <p className="caption-text">{caption}</p>
                      </div>
                      <button className="btn-copy" onClick={copyCaption}>
                        {copied ? (
                          <>
                            <span className="btn-icon">✅</span>
                            <span>Copied!</span>
                          </>
                        ) : (
                          <>
                            <span className="btn-icon">📋</span>
                            <span>Copy to Clipboard</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}

                  {error && (
                    <div className="error-alert">
                      <span>❌</span>
                      <span>{error}</span>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>

        </div>

        <div className="feature-strip">
          <div className="feature-item">
            <div className="feature-icon-box">
              <span>⚡</span>
            </div>
            <div className="feature-text">
              <h4>Lightning Fast</h4>
              <p>Instant AI analysis</p>
            </div>
          </div>
          <div className="feature-item">
            <div className="feature-icon-box">
              <span>✨</span>
            </div>
            <div className="feature-text">
              <h4>AI Powered</h4>
              <p>Advanced deep learning</p>
            </div>
          </div>
          <div className="feature-item">
            <div className="feature-icon-box">
              <span>🖼️</span>
            </div>
            <div className="feature-text">
              <h4>High Accuracy</h4>
              <p>Precise descriptions</p>
            </div>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>© 2024 CaptionAI • Powered by Advanced AI Technology</p>
      </footer>
    </div>
  );
}

export default App;
