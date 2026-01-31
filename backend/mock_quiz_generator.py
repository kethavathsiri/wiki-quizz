"""
Mock quiz generator for testing when LLM quota is exceeded.
Generates plausible quiz questions based on article content.
"""
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class MockQuizGenerator:
    """Generate quiz questions from article text without LLM"""
    
    def generate_quiz(self, title: str, content: str) -> List[Dict]:
        """Generate 5+ quiz questions from article content"""
        try:
            # Extract key sentences from content
            sentences = self._extract_sentences(content)
            if not sentences:
                logger.warning("Could not extract sentences from content")
                return []
            
            questions = []
            
            # Generate different types of questions
            for i, sentence in enumerate(sentences[:8]):
                if len(questions) >= 8:
                    break
                
                if i % 3 == 0:
                    q = self._create_fill_blank_question(sentence, i)
                elif i % 3 == 1:
                    q = self._create_true_false_question(sentence, i)
                else:
                    q = self._create_multiple_choice_question(sentence, i)
                
                if q:
                    questions.append(q)
            
            logger.info(f"Generated {len(questions)} mock quiz questions")
            return questions[:8]
        except Exception as e:
            logger.error(f"Error generating mock quiz: {e}")
            return []
    
    def _extract_sentences(self, content: str) -> List[str]:
        """Extract meaningful sentences from content"""
        # Split by period, question mark, exclamation mark
        sentences = re.split(r'[.!?]+', content)
        
        # Filter to meaningful sentences (30-150 chars)
        meaningful = []
        for sent in sentences:
            sent = sent.strip()
            if 30 < len(sent) < 150 and not sent.startswith('['):
                meaningful.append(sent)
        
        return meaningful[:20]
    
    def _create_fill_blank_question(self, sentence: str, index: int) -> Dict:
        """Create a fill-in-the-blank style question"""
        # Find a good word to blank out (not too common)
        words = sentence.split()
        if len(words) < 5:
            return None
        
        blank_idx = min(index % len(words), len(words) - 1)
        target_word = words[blank_idx]
        
        if len(target_word) < 3:  # Skip small words
            return None
        
        question_text = ' '.join(words[:blank_idx] + ['_____'] + words[blank_idx+1:])
        
        # Generate plausible wrong answers
        options = [target_word]
        wrong_answers = self._generate_similar_words(target_word)
        options.extend(wrong_answers[:3])
        
        if len(options) < 4:
            return None
        
        import random
        random.shuffle(options)
        
        return {
            "question": f"Fill in the blank: {question_text}",
            "options": options,
            "answer": target_word,
            "difficulty": ["easy", "medium", "hard"][index % 3],
            "explanation": f"The correct answer is '{target_word}' based on the context."
        }
    
    def _create_true_false_question(self, sentence: str, index: int) -> Dict:
        """Create a true/false style question converted to multiple choice"""
        question_text = sentence.replace('.', '').strip()
        is_true = index % 2 == 0
        
        if is_true:
            answer = "True"
            explanation = "This statement is correct based on the article content."
        else:
            answer = "False"
            question_text = question_text.replace('is', 'is not').replace('was', 'was not')
            explanation = "This statement is incorrect. The actual fact is the opposite."
        
        return {
            "question": f"Is the following statement true? {question_text}",
            "options": ["True", "False", "Cannot be determined", "Partially true"],
            "answer": answer,
            "difficulty": ["easy", "medium", "hard"][index % 3],
            "explanation": explanation
        }
    
    def _create_multiple_choice_question(self, sentence: str, index: int) -> Dict:
        """Create a regular multiple choice question"""
        # Extract key entities or concepts
        words = sentence.split()
        if len(words) < 6:
            return None
        
        # Create a question that asks about a key term
        key_word_idx = min(2 + (index % 3), len(words) - 1)
        key_word = words[key_word_idx]
        
        if len(key_word) < 3:
            return None
        
        question = f"According to the article, what is the significance of '{key_word}'?"
        
        # Generate options
        correct_answer = "A key concept mentioned in the article"
        wrong_answers = [
            "A term not mentioned in the article",
            "A concept from a different topic",
            "A historical reference not related to the subject"
        ]
        
        options = [correct_answer] + wrong_answers
        import random
        random.shuffle(options)
        
        return {
            "question": question,
            "options": options,
            "answer": correct_answer,
            "difficulty": ["easy", "medium", "hard"][index % 3],
            "explanation": f"'{key_word}' is mentioned in the article as part of the main content."
        }
    
    def _generate_similar_words(self, word: str) -> List[str]:
        """Generate plausible wrong answers"""
        # Simple approach: common wrong answers
        common_wrong = [
            word[:-1] if len(word) > 1 else word + 's',  # Remove/add suffix
            word.capitalize() if word.islower() else word.lower(),  # Change case
            word + 'ing' if not word.endswith('ing') else word[:-3],  # Add/remove -ing
            'the ' + word.lower(),  # Add article
        ]
        return [w for w in common_wrong if w != word][:3]
    
    def generate_related_topics(self, title: str, content: str) -> List[str]:
        """Generate related topics based on content keywords"""
        # Extract common nouns and proper nouns
        words = re.findall(r'\b[A-Z][a-z]+\b', content)
        
        # Get unique words, limit to 8
        topics = list(set(words))[:8]
        
        if len(topics) < 5:
            # Fallback: add generic related topics
            topics.extend([
                "History",
                "Science",
                "Technology",
                "Culture",
                "Society"
            ])
        
        return topics[:8]
