import os
import json
import re
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# FIX 1: Initialize ChatNVIDIA with proper configuration
api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

# Use meta/llama instead of nvidia/ namespace for standard models
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    api_key=api_key,
    temperature=0.7
)

def analyze_paper(pdf_path):
    """Extracts hardware relationships from PDF using NVIDIA NIM."""
    if not os.path.exists(pdf_path):
        return []

    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        
        # FIX 2: Skip the cover page and table of contents. Read pages 2 through 7.
        context = "\n".join([p.page_content for p in pages[1:7]]) 

        prompt = ChatPromptTemplate.from_template("""
        You are an NVIDIA Systems Research Assistant. 
        Analyze the text and extract technical relationships.
        Focus on: Architectures (Blackwell, Hopper, Ampere) and Features (FP4, NVLink, Cuda).

        Return ONLY a JSON list of objects. No intro, no outro.
        Format: [{{"source": "...", "relation": "...", "target": "..."}}]

        Context: {context}
        """)

        chain = prompt | llm
        response = chain.invoke({"context": context})
        
        # Clean the response string to find the JSON list
        raw_content = response.content.strip()
        
        # FIX 3: The "X-Ray" Debug Prints
        print("\n=== RAW LLM OUTPUT ===")
        print(raw_content)
        print("========================\n")

        # Regex to extract content between [ and ] in case the LLM adds text
        json_match = re.search(r'\[.*\]', raw_content, re.DOTALL)
        
        if json_match:
            return json.loads(json_match.group())
        else:
            print("Regex failed to find JSON brackets.")
            return []

    except Exception as e:
        # This will now print the exact API or file error in your terminal!
        print(f"\n❌ EXTRACTION ERROR: {e}\n")
        return []