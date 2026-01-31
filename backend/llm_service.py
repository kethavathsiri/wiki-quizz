"""
LLM service for generating quizzes using LangChain and Google Gemini
Falls back to mock generator if quota is exceeded
"""
import json
import logging
from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GEMINI_API_KEY
from mock_quiz_generator import MockQuizGenerator
import google.api_core.exceptions

logger = logging.getLogger(__name__)

class QuizGenerator:
    """Generate quizzes from article content using LLM"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.7,
            max_output_tokens=2048
        )
        self.quiz_prompt = self._create_quiz_prompt()
        self.topics_prompt = self._create_topics_prompt()
        self.mock_generator = MockQuizGenerator()
        # Use mock generator by default until Gemini quota resets
        self.use_mock = True
    
    def _create_quiz_prompt(self) -> PromptTemplate:
        """Create prompt template for quiz generation"""
        template = """You are a quiz generator. Your ONLY task is to generate valid JSON.

Article: {title}
Content: {content}

Generate exactly 5 multiple-choice questions based on the article.

RULES:
- Output ONLY valid JSON array
- NO markdown, NO explanations, NO extra text
- Each question must have exactly 4 options
- Answer must be one of the 4 options (exact match)
- Difficulty must be: easy, medium, or hard
- All fields required: question, options, answer, difficulty, explanation

JSON FORMAT:
[
  {{
    "question": "What is..?",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "answer": "Option 2",
    "difficulty": "medium",
    "explanation": "Because..."
  }}
]

Generate the quiz:"""
        
        return PromptTemplate(
            input_variables=["title", "content"],
            template=template
        )
    
    def _create_topics_prompt(self) -> PromptTemplate:
        """Create prompt template for related topics"""
        template = """Based on the following Wikipedia article, suggest 5-8 related Wikipedia topics for further reading.

Article Title: {title}
Article Content Summary:
{content}

IMPORTANT INSTRUCTIONS:
1. Suggest real Wikipedia topics related to the article
2. Topics should be diverse and relevant
3. Return ONLY a JSON array of topic names (strings)
4. No markdown, no extra text

Return in this exact format:
["Topic 1", "Topic 2", "Topic 3", ...]

