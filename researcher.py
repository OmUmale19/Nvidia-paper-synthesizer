import os
import json
import re
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize ChatNVIDIA with proper configuration
api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

# Use meta/llama instead of nvidia/ namespace for standard models
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    api_key=api_key,
    temperature=0.3  # Lower temperature for more consistent JSON
)

def parse_json_response(response_text):
    """Parse JSON from LLM response with multiple strategies."""
    # Strategy 1: Try to find JSON array directly
    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    # Strategy 2: Try to find JSON object and convert to array
    obj_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if obj_match:
        try:
            obj = json.loads(obj_match.group())
            return [obj] if isinstance(obj, dict) else obj
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Try to clean markdown code blocks
    cleaned = response_text.replace('```json', '').replace('```', '').strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    
    return []

def analyze_paper(pdf_path):
    """Extracts hardware relationships from PDF using NVIDIA NIM."""
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found: {pdf_path}")
        return []

    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        
        if not pages:
            print("❌ No pages extracted from PDF")
            return []
        
        # Use first 8 pages for context
        context = "\n".join([p.page_content for p in pages[:8]])
        
        # Improved prompt with explicit instructions
        prompt = ChatPromptTemplate.from_template("""Extract hardware relationships from this NVIDIA research paper.

Return ONLY a JSON array. Each element must have exactly these three fields:
- "source": hardware component (string)
- "relation": type of relationship (string)  
- "target": hardware component (string)

Examples of valid relationships:
[
  {{"source": "Blackwell", "relation": "includes_architecture", "target": "Tensor_Cores"}},
  {{"source": "NVLink", "relation": "enables", "target": "GPU_GPU_Communication"}},
  {{"source": "Hopper", "relation": "predecessor_of", "target": "Blackwell"}}
]

Text to analyze:
{context}

Return ONLY the JSON array, nothing else:""")

        chain = prompt | llm
        response = chain.invoke({"context": context})
        
        raw_content = response.content.strip()
        
        print("\n=== RAW LLM OUTPUT ===")
        print(raw_content[:500])  # Print first 500 chars
        print("========================\n")

        # Try to parse the response
        relationships = parse_json_response(raw_content)
        
        print(f"✅ Extracted {len(relationships)} relationships")
        if relationships:
            print(f"Sample: {relationships[0] if relationships else 'None'}")
        
        return relationships

    except Exception as e:
        print(f"\n❌ EXTRACTION ERROR: {type(e).__name__}: {e}\n")
        import traceback
        traceback.print_exc()
        return []