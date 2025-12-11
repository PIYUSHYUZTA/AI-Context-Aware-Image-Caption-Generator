import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, Image as ImageIcon, Sparkles, Download, X, Loader2, Zap, Copy, Check, Info } from 'lucide-react';
import axios from 'axios';
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
      const response = await axios.post('http://localhost:8000/api/v1/caption', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setCaption(response.data.caption);
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
      {/* Subtle Background Grid */}
      <div className="background-grid"></div>
      <div className="background-gradient"></div>

      {/* Professional Header */}
      <motion.header 
        className="header"
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon-wrapper">
              <Sparkles className="logo-icon" />
            </div>
            <div className="logo-text">
              <h1 className="logo-title">CaptionAI</h1>
              <span className="logo-subtitle">Professional Edition</span>
            </div>
          </div>
          <div className="header-actions">
            <button className="header-btn">
              <Info size={18} />
              <span>About</span>
            </button>
          </div>
        </div>
      </motion.header>

      {/* Main Workspace */}
      <main className="workspace">
        <div className="workspace-container">
          
          {/* Left Panel - Upload Area */}
          <motion.div 
            className="panel panel-upload"
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
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
                      <Upload className="upload-icon" />
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
                <motion.div 
                  className="image-preview-container"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                >
                  <div className="image-preview-wrapper">
                    <img src={previewUrl} alt="Preview" className="image-preview" />
                    <motion.button
                      className="btn-remove"
                      onClick={clearImage}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      <X size={16} />
                    </motion.button>
                  </div>
                  <div className="image-info">
                    <ImageIcon size={16} />
                    <span>Image loaded successfully</span>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>

          {/* Right Panel - Caption Output */}
          <motion.div 
            className="panel panel-output"
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="panel-header">
              <h2 className="panel-title">Generated Caption</h2>
              <span className="panel-badge">Step 2</span>
            </div>

            <div className="panel-content">
              {!previewUrl ? (
                <div className="empty-state">
                  <div className="empty-icon">
                    <Sparkles size={48} />
                  </div>
                  <h3 className="empty-title">No image uploaded yet</h3>
                  <p className="empty-description">
                    Upload an image to generate an AI-powered caption
                  </p>
                </div>
              ) : (
                <>
                  <motion.button
                    className="btn-generate"
                    onClick={generateCaption}
                    disabled={loading}
                    whileHover={{ scale: loading ? 1 : 1.02 }}
                    whileTap={{ scale: loading ? 1 : 0.98 }}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="btn-icon spinning" />
                        <span>Analyzing image...</span>
                      </>
                    ) : (
                      <>
                        <Zap className="btn-icon" />
                        <span>Generate Caption</span>
                      </>
                    )}
                  </motion.button>

                  <AnimatePresence>
                    {caption && (
                      <motion.div
                        className="caption-output"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                      >
                        <div className="caption-label">
                          <Sparkles size={16} />
                          <span>AI Generated Caption</span>
                        </div>
                        <div className="caption-content">
                          <p className="caption-text">{caption}</p>
                        </div>
                        <motion.button
                          className="btn-copy"
                          onClick={copyCaption}
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                        >
                          {copied ? (
                            <>
                              <Check className="btn-icon" />
                              <span>Copied!</span>
                            </>
                          ) : (
                            <>
                              <Copy className="btn-icon" />
                              <span>Copy to Clipboard</span>
                            </>
                          )}
                        </motion.button>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {error && (
                    <motion.div
                      className="error-alert"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                    >
                      <X size={16} />
                      <span>{error}</span>
                    </motion.div>
                  )}
                </>
              )}
            </div>
          </motion.div>

        </div>

        {/* Bottom Feature Cards */}
        <motion.div 
          className="feature-strip"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="feature-item">
            <div className="feature-icon-box">
              <Zap size={20} />
            </div>
            <div className="feature-text">
              <h4>Lightning Fast</h4>
              <p>Instant AI analysis</p>
            </div>
          </div>
          <div className="feature-item">
            <div className="feature-icon-box">
              <Sparkles size={20} />
            </div>
            <div className="feature-text">
              <h4>AI Powered</h4>
              <p>Advanced deep learning</p>
            </div>
          </div>
          <div className="feature-item">
            <div className="feature-icon-box">
              <ImageIcon size={20} />
            </div>
            <div className="feature-text">
              <h4>High Accuracy</h4>
              <p>Precise descriptions</p>
            </div>
          </div>
        </motion.div>
      </main>

      {/* Minimal Footer */}
      <footer className="footer">
        <p>© 2024 CaptionAI • Powered by Advanced AI Technology</p>
      </footer>
    </div>
  );
}

export default App;
