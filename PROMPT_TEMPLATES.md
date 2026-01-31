## LangChain Prompt Templates for Wiki Quiz Generation

This document outlines the LangChain prompt templates used in the Wiki Quiz application for generating quizzes and related topics from Wikipedia articles.

### 1. Quiz Generation Prompt Template

**File**: `backend/llm_service.py` - `_create_quiz_prompt()` method

**Purpose**: Generate multiple-choice quiz questions from Wikipedia article content with grounding in source material.

```python
TEMPLATE = """Based on the following Wikipedia article content, generate a quiz with 5-8 multiple-choice questions.

Article Title: {title}
Article Content:
{content}

IMPORTANT INSTRUCTIONS:
1. Generate questions that are grounded in the article content
2. Each question must have 4 options (A-D)
3. Difficulty levels: easy, medium, or hard
4. Questions should test understanding, not just memorization
5. Provide brief explanations for each answer
6. Return ONLY valid JSON (no markdown, no extra text)

Return the quiz in this exact JSON format:
[
  {
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Correct option text",
    "difficulty": "easy|medium|hard",
    "explanation": "Why this is correct"
  }
]

Generate the quiz now:"""
```

**Key Design Decisions**:
- **Grounding Requirement**: Explicit instruction to base questions on article content minimizes hallucination
- **JSON-only Output**: Eliminates parsing issues with markdown formatting
- **Difficulty Levels**: Ensures question variety and appropriate challenge
- **Format Specification**: Exact JSON schema prevents parsing errors
- **No Markdown**: Forces strict JSON format compliance

**Expected Input**:
- `title`: Article title (string)
- `content`: Extracted article text, limited to 5000 characters

**Expected Output**:
- Array of quiz questions (JSON)
- Each with question, 4 options, correct answer, difficulty, and explanation

---

### 2. Related Topics Generation Prompt Template

**File**: `backend/llm_service.py` - `_create_topics_prompt()` method

**Purpose**: Generate relevant Wikipedia topics for further reading based on article content.

```python
TEMPLATE = """Based on the following Wikipedia article, suggest 5-8 related Wikipedia topics for further reading.

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
```

**Key Design Decisions**:
- **Real Topics**: Constraint ensures suggested topics are verifiable on Wikipedia
- **Diversity Requirement**: Prevents repetitive or closely related suggestions
- **Array Format**: Simple JSON array for easy parsing
- **Content Limitation**: Uses article summary rather than full content for efficiency

**Expected Input**:
- `title`: Article title (string)
- `content`: Article summary/content excerpt

**Expected Output**:
- JSON array of 5-8 related topic names (strings)

---

### 3. Prompt Optimization Strategies

#### Content Preparation
- **Text Truncation**: Article content limited to 5000 characters to manage token usage
- **Noise Removal**: Wikipedia markup, script tags, and styles removed before content extraction
- **Section Prioritization**: Summary and key sections highlighted to focus LLM attention

#### Constraint Engineering
- **Explicit Format Specification**: Detailed JSON schema prevents ambiguous outputs
- **Strict Instructions**: All-caps "IMPORTANT INSTRUCTIONS" section ensures attention
- **Output Validation**: Backend validates all responses before returning to frontend

#### Hallucination Mitigation
1. **Source Grounding**: "Based on the following content" anchors model to provided material
2. **Answer Verification**: Backend checks that correct answer is in options list
3. **Difficulty Validation**: Only accepts predefined difficulty levels
4. **Content Context**: Providing article title and content prevents generic questions

---

### 4. Response Validation

**File**: `backend/llm_service.py` - `_validate_question()` method

```python
def _validate_question(self, question: Dict) -> bool:
    # Checks:
    # 1. All required fields present
    # 2. Exactly 4 options provided
    # 3. Correct answer is in options list
    # 4. Difficulty is easy/medium/hard
```

---

### 5. Example Prompt-Response Cycle

**Input Article Excerpt** (Alan Turing):
```
"Alan Turing was a British mathematician... He worked at Bletchley Park 
during WWII breaking the Enigma code. He proposed the Turing Test..."
```

**Generated Quiz Question**:
```json
{
  "question": "What was Alan Turing's primary role during World War II?",
  "options": [
    "Developing radar technology",
    "Breaking the Enigma code",
    "Building fighter aircraft",
    "Managing supply lines"
  ],
  "answer": "Breaking the Enigma code",
  "difficulty": "medium",
  "explanation": "Mentioned in the provided content as his key wartime contribution at Bletchley Park."
}
```

---

### 6. Token Efficiency

**Estimated Token Usage per Request**:
- Quiz generation: ~1500-2000 tokens
  - Input: ~200 (instructions) + ~500 (content) = ~700
  - Output: ~800-1300 (8 questions × 100-150 tokens each)
- Related topics: ~500-800 tokens
  - Input: ~200 (instructions) + ~300 (content) = ~500
  - Output: ~300 (topic list)

**Total per Wikipedia article**: ~2500 tokens (well within Gemini free tier limits)

---

### 7. Future Optimization Opportunities

1. **Few-shot Prompting**: Add example Q&A pairs to improve consistency
2. **Question Diversity**: Add constraint to avoid similar questions from same section
3. **Entity-Based Questions**: Emphasize key entities (people, organizations, locations)
4. **Multi-language Support**: Extend prompts for non-English Wikipedia
5. **Adaptive Difficulty**: Generate questions calibrated to article complexity

