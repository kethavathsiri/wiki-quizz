import QuizDisplay from './QuizDisplay';
import './QuizModal.css';

function QuizModal({ quiz, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>
        <QuizDisplay quiz={quiz} />
      </div>
    </div>
  );
}

export default QuizModal;
