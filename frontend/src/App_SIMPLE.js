import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app" style={{background: '#fafafa', minHeight: '100vh'}}>
      <header className="header" style={{background: 'white', padding: '20px', borderBottom: '1px solid #e0e0e0'}}>
        <div style={{maxWidth: '1400px', margin: '0 auto', display: 'flex', justifyContent: 'space-between'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '12px'}}>
            <div style={{width: '40px', height: '40px', background: '#6366f1', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '20px'}}>
              ✨
            </div>
            <div>
              <h1 style={{fontSize: '20px', fontWeight: '700', margin: 0}}>CaptionAI</h1>
              <span style={{fontSize: '12px', color: '#999'}}>PROFESSIONAL EDITION</span>
            </div>
          </div>
          <button style={{padding: '8px 16px', border: '1px solid #e0e0e0', borderRadius: '8px', background: 'white'}}>
            ℹ️ About
          </button>
        </div>
      </header>

      <main style={{maxWidth: '1400px', margin: '32px auto', padding: '0 32px'}}>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px'}}>
          {/* Left Panel */}
          <div style={{background: 'white', border: '1px solid #e0e0e0', borderRadius: '12px', overflow: 'hidden'}}>
            <div style={{padding: '20px 24px', borderBottom: '1px solid #e0e0e0', background: '#f5f5f5', display: 'flex', justifyContent: 'space-between'}}>
              <h2 style={{fontSize: '16px', fontWeight: '600', margin: 0}}>Image Upload</h2>
              <span style={{padding: '4px 12px', background: '#eef2ff', color: '#6366f1', borderRadius: '999px', fontSize: '12px', fontWeight: '600'}}>STEP 1</span>
            </div>
            <div style={{padding: '24px'}}>
              <div style={{border: '2px dashed #e0e0e0', borderRadius: '12px', padding: '48px', textAlign: 'center', background: '#f5f5f5'}}>
                <div style={{width: '80px', height: '80px', margin: '0 auto 20px', background: 'white', border: '2px solid #e0e0e0', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '36px'}}>
                  📤
                </div>
                <h3 style={{fontSize: '18px', fontWeight: '600', marginBottom: '8px'}}>Drop your image here</h3>
                <p style={{color: '#666', marginBottom: '20px'}}>or click to browse files</p>
                <div style={{display: 'flex', gap: '8px', justifyContent: 'center', marginBottom: '12px'}}>
                  <span style={{padding: '4px 12px', background: 'white', border: '1px solid #e0e0e0', borderRadius: '6px', fontSize: '12px', fontWeight: '600'}}>PNG</span>
                  <span style={{padding: '4px 12px', background: 'white', border: '1px solid #e0e0e0', borderRadius: '6px', fontSize: '12px', fontWeight: '600'}}>JPG</span>
                  <span style={{padding: '4px 12px', background: 'white', border: '1px solid #e0e0e0', borderRadius: '6px', fontSize: '12px', fontWeight: '600'}}>JPEG</span>
                </div>
                <p style={{fontSize: '12px', color: '#999'}}>Maximum file size: 10MB</p>
              </div>
            </div>
          </div>

          {/* Right Panel */}
          <div style={{background: 'white', border: '1px solid #e0e0e0', borderRadius: '12px', overflow: 'hidden'}}>
            <div style={{padding: '20px 24px', borderBottom: '1px solid #e0e0e0', background: '#f5f5f5', display: 'flex', justifyContent: 'space-between'}}>
              <h2 style={{fontSize: '16px', fontWeight: '600', margin: 0}}>Generated Caption</h2>
              <span style={{padding: '4px 12px', background: '#eef2ff', color: '#6366f1', borderRadius: '999px', fontSize: '12px', fontWeight: '600'}}>STEP 2</span>
            </div>
            <div style={{padding: '24px', textAlign: 'center'}}>
              <div style={{width: '80px', height: '80px', margin: '0 auto 20px', background: '#f5f5f5', border: '2px solid #e0e0e0', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '48px'}}>
                ✨
              </div>
              <h3 style={{fontSize: '18px', fontWeight: '600', marginBottom: '8px'}}>No image uploaded yet</h3>
              <p style={{color: '#666', fontSize: '14px'}}>Upload an image to generate an AI-powered caption</p>
            </div>
          </div>
        </div>

        {/* Feature Strip */}
        <div style={{marginTop: '32px', padding: '32px', background: 'white', border: '1px solid #e0e0e0', borderRadius: '12px', display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '24px'}}>
          <div style={{display: 'flex', alignItems: 'center', gap: '16px'}}>
            <div style={{width: '48px', height: '48px', background: '#eef2ff', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px'}}>⚡</div>
            <div>
              <h4 style={{fontSize: '14px', fontWeight: '600', marginBottom: '4px'}}>Lightning Fast</h4>
              <p style={{fontSize: '12px', color: '#666', margin: 0}}>Instant AI analysis</p>
            </div>
          </div>
          <div style={{display: 'flex', alignItems: 'center', gap: '16px'}}>
            <div style={{width: '48px', height: '48px', background: '#eef2ff', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px'}}>✨</div>
            <div>
              <h4 style={{fontSize: '14px', fontWeight: '600', marginBottom: '4px'}}>AI Powered</h4>
              <p style={{fontSize: '12px', color: '#666', margin: 0}}>Advanced deep learning</p>
            </div>
          </div>
          <div style={{display: 'flex', alignItems: 'center', gap: '16px'}}>
            <div style={{width: '48px', height: '48px', background: '#eef2ff', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px'}}>🖼️</div>
            <div>
              <h4 style={{fontSize: '14px', fontWeight: '600', marginBottom: '4px'}}>High Accuracy</h4>
              <p style={{fontSize: '12px', color: '#666', margin: 0}}>Precise descriptions</p>
            </div>
          </div>
        </div>
      </main>

      <footer style={{textAlign: 'center', padding: '24px', borderTop: '1px solid #e0e0e0', background: 'white', color: '#999', fontSize: '14px'}}>
        © 2024 CaptionAI • Powered by Advanced AI Technology
      </footer>

      <div style={{position: 'fixed', bottom: '20px', right: '20px', background: '#10b981', color: 'white', padding: '12px 20px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.15)', fontWeight: '600'}}>
        ✅ UI IS WORKING!
      </div>
    </div>
  );
}

export default App;
