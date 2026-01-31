import axios from 'axios';
import { useEffect, useRef, useState } from 'react';
import './GenerateQuiz.css';
import QuizDisplay from './QuizDisplay';

function GenerateQuiz({ apiBaseUrl, onQuizGenerated, onError }) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [quiz, setQuiz] = useState(null);
  const [success, setSuccess] = useState('');
  const quizDisplayRef = useRef(null);

  // Auto-scroll to quiz when it's generated
  useEffect(() => {
    if (quiz && quizDisplayRef.current) {
      setTimeout(() => {
        quizDisplayRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 300);
    }
  }, [quiz]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!url.trim()) {
      onError('Please enter a Wikipedia URL');
      return;
    }

    // Clear old quiz data before fetching new one
    setQuiz(null);
    setLoading(true);
    setSuccess('');
    onError('');

    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios.post(`${apiBaseUrl}/api/quiz/generate`, {
        url: url.trim()
      }, { headers });

      setQuiz(response.data);
      setSuccess('✓ Quiz generated successfully!');
      onQuizGenerated();
      setUrl('');
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Error generating quiz';
      onError(errorMsg);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generate-quiz-container">
      <div className="form-section">
        <h2>Enter Wikipedia Article URL</h2>
        
        <form onSubmit={handleSubmit} className="quiz-form">
          <div className="input-group">
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
              disabled={loading}
              className="url-input"
            />
            <button
              type="submit"
              disabled={loading}
              className="submit-button"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  <span>Generating...</span>
                </>
              ) : (
                'Generate Quiz'
              )}
            </button>
          </div>

          <div className="example-urls">
            <p className="hint">Example URLs:</p>
            <ul>
              <li>https://en.wikipedia.org/wiki/Alan_Turing</li>
              <li>https://en.wikipedia.org/wiki/Python_(programming_language)</li>
              <li>https://en.wikipedia.org/wiki/Climate_change</li>
            </ul>
          </div>
        </form>

        {success && <div className="success-message">{success}</div>}
      </div>

      {loading && (
        <div className="loading-container">
          <div className="progress-animation">
            <div className="progress-circle"></div>
            <p>Scraping article and generating quiz...</p>
          </div>
        </div>
      )}

      {quiz && <div ref={quizDisplayRef}><QuizDisplay quiz={quiz} /></div>}
    </div>
  );
}

export default GenerateQuiz;
