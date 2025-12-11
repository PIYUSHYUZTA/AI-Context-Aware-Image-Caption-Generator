import React from 'react';

function App() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        background: 'white',
        padding: '60px',
        borderRadius: '20px',
        boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
        textAlign: 'center',
        maxWidth: '600px'
      }}>
        <h1 style={{
          fontSize: '48px',
          color: '#667eea',
          marginBottom: '20px'
        }}>
          ✅ REACT IS WORKING!
        </h1>
        <p style={{
          fontSize: '24px',
          color: '#333',
          marginBottom: '30px'
        }}>
          If you can see this, React is rendering correctly.
        </p>
        <div style={{
          background: '#f0f0f0',
          padding: '20px',
          borderRadius: '10px',
          marginTop: '20px'
        }}>
          <p style={{fontSize: '16px', color: '#666', margin: '10px 0'}}>
            ✅ JavaScript is working
          </p>
          <p style={{fontSize: '16px', color: '#666', margin: '10px 0'}}>
            ✅ React is rendering
          </p>
          <p style={{fontSize: '16px', color: '#666', margin: '10px 0'}}>
            ✅ Styles are applying
          </p>
        </div>
        <button 
          onClick={() => alert('Button clicked! Everything works!')}
          style={{
            marginTop: '30px',
            padding: '15px 40px',
            fontSize: '18px',
            background: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '10px',
            cursor: 'pointer',
            fontWeight: 'bold'
          }}
        >
          Click Me to Test
        </button>
      </div>
    </div>
  );
}

export default App;
