# 🧪 Wiki Quiz Generator - Testing Guide

## Overview

This guide provides comprehensive testing procedures for the Wiki Quiz Generator application.

## Setup for Testing

### Prerequisites
- Backend running on http://localhost:8000
- Frontend running on http://localhost:3000
- PostgreSQL database initialized
- Valid Gemini API key configured

### Test Environment
```bash
# Backend
cd backend
source venv/bin/activate
python main.py

# Frontend (in another terminal)
cd frontend
npm start
```

---

## Test Cases

### 1. TAB 1 - GENERATE QUIZ

#### Test 1.1: Basic Quiz Generation
**Objective**: Verify quiz generates from valid Wikipedia URL

**Steps**:
1. Navigate to Tab 1: "Generate Quiz"
2. Enter URL: `https://en.wikipedia.org/wiki/Alan_Turing`
3. Click "Generate Quiz" button
4. Wait for processing (5-15 seconds)

**Expected Results**:
- ✅ Loading indicator shows during processing
- ✅ Quiz displays with:
  - Article title: "Alan Turing"
  - Summary paragraph (100-500 characters)
  - Key entities (people, organizations, locations)
  - 5-8 quiz questions
  - Related topics list
  - Each question has 4 options (A-D)
  - Difficulty badge (easy/medium/hard)
- ✅ Questions are grounded in article content
- ✅ Correct answer is among the 4 options

**Sample Validation**:
```
Title: "Alan Turing" ✓
Questions: 7 ✓
Sections: ["Early life", "World War II", "Legacy", ...] ✓
Related Topics: ["Turing Machine", "Enigma", ...] ✓
```

---

#### Test 1.2: Invalid URL Handling
**Objective**: Verify error handling for invalid URLs

**Steps**:
1. Navigate to Tab 1
2. Enter invalid URL: `https://example.com/fake`
3. Click "Generate Quiz"

**Expected Results**:
- ✅ Error message displays: "Invalid Wikipedia URL"
- ✅ No loading state
- ✅ Form remains interactive
- ✅ User can try again

---

#### Test 1.3: Empty URL Handling
**Objective**: Verify validation for empty input

**Steps**:
1. Leave URL field empty
2. Click "Generate Quiz"

**Expected Results**:
- ✅ Error message: "Please enter a Wikipedia URL"
- ✅ No API call made
- ✅ Form remains focused on input

---

#### Test 1.4: Network Error Handling
**Objective**: Verify graceful handling of network failures

**Steps**:
1. Stop backend server
2. Enter valid Wikipedia URL
3. Click "Generate Quiz"
4. Wait 10+ seconds for timeout

**Expected Results**:
- ✅ Error message displays (not a blank page)
- ✅ User can see what went wrong
- ✅ Frontend remains responsive
- ✅ User can retry after backend restarts

---

#### Test 1.5: Caching Verification
**Objective**: Verify duplicate URLs return cached result

**Steps**:
1. Generate quiz for: `https://en.wikipedia.org/wiki/Python_(programming_language)`
2. Note response time (should be 5-15 seconds)
3. Click "Generate Quiz" again with same URL
4. Note response time (should be <1 second)
5. Check if `is_cached: false` becomes `is_cached: true`

**Expected Results**:
- ✅ Second generation is much faster
- ✅ Cached result contains identical data
- ✅ Created timestamp matches
- ✅ Cache flag updated appropriately

---

### 2. QUIZ MODE - TAKE QUIZ

#### Test 2.1: Answer Selection
**Objective**: Verify user can select answers

**Steps**:
1. Generate a quiz (from Test 1.1)
2. For each question:
   - Click different option buttons
   - Observe visual feedback

**Expected Results**:
- ✅ Selected option highlights in different color
- ✅ Can change selection by clicking another option
- ✅ All options are clickable
- ✅ Visual feedback is clear

---

#### Test 2.2: Submit Answers
**Objective**: Verify score calculation

**Steps**:
1. Answer all questions (select one per question)
2. Click "Submit Answers" button
3. Observe score calculation

**Expected Results**:
- ✅ Score displays: "X / Y" (e.g., "5 / 7")
- ✅ Score percentage shows (e.g., "71%")
- ✅ Correct answers highlighted in green
- ✅ Incorrect answers highlighted in red
- ✅ Correct answer always shown
- ✅ Explanations display for each question

---

#### Test 2.3: Review Explanations
**Objective**: Verify explanation text is provided

**Steps**:
1. Submit quiz (from Test 2.2)
2. Read explanation box for each question

**Expected Results**:
- ✅ Each answer has an explanation box
- ✅ Explanation explains why correct answer is right
- ✅ Explanation is grounded in article content
- ✅ Text is readable and clear

---

#### Test 2.4: Reset Quiz
**Objective**: Verify quiz can be retaken

**Steps**:
1. Submit quiz (from Test 2.2)
2. Click "Try Again" button
3. Answer differently
4. Submit again

**Expected Results**:
- ✅ Quiz resets to unanswered state
- ✅ Previous answers cleared
- ✅ Score clears
- ✅ Explanations hidden
- ✅ Options become clickable again
- ✅ New score calculated for new answers

---

### 3. TAB 2 - HISTORY VIEW

#### Test 3.1: List Quizzes
**Objective**: Verify history displays all previous quizzes

**Steps**:
1. Generate 3+ quizzes with different URLs (Tests 1.1, 1.2, etc.)
2. Switch to Tab 2: "History"
3. Observe the quizzes table

**Expected Results**:
- ✅ Table displays all generated quizzes
- ✅ Shows Title, URL, Generated Date, Cached status
- ✅ Rows sorted by most recent first
- ✅ Count shows correct total

Example Table:
```
| Title | URL | Generated | Cached | Actions |
|-------|-----|-----------|--------|---------|
| Alan Turing | alu... | Jan 31 | No | Details | Delete |
| Python | pyt... | Jan 31 | Yes | Details | Delete |
```

---

#### Test 3.2: Empty History
**Objective**: Verify empty state when no quizzes exist

**Steps**:
1. Delete all quizzes from database (or fresh install)
2. Switch to Tab 2

**Expected Results**:
- ✅ "No quizzes yet" message displays
- ✅ Friendly instruction: "Generate your first quiz to see it here!"
- ✅ No broken table layouts

---

#### Test 3.3: View Details
**Objective**: Verify details modal displays full quiz

**Steps**:
1. Go to Tab 2 (History)
2. Click "Details" button for any quiz
3. Observe modal content

**Expected Results**:
- ✅ Modal opens with smooth animation
- ✅ Modal displays full quiz (same as Tab 1)
- ✅ All quiz content visible:
  - Article summary
  - Key entities
  - Sections
  - All questions with options
  - Related topics
- ✅ Close button (X) in top-right corner
- ✅ Can click outside modal to close

---

#### Test 3.4: Delete Quiz
**Objective**: Verify quiz deletion from database

**Steps**:
1. Go to Tab 2 (History)
2. Note total quiz count
3. Click "Delete" button for a quiz
4. Confirm deletion in alert
5. Check updated count

**Expected Results**:
- ✅ Confirmation dialog appears
- ✅ Quiz removed from table after confirmation
- ✅ Total count decreases by 1
- ✅ Database reflects deletion (can verify with SQL)
- ✅ Quiz cannot be found if "Details" clicked on other quizzes

---

#### Test 3.5: Sort by Date
**Objective**: Verify chronological sorting

**Steps**:
1. Generate quizzes at different times
2. Go to Tab 2
3. Observe order of quizzes

**Expected Results**:
- ✅ Most recent quizzes appear first
- ✅ Date column shows creation date
- ✅ Order is consistent

---

### 4. ARTICLE EXTRACTION QUALITY

#### Test 4.1: Summary Extraction
**Objective**: Verify article summary is meaningful

**Test URLs**:
- Alan Turing: Should include mathematician/computer scientist
- Python: Should mention programming language/syntax
- Climate Change: Should mention environmental/global warming

**Validation**:
- ✅ Summary is first substantial paragraph
- ✅ Summary is 100-500 characters
- ✅ Summary is grammatically correct
- ✅ Summary introduces the main topic

---

#### Test 4.2: Entity Extraction
**Objective**: Verify key entities are correctly identified

**Expected for Alan Turing**:
- People: Alan Turing, Alonzo Church, etc.
- Organizations: Cambridge, Bletchley Park, etc.
- Locations: England, Princeton, etc.

**Validation**:
- ✅ 5-10 entities per category
- ✅ Entities are relevant to article
- ✅ No duplicate entities
- ✅ No malformed text

---

#### Test 4.3: Section Extraction
**Objective**: Verify article sections are identified

**Expected for Alan Turing**:
```
["Early life", "Mathematical logic", "World War II", "Manchester years", ...]
```

**Validation**:
- ✅ 5-15 sections extracted
- ✅ Sections are main topics
- ✅ Sections appear in article order
- ✅ No "Contents" or meta sections

---

### 5. QUIZ QUALITY ASSESSMENT

#### Test 5.1: Question Diversity
**Objective**: Verify questions cover different topics

**Validation**:
- ✅ Questions span multiple sections
- ✅ Questions test different knowledge types:
  - Factual recall (easy)
  - Comprehension (medium)
  - Analysis/inference (hard)
- ✅ No duplicate questions
- ✅ No questions requiring outside knowledge

---

#### Test 5.2: Answer Correctness
**Objective**: Verify answers are grounded in article

**Process**:
1. For each question, check:
   - Is correct answer mentioned in article?
   - Are incorrect answers plausible but wrong?
   - Could a reader find the answer in article?

**Expected**:
- ✅ All correct answers are in article
- ✅ Incorrect options are realistic distractors
- ✅ No trick questions
- ✅ No ambiguous answers

