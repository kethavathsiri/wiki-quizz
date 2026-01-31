#!/usr/bin/env python
"""Debug script to trace data flow from scraping to API response"""
import json
import sys
from scraper import scrape_wikipedia_article
from llm_service import QuizGenerator

def debug_scraper():
    """Test scraping and see what data is extracted"""
    
    # Use Alan Turing article
    url = "https://en.wikipedia.org/wiki/Alan_Turing"
    
    print("=" * 80)
    print(f"SCRAPING: {url}")
    print("=" * 80)
    
    try:
        scraped_data = scrape_wikipedia_article(url)
        
        print(f"\n1. TITLE:")
        print(f"   {scraped_data['title']}")
        
        print(f"\n2. SUMMARY (first 300 chars):")
        print(f"   {scraped_data['summary'][:300]}...")
        print(f"   Length: {len(scraped_data['summary'])} chars")
        
        print(f"\n3. SECTIONS ({len(scraped_data['sections'])} total):")
        for i, section in enumerate(scraped_data['sections'][:5], 1):
            print(f"   {i}. {section}")
        if len(scraped_data['sections']) > 5:
            print(f"   ... and {len(scraped_data['sections']) - 5} more")
        
        print(f"\n4. KEY ENTITIES:")
        entities = scraped_data['key_entities']
        print(f"   People: {entities.get('people', [])[:3]}")
        print(f"   Organizations: {entities.get('organizations', [])[:3]}")
        print(f"   Locations: {entities.get('locations', [])[:3]}")
        
        print(f"\n5. FULL TEXT (first 500 chars):")
        full_text = scraped_data['full_text']
        print(f"   {full_text[:500]}...")
        print(f"   Length: {len(full_text)} chars")
        
        # Check for noise
        print(f"\n6. NOISE ANALYSIS:")
        noise_indicators = {
            'Reference markers [1], [2]': len([c for c in full_text if c == '[']) > 5,
            'Extra whitespace': '  ' in full_text,
            'Garbled text': any(char in full_text for char in ['\x00', '\x01']),
            'Special chars': sum(1 for c in full_text if ord(c) > 127),
        }
        for indicator, found in noise_indicators.items():
            status = "❌ FOUND" if found else "✓ OK"
            print(f"   {status}: {indicator}")
        
        # Now test LLM quiz generation
        print("\n" + "=" * 80)
        print("GENERATING QUIZ")
        print("=" * 80)
        
        qg = QuizGenerator()
        quiz = qg.generate_quiz(scraped_data['title'], scraped_data['full_text'])
        
        print(f"\nGenerated {len(quiz)} questions")
        
        if len(quiz) > 0:
            print("\nFirst question sample:")
            q = quiz[0]
            print(f"  Question: {q['question']}")
            print(f"  Options: {q['options']}")
            print(f"  Answer: {q['answer']}")
            print(f"  Difficulty: {q['difficulty']}")
        else:
            print("\n❌ NO QUESTIONS GENERATED!")
            print("   This means the LLM extraction failed or validation failed")
        
        # Create a mock API response
        print("\n" + "=" * 80)
        print("API RESPONSE STRUCTURE")
        print("=" * 80)
        
        api_response = {
            "title": scraped_data['title'],
            "summary": scraped_data['summary'],
            "sections": scraped_data['sections'],
            "key_entities": scraped_data['key_entities'],
            "quiz": quiz,
            "related_topics": []
        }
        
        print(f"\nResponse keys: {list(api_response.keys())}")
        print(f"Quiz questions: {len(api_response['quiz'])}")
        
        # Check response for noise
        print(f"\n7. RESPONSE CONTENT CHECK:")
        print(f"   Title clean: {'✓' if isinstance(api_response['title'], str) else '❌'}")
        print(f"   Summary length: {len(api_response['summary'])} chars")
        print(f"   Quiz count: {len(api_response['quiz'])}")
        
        if len(api_response['quiz']) > 0:
            first_q = api_response['quiz'][0]
            print(f"\n   First question fields:")
            for key, value in first_q.items():
                if isinstance(value, str):
                    print(f"      {key}: {value[:50]}..." if len(str(value)) > 50 else f"      {key}: {value}")
                else:
                    print(f"      {key}: {type(value).__name__} with {len(value)} items")
        
        # Save response to file for inspection
        print("\n" + "=" * 80)
        print("SAVING DEBUG DATA")
        print("=" * 80)
        
        with open('/tmp/debug_response.json', 'w') as f:
            json.dump(api_response, f, indent=2)
        print("✓ Saved to /tmp/debug_response.json")
        
        with open('/tmp/debug_raw_text.txt', 'w') as f:
            f.write(scraped_data['full_text'])
        print("✓ Saved raw text to /tmp/debug_raw_text.txt")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_scraper()
    sys.exit(0 if success else 1)