Generate the related topics now:"""
        
        return PromptTemplate(
            input_variables=["title", "content"],
            template=template
        )
    
    def generate_quiz(self, title: str, content: str) -> List[Dict]:
        """
        Generate quiz questions from article content
        Falls back to mock generator if LLM quota is exceeded
        """
        try:
            logger.info(f"Generating quiz for article: {title}")
            logger.debug(f"Content length: {len(content)} characters")
            
            # If mock mode is enabled, use it directly
            if self.use_mock:
                logger.info("Using mock quiz generator (LLM quota exceeded)")
                return self.mock_generator.generate_quiz(title, content)
            
            try:
                chain = LLMChain(llm=self.llm, prompt=self.quiz_prompt)
                response = chain.invoke(input={"title": title, "content": content})["text"]
            except (google.api_core.exceptions.ResourceExhausted, Exception) as llm_err:
                # Check if it's a quota error or timeout
                err_str = str(llm_err).lower()
                if "quota" in err_str or "429" in err_str or "exceeded" in err_str or "timeout" in err_str:
                    logger.warning(f"LLM unavailable (quota/timeout): {type(llm_err).__name__}")
                    logger.info("Switching to mock quiz generator")
                    self.use_mock = True
                    return self.mock_generator.generate_quiz(title, content)
                # Re-raise other errors
                raise
            
            logger.info(f"LLM Response length: {len(response)} chars")
            logger.debug(f"LLM Response (first 500 chars): {response[:500]}")
            
            # Clean and extract JSON from response
            try:
                quiz_data = self._extract_json_from_response(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to extract JSON from primary response: {e}")
                logger.error(f"Response was: {response[:300]}")
                # Fall back to mock generator on JSON extraction failure
                logger.info("Falling back to mock quiz generator")
                self.use_mock = True
                return self.mock_generator.generate_quiz(title, content)
            
            logger.info(f"Extracted {len(quiz_data) if isinstance(quiz_data, list) else 1} potential questions")
            
            # Validate and clean quiz data
            cleaned_quiz = []
            for idx, question in enumerate(quiz_data if isinstance(quiz_data, list) else [quiz_data]):
                logger.debug(f"Validating question {idx + 1}")
                if self._validate_question(question):
                    # Clean text fields
                    cleaned_question = self._clean_question(question)
                    cleaned_quiz.append(cleaned_question)
                    logger.debug(f"Question {idx + 1} validated and cleaned")
                else:
                    logger.warning(f"Question {idx + 1} failed validation")
            
            logger.info(f"Generated {len(cleaned_quiz)} valid quiz questions")
            # Ensure minimum 5 questions
            if len(cleaned_quiz) < 5:
                logger.warning(f"Only {len(cleaned_quiz)} questions generated, need at least 5")
                return []  # Return empty to signal failure
            return cleaned_quiz[:8]  # Return max 8 questions
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM quiz response: {e}")
            # Fall back to mock generator
            return self.mock_generator.generate_quiz(title, content)
        except Exception as e:
            logger.error(f"Error generating quiz: {e}", exc_info=True)
            # Fall back to mock generator on any error
            return self.mock_generator.generate_quiz(title, content)
    
    def generate_related_topics(self, title: str, content: str) -> List[str]:
        """
        Generate related Wikipedia topics
        Falls back to mock generator if LLM fails
        """
        try:
            if self.use_mock:
                logger.info("Using mock related topics generator")
                return self.mock_generator.generate_related_topics(title, content)
            
            chain = LLMChain(llm=self.llm, prompt=self.topics_prompt)
            response = chain.invoke(input={"title": title, "content": content})["text"]
            
            # Clean and extract JSON from response
            topics = self._extract_json_from_response(response)
            
            # Ensure it's a list of strings
            if isinstance(topics, list):
                cleaned_topics = []
                for topic in topics:
                    if isinstance(topic, str):
                        cleaned = topic.strip()
                        if cleaned:
                            cleaned_topics.append(cleaned)
                return cleaned_topics[:8]
            
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM topics response: {e}")
            logger.info("Falling back to mock related topics generator")
            return self.mock_generator.generate_related_topics(title, content)
        except Exception as e:
            logger.error(f"Error generating related topics: {e}")
            return self.mock_generator.generate_related_topics(title, content)
    
    def _extract_json_from_response(self, response: str):
        """
        Extract JSON from LLM response that may contain markdown or extra text
        """
        import re
        
        logger.debug(f"Attempting to extract JSON from response (length: {len(response)})")
        logger.debug(f"Response preview: {response[:300]}")
        
        # Handle empty response
        if not response or not response.strip():
            logger.error("Response is empty")
            raise json.JSONDecodeError("Response is empty", response, 0)
        
        # Try direct JSON parsing first
        try:
            result = json.loads(response)
            logger.debug("Successfully parsed response as valid JSON")
            return result
        except json.JSONDecodeError:
            logger.debug("Direct JSON parsing failed, trying pattern matching")
            pass
        
        # Remove markdown code blocks if present
        response_clean = re.sub(r'```json\s*\n?', '', response)
        response_clean = re.sub(r'```\s*\n?', '', response_clean)
        response_clean = response_clean.strip()
        
        # Try again after removing markdown
        try:
            result = json.loads(response_clean)
            logger.debug("Successfully parsed after removing markdown")
            return result
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON array pattern (more permissive - match nested braces)
        json_match = re.search(r'\[\s*\{.*?\}\s*(?:,\s*\{.*?\}\s*)*\]', response_clean, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                logger.debug(f"Found JSON array pattern, extracted {len(result) if isinstance(result, list) else 1} items")
                return result
            except json.JSONDecodeError as e:
                logger.debug(f"JSON array pattern found but failed to parse: {e}")
                pass
        
        # Try to find JSON object pattern
        json_match = re.search(r'\{.*?\}', response_clean, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                logger.debug(f"Found JSON object pattern")
                return result
            except json.JSONDecodeError:
                logger.debug("JSON object pattern found but failed to parse")
                pass
        
        # If all else fails, raise error with more context
        logger.error(f"Could not extract valid JSON from response")
        logger.error(f"Full response: {response_clean[:500]}")
        raise json.JSONDecodeError("Could not extract JSON from response", response_clean, 0)
    
    def _clean_question(self, question: Dict) -> Dict:
        """
        Clean question text by removing HTML entities and extra whitespace
        """
        def clean_text(text):
            if not isinstance(text, str):
                return text
            # Remove common HTML entities
            text = text.replace('&quot;', '"')
            text = text.replace('&apos;', "'")
            text = text.replace('&amp;', '&')
            text = text.replace('&lt;', '<')
            text = text.replace('&gt;', '>')
            # Normalize whitespace
            text = ' '.join(text.split())
            return text.strip()
        
        return {
            "question": clean_text(question.get("question", "")),
            "options": [clean_text(opt) for opt in question.get("options", [])],
            "answer": clean_text(question.get("answer", "")),
            "difficulty": question.get("difficulty", "medium").lower(),
            "explanation": clean_text(question.get("explanation", ""))
        }    
    def _validate_question(self, question: Dict) -> bool:
        """Validate question has required fields"""
        required_fields = ["question", "options", "answer", "difficulty", "explanation"]
        
        # Check all required fields exist
        if not all(field in question for field in required_fields):
            return False
        
        # Validate options
        options = question.get("options", [])
        if not isinstance(options, list) or len(options) != 4:
            return False
        
        # Validate answer is in options (after cleaning)
        answer = question.get("answer", "")
        if answer not in options:
            return False
        
        # Validate difficulty
        difficulty = question.get("difficulty", "").lower()
        if difficulty not in ["easy", "medium", "hard"]:
            return False
        
        # Validate text fields are not empty
        if not question.get("question", "").strip():
            return False
        if not question.get("explanation", "").strip():
            return False
        
        return True