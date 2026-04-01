import streamlit as st
import os
import streamlit.components.v1 as components
from researcher import analyze_paper
# Note: Ensure graph_engine.py is in the same folder
try:
    from graph_engine import create_knowledge_graph
except ImportError:
    # Fallback if graph_engine isn't ready yet
    def create_knowledge_graph(data): return None

st.set_page_config(page_title="NVIDIA Research Synthesizer", layout="wide")

st.title("🌲 NVIDIA Research Synthesizer")
st.info("Extracting System Architectures using NVIDIA NIM (Llama-3.1-Nemotron)")

# Setup data directory
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

uploaded_file = st.file_uploader("Upload NVIDIA Research Paper (PDF)", type="pdf")

if uploaded_file:
    file_path = os.path.join(DATA_DIR, uploaded_file.name)
    
    # Save the file locally
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("Analyzing GPU Architectures..."):
        entities = analyze_paper(file_path)
        
        if entities and len(entities) > 0:
            st.success(f"Found {len(entities)} technical relationships!")
            
            # Create and Display Graph
            graph_path = create_knowledge_graph(entities)
            if graph_path and os.path.exists(graph_path):
                st.subheader("Architectural Knowledge Graph")
                with open(graph_path, 'r', encoding='utf-8') as f:
                    components.html(f.read(), height=600, scrolling=True)
            
            # Display Table
            st.subheader("Extracted Insights")
            st.table(entities)
        else:
            st.warning("No specific hardware relationships were extracted. Try a different paper!")