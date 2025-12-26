#!/usr/bin/env python3
"""
Test script to verify Ollama integration
"""
import sys
import os

# Add the workspace to the Python path
sys.path.insert(0, '/workspace')

from llm.generator import test_ollama_connection, generate_sql_with_ollama

def test_ollama():
    print("Testing Ollama connection...")
    if test_ollama_connection():
        print("✅ Ollama connection successful!")
        
        # Test generating SQL
        print("\nTesting SQL generation with Ollama...")
        prompt = "Convert this natural language to SQL: Show all users from the users table"
        result = generate_sql_with_ollama(prompt, model="llama2")
        
        if result:
            print(f"✅ SQL generated successfully:")
            print(result)
        else:
            print("❌ Failed to generate SQL")
    else:
        print("❌ Ollama connection failed. Make sure Ollama is running on localhost:11434")
        print("To start Ollama, run: ollama serve")

if __name__ == "__main__":
    test_ollama()