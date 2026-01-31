import axios from 'axios';
import { useEffect, useState } from 'react';
import './QuizHistory.css';

function QuizHistory({ apiBaseUrl, onShowDetails, refreshTrigger }) {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchQuizzes();
  }, [refreshTrigger, apiBaseUrl]);

  const fetchQuizzes = async () => {
    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios.get(`${apiBaseUrl}/api/history`, { headers });
      setQuizzes(response.data);
    } catch (err) {
      setError('Failed to load quiz history');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (quizId) => {
    if (!window.confirm('Are you sure you want to delete this quiz?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      await axios.delete(`${apiBaseUrl}/api/quiz/${quizId}`, { headers });
      setQuizzes(quizzes.filter(q => q.id !== quizId));
    } catch (err) {
      setError('Failed to delete quiz');
      console.error('Error:', err);
    }
  };

  const fetchQuizDetails = async (quizId) => {
    try {
      const token = localStorage.getItem('token');
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios.get(`${apiBaseUrl}/api/quiz/${quizId}`, { headers });
      onShowDetails(response.data);
    } catch (err) {
      setError('Failed to load quiz details');
      console.error('Error:', err);
    }
  };

  if (loading) {
    return <div className="loading">Loading quizzes...</div>;
  }

  if (quizzes.length === 0) {
    return (
      <div className="history-container">
        <div className="empty-state">
          <h2>No quizzes yet</h2>
          <p>Generate your first quiz to see it here!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="history-container">
      {error && <div className="error-message">{error}</div>}

      <div className="quizzes-table">
        <h2>Previous Quizzes ({quizzes.length})</h2>
        
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>URL</th>
                <th>Generated</th>
                <th>Cached</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {quizzes.map((quiz) => (
                <tr key={quiz.id}>
                  <td>
                    <span className="title-text">{quiz.title}</span>
                  </td>
                  <td>
                    <a
                      href={quiz.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="url-link"
                    >
                      {quiz.url.split('/wiki/')[1] || 'View'}
                    </a>
                  </td>
                  <td>
                    <span className="date">
                      {new Date(quiz.created_at).toLocaleDateString()}
                    </span>
                  </td>
                  <td>
                    <span className={`cache-badge ${quiz.is_cached ? 'cached' : 'fresh'}`}>
                      {quiz.is_cached ? 'Yes' : 'No'}
                    </span>
                  </td>
                  <td>
                    <div className="action-buttons">
                      <button
                        className="btn-details"
                        onClick={() => fetchQuizDetails(quiz.id)}
                      >
                        Details
                      </button>
                      <button
                        className="btn-delete"
                        onClick={() => handleDelete(quiz.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default QuizHistory;
