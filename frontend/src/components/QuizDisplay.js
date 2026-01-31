import { useState } from 'react';
import './QuizDisplay.css';

function QuizDisplay({ quiz }) {
  const [userAnswers, setUserAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const handleAnswerSelect = (questionIndex, option) => {
    if (!submitted) {
      setUserAnswers({
        ...userAnswers,
        [questionIndex]: option
      });
    }
  };

  const handleSubmitAnswers = () => {
    let correctCount = 0;
    quiz.quiz.forEach((question, index) => {
      if (userAnswers[index] === question.answer) {
        correctCount++;
      }
    });
    setScore(correctCount);
    setSubmitted(true);
  };

  const handleReset = () => {
    setUserAnswers({});
    setSubmitted(false);
    setScore(0);
  };

  return (
    <div className="quiz-display">
      {/* Article Info */}
      <div className="article-info">
        <h2>{quiz.title}</h2>
        <p className="summary">{quiz.summary}</p>
        
        {/* Key Entities */}
        {quiz.key_entities && (
          <div className="entities-section">
            <h3>Key Entities</h3>
            <div className="entities-grid">
              {quiz.key_entities.people?.length > 0 && (
                <div className="entity-box">
                  <h4>People</h4>
                  <ul>
                    {quiz.key_entities.people.map((person, idx) => (
                      <li key={idx}>{person}</li>
                    ))}
                  </ul>
                </div>
              )}
              {quiz.key_entities.organizations?.length > 0 && (
                <div className="entity-box">
                  <h4>Organizations</h4>
                  <ul>
                    {quiz.key_entities.organizations.map((org, idx) => (
                      <li key={idx}>{org}</li>
                    ))}
                  </ul>
                </div>
              )}
              {quiz.key_entities.locations?.length > 0 && (
                <div className="entity-box">
                  <h4>Locations</h4>
                  <ul>
                    {quiz.key_entities.locations.map((loc, idx) => (
                      <li key={idx}>{loc}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Sections */}
        {quiz.sections?.length > 0 && (
          <div className="sections-section">
            <h3>Article Sections</h3>
            <div className="sections-list">
              {quiz.sections.map((section, idx) => (
                <span key={idx} className="section-tag">{section}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Quiz Questions */}
      <div className="quiz-section">
        <h2>Quiz ({quiz.quiz?.length || 0} questions)</h2>
        
        {submitted && (
          <div className="score-display">
            <h3>Your Score: {score} / {quiz.quiz?.length || 0}</h3>
            <div className="score-percentage">
              {Math.round((score / (quiz.quiz?.length || 1)) * 100)}%
            </div>
          </div>
        )}

        <div className="questions-container">
          {quiz.quiz?.map((question, qIdx) => {
            const isAnswered = userAnswers[qIdx] !== undefined;
            const isCorrect = userAnswers[qIdx] === question.answer;

            return (
              <div key={qIdx} className="question-card">
                <div className="question-header">
                  <h3>Question {qIdx + 1}</h3>
                  <span className={`difficulty ${question.difficulty}`}>
                    {question.difficulty}
                  </span>
                </div>

                <p className="question-text">{question.question}</p>

                <div className="options-grid">
                  {question.options?.map((option, oIdx) => {
                    const isSelected = userAnswers[qIdx] === option;
                    let className = 'option-button';
                    
                    if (submitted) {
                      if (option === question.answer) className += ' correct';
                      if (isSelected && !isCorrect) className += ' incorrect';
                    }
                    if (isSelected && !submitted) className += ' selected';

                    return (
                      <button
                        key={oIdx}
                        className={className}
                        onClick={() => handleAnswerSelect(qIdx, option)}
                        disabled={submitted}
                      >
                        <span className="option-letter">
                          {String.fromCharCode(65 + oIdx)}
                        </span>
                        <span className="option-text">{option}</span>
                      </button>
                    );
                  })}
                </div>

                {submitted && (
                  <div className="explanation-box">
                    <p className="explanation-label">Explanation:</p>
                    <p>{question.explanation}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {!submitted ? (
          <button className="submit-quiz-button" onClick={handleSubmitAnswers}>
            Submit Answers
          </button>
        ) : (
          <button className="reset-quiz-button" onClick={handleReset}>
            Try Again
          </button>
        )}
      </div>

      {/* Related Topics */}
      {quiz.related_topics?.length > 0 && (
        <div className="related-topics-section">
          <h2>Related Topics for Further Reading</h2>
          <div className="topics-grid">
            {quiz.related_topics.map((topic, idx) => (
              <a
                key={idx}
                href={`https://en.wikipedia.org/wiki/${topic.replace(/\s+/g, '_')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="topic-card"
              >
                <span>{topic}</span>
                <span className="external-icon">↗</span>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default QuizDisplay;
