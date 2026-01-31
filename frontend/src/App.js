import { useState } from 'react';
import './App.css';
import GenerateQuiz from './components/GenerateQuiz';
import HomePage from './components/HomePage';
import QuizHistory from './components/QuizHistory';
import QuizModal from './components/QuizModal';

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [refreshHistory, setRefreshHistory] = useState(false);
  const [error, setError] = useState('');
  const [token, setToken] = useState(localStorage.getItem('token') || null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const handleQuizGenerated = () => {
    setRefreshHistory(!refreshHistory);
    setError('');
  };

  const handleShowDetails = (quiz) => {
    setSelectedQuiz(quiz);
    setShowModal(true);
  };

  const handleLogin = (tok) => {
    setToken(tok);
    setActiveTab('generate');
    setRefreshHistory(!refreshHistory);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedQuiz(null);
  };

  // Show homepage if not logged in
  if (!token) {
    return <HomePage apiBaseUrl={API_BASE_URL} onLogin={handleLogin} />;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>📚 Wiki Quiz Generator</h1>
        <p>Generate interactive quizzes from Wikipedia articles</p>
      </header>

      <div className="tab-navigation">
        <button
          className={`tab-button ${activeTab === 'generate' ? 'active' : ''}`}
          onClick={() => setActiveTab('generate')}
        >
          Generate Quiz
        </button>
        <button
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          History
        </button>
        <div style={{ marginLeft: 'auto' }}>
          <button className="tab-button" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <main className="main-content">
        {activeTab === 'generate' && (
          <GenerateQuiz
            apiBaseUrl={API_BASE_URL}
            onQuizGenerated={handleQuizGenerated}
            onError={setError}
          />
        )}
        {activeTab === 'history' && (
          <QuizHistory
            apiBaseUrl={API_BASE_URL}
            onShowDetails={handleShowDetails}
            refreshTrigger={refreshHistory}
          />
        )}
      </main>

      {showModal && selectedQuiz && (
        <QuizModal quiz={selectedQuiz} onClose={handleCloseModal} />
      )}
    </div>
  );
}

export default App;
