# NVIDIA Paper Synthesizer

A powerful application for synthesizing and analyzing NVIDIA research papers with an interactive graph-based visualization system.

## Features

- **Paper Research & Analysis**: Intelligent researcher module for extracting and analyzing paper content
- **Graph Visualization**: Interactive network graph visualization using Vis.js
- **Dynamic Data Processing**: Advanced graph engine for building and manipulating knowledge graphs
- **Web Interface**: Interactive HTML-based visualization with search and filtering capabilities
- **Streamlit App**: User-friendly web interface for easy interaction

## Project Structure

```
nvidia-paper-synthesizer/
├── main.py                    # Main application entry point
├── researcher.py              # Paper research and analysis module
├── graph_engine.py            # Graph construction and manipulation engine
├── graph.html                 # Generated graph visualization
├── requirements.txt           # Python dependencies
├── data/                      # Data storage directory
└── lib/                       # Frontend libraries
    ├── bindings/              # Custom JavaScript bindings
    ├── tom-select/            # Select UI component library
    └── vis-9.1.2/             # Vis.js network visualization library
```

## Requirements

- Python 3.8 or higher
- Streamlit
- Additional dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/nvidia-paper-synthesizer.git
   cd nvidia-paper-synthesizer
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # On Windows PowerShell
   # or
   source .venv/bin/activate   # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run main.py
   ```

2. The application will open in your default browser at `http://localhost:8501`

### Key Components

- **Graph Engine**: Processes and analyzes paper data to build knowledge graphs
- **Researcher Module**: Extracts insights and relationships from paper content
- **Visualization**: Generates interactive network graphs showing paper relationships and concepts

## How It Works

1. Input paper data or research content
2. The researcher module analyzes and extracts key information
3. The graph engine builds a knowledge graph from extracted data
4. Visualization engine renders an interactive network graph
5. Explore relationships and connections in the web interface

## Dependencies

See `requirements.txt` for the complete list of Python packages. Key dependencies include:
- `streamlit` - Web application framework
- `vis.js` - Network visualization library (included in lib/)
- `tom-select` - Enhanced select input (included in lib/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This project is designed for research and educational purposes.