---

#### Test 5.3: Difficulty Distribution
**Objective**: Verify balanced difficulty levels

**Validation**:
- ✅ Mix of easy (1-2), medium (2-4), hard (1-2) questions
- ✅ Easy questions test basic facts
- ✅ Medium questions test understanding
- ✅ Hard questions test deep comprehension

---

#### Test 5.4: Related Topics Relevance
**Objective**: Verify suggested topics are related

**For Alan Turing, expect**:
- Turing Machine ✅
- Enigma Machine ✅
- Bletchley Park ✅
- NOT: "Pizza" ❌

**Validation**:
- ✅ 5-8 related topics
- ✅ Topics exist on Wikipedia
- ✅ Topics are directly related
- ✅ No spam/irrelevant topics

---

### 6. RESPONSIVE DESIGN

#### Test 6.1: Desktop (1920x1080)
**Objective**: Verify UI on desktop

**Validation**:
- ✅ Content not cramped
- ✅ Multiple columns work properly
- ✅ All buttons accessible
- ✅ Text readable

#### Test 6.2: Tablet (768x1024)
**Objective**: Verify UI on tablet

**Validation**:
- ✅ Single column layout works
- ✅ Touch targets are large enough
- ✅ No horizontal scroll needed
- ✅ Modals are appropriately sized

#### Test 6.3: Mobile (375x667)
**Objective**: Verify UI on mobile

**Validation**:
- ✅ Content stacks vertically
- ✅ Touch targets are 44px minimum
- ✅ No overflow issues
- ✅ Modal covers full screen
- ✅ Forms are usable

---

### 7. PERFORMANCE TESTING

#### Test 7.1: Quiz Generation Time
**Objective**: Verify acceptable response time

**Expected**:
- Cold generation: 5-15 seconds
- Cached result: <1 second

**Validation**:
- ✅ First generation completes within 15 seconds
- ✅ Loading state shows during processing
- ✅ Cached results are instant

#### Test 7.2: API Response Times
**Objective**: Verify API endpoints are fast

Using browser DevTools Network tab:
- POST /api/quiz/generate: 5-15s
- GET /api/quiz/list: <500ms
- GET /api/quiz/{id}: <500ms
- DELETE /api/quiz/{id}: <500ms

---

### 8. DATABASE INTEGRITY

#### Test 8.1: Data Persistence
**Objective**: Verify data survives backend restart

**Steps**:
1. Generate quiz (Tab 1)
2. Stop backend
3. Start backend
4. Go to Tab 2 (History)

**Expected**:
- ✅ Quiz still appears in history
- ✅ All data (quiz questions, metadata) intact
- ✅ No data corruption

#### Test 8.2: Concurrent Access
**Objective**: Verify multiple browsers don't conflict

**Steps**:
1. Open app in 2 browser windows
2. Generate different quizzes simultaneously
3. Check history in both windows

**Expected**:
- ✅ Both quizzes appear in history
- ✅ No data loss
- ✅ No duplicate entries

---

## Regression Testing Checklist

Before each release:

- [ ] Tab 1: Generate Quiz with valid URL
- [ ] Tab 1: Error handling (invalid URL, empty input)
- [ ] Quiz Mode: Answer selection and submission
- [ ] Quiz Mode: Score calculation accuracy
- [ ] Tab 2: History displays all quizzes
- [ ] Tab 2: Delete quiz functionality
- [ ] Tab 2: Details modal opens/closes
- [ ] Caching: Second generation is faster
- [ ] Responsive: Desktop, tablet, mobile layouts work
- [ ] Database: Data persists after restart
- [ ] API: All endpoints return correct status codes
- [ ] Error Messages: All error messages are clear
- [ ] UI: No console errors in DevTools

---

## Sample Test Data

Recommended Wikipedia URLs for testing:
- ✅ https://en.wikipedia.org/wiki/Alan_Turing
- ✅ https://en.wikipedia.org/wiki/Python_(programming_language)
- ✅ https://en.wikipedia.org/wiki/Climate_change
- ✅ https://en.wikipedia.org/wiki/Artificial_intelligence
- ✅ https://en.wikipedia.org/wiki/DNA

---

## Troubleshooting Test Failures

### Quiz won't generate
- Check Gemini API key is valid
- Check internet connection
- Check backend logs for errors
- Verify PostgreSQL is running

### Score calculation wrong
- Check quiz JSON format
- Verify answer is in options
- Check difficulty level format

### Modal won't open
- Check browser console for errors
- Verify quiz data is complete
- Try refreshing page

### History shows cached=false
- First generation always shows false
- Generate again to see cached=true

---

## Performance Benchmarks

**Targets**:
- Cold quiz generation: < 15s
- Cached quiz return: < 1s
- History load: < 500ms
- Modal open: < 100ms

---

**Last Updated**: January 31, 2026
