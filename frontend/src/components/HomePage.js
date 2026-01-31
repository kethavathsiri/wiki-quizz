import { useState } from 'react';
import './HomePage.css';
import Login from './Login';
import Register from './Register';

function HomePage({ apiBaseUrl, onLogin }) {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [error, setError] = useState('');

  const handleLoginSuccess = (token) => {
    setShowLogin(false);
    setShowRegister(false);
    onLogin(token);
  };

  const handleError = (err) => {
    setError(err);
  };

  if (showLogin) {
    return (
      <div className="home-page">
        <div className="auth-container">
          <Login apiBaseUrl={apiBaseUrl} onLogin={handleLoginSuccess} onError={handleError} />
          <p className="toggle-text">
            Don't have an account? <button className="link-button" onClick={() => { setShowLogin(false); setShowRegister(true); }}>Register here</button>
          </p>
          {error && <div className="error-message">{error}</div>}
        </div>
      </div>
    );
  }

  if (showRegister) {
    return (
      <div className="home-page">
        <div className="auth-container">
          <Register apiBaseUrl={apiBaseUrl} onLogin={handleLoginSuccess} onError={handleError} />
          <p className="toggle-text">
            Already have an account? <button className="link-button" onClick={() => { setShowRegister(false); setShowLogin(true); }}>Login here</button>
          </p>
          {error && <div className="error-message">{error}</div>}
        </div>
      </div>
    );
  }

  return (
    <div className="home-page">
      <div className="home-content">
        <div className="home-header">
          <h1>📚 Wiki Quiz Generator</h1>
          <p className="subtitle">Learn from Wikipedia articles with interactive quizzes</p>
        </div>

        <div className="home-description">
          <p>Welcome to Wiki Quiz Generator! Generate personalized quizzes from any Wikipedia article using AI.</p>
          <div className="features">
            <div className="feature">
              <h3>🎯 Smart Questions</h3>
              <p>AI-generated multiple choice questions from Wikipedia content</p>
            </div>
            <div className="feature">
              <h3>📊 Track Progress</h3>
              <p>Save your quizzes and access your history anytime</p>
            </div>
            <div className="feature">
              <h3>🚀 Instant Results</h3>
              <p>Get instant feedback on your answers</p>
            </div>
          </div>
        </div>

        <div className="home-actions">
          <button className="btn-primary" onClick={() => setShowLogin(true)}>Login</button>
          <button className="btn-secondary" onClick={() => setShowRegister(true)}>Create Account</button>
        </div>

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default HomePage;
