# Local AI Assistant

A local AI assistant designed to help with day-to-day tasks without relying on cloud services, prioritizing privacy and customizability.

## Project Overview

This project aims to create a privacy-focused AI assistant that runs entirely on local hardware (specifically optimized for MacBook). The assistant will provide:

- Voice and text communication
- Step-by-step reasoning capabilities
- Customizable knowledge base
- Inter-agent connectivity
- Web search functionality
- Specialized modes for different tasks

## Tech Stack

### Backend
- **Flask**: Lightweight web framework
- **LLama.cpp/llama-cpp-python**: For running optimized local language models
- **SpeechRecognition**: Python library for speech-to-text
- **pyttsx3/gTTS**: For text-to-speech capabilities
- **SQLite**: Lightweight database for knowledge storage
- **Socket.IO**: For real-time communication between agents
- **Requests/BeautifulSoup**: For web scraping and search capabilities

### Frontend
- **HTML5/CSS3**: For UI structure and styling
- **Bootstrap**: Responsive design components
- **JavaScript**: Frontend interactivity
- **Web Speech API**: Browser-based voice recognition/synthesis
- **Socket.IO Client**: Real-time connections
- **Marked.js**: Rendering markdown in chat responses

## Implementation Plan

### Phase 1: Core Local AI Setup
- Set up Flask application structure
- Integrate local language model
- Build basic chat interface with mode switching

### Phase 2: Voice Integration & Knowledge Base
- Implement speech processing (input/output)
- Create knowledge base system
- Add reasoning capability visualization

### Phase 3: Connectivity Features
- Web search integration
- Inter-agent communication
- Agent connection manager UI

### Phase 4: Testing & Refinement
- Comprehensive testing on different hardware profiles
- Optimize memory usage and response time
- Final UI polish and documentation

## Setup Instructions

### Folder Structure:

```md
local-ai-assistant/
│
├── app.py                      # Main application entry point
├── config.py                   # Configuration settings
├── .env                        # Environment variables (git ignored)
├── requirements.txt            # Dependencies list
├── setup.py                    # First-time setup script
│
├── static/                     # Static files
│   ├── css/                    # Stylesheets
│   │   └── style.css           # Main stylesheet
│   ├── js/                     # JavaScript files
│   │   ├── chat.js             # Chat interface logic
│   │   ├── voice.js            # Voice processing logic
│   │   └── agent-manager.js    # Agent communication logic
│   ├── img/                    # Image assets
│   └── models/                 # LLM model files (git ignored)
│
├── templates/                  # Jinja2 templates
│   ├── base.html               # Base template with common elements
│   ├── index.html              # Main chat interface
│   ├── settings.html           # Settings page
│   └── agent_manager.html      # Agent connection management interface
│
├── core/                       # Core application modules
│   ├── __init__.py             # Package initializer
│   ├── model_manager.py        # LLM model loading and inference
│   ├── chat_processor.py       # Processes chat messages
│   └── mode_handler.py         # Handles different assistant modes
│
├── features/                   # Feature-specific modules
│   ├── __init__.py             # Package initializer
│   ├── voice/                  # Voice processing
│   │   ├── __init__.py
│   │   ├── speech_recognition.py
│   │   └── text_to_speech.py
│   ├── knowledge/              # Knowledge base
│   │   ├── __init__.py
│   │   ├── database.py         # Database connection and queries
│   │   ├── schema.py           # Database schema
│   │   └── manager.py          # Knowledge management
│   └── connectivity/           # Connectivity features
│       ├── __init__.py
│       ├── search.py           # Web search implementat  ion
│       ├── agent_discovery.py  # Finds other agents on network
│       └── socket_manager.py   # Handles agent communication
│
├── api/                        # API endpoints
│   ├── __init__.py             # Package initializer
│   ├── routes.py               # API route definitions
│   ├── chat.py                 # Chat API handlers
│   └── knowledge.py            # Knowledge base API handlers
│
├── utils/                      # Utility functions
│   ├── __init__.py             # Package initializer
│   ├── security.py             # Security-related utilities
│   ├── caching.py              # Response caching
│   └── logger.py               # Custom logging
│
└── tests/                      # Test files
    ├── __init__.py             # Package initializer
    ├── test_model.py           # Model tests
    ├── test_chat.py            # Chat functionality tests
    ├── test_voice.py           # Voice feature tests
    └── test_knowledge.py       # Knowledge base tests
```

(Coming soon)

### Running the Local AI Assistant Project

To start running this local AI assistant project, follow these steps:

Step 1: Set Up the Environment
First, install the required Python dependencies:

Step 2: Run the Setup Script
The project includes a setup script that will:

Create a .env file with default settings
Set up the model directory
Initialize the SQLite database
Download the LLM model (optional)
Run the setup script:

When prompted, choose whether to download the model. The setup will download the Mistral 7B Instruct model (approximately 4GB) if you answer 'y'.

Step 3: Start the Application
After completing the setup, start the Flask application:

The application will be available at http://127.0.0.1:3000/ by default.

Step 4: Access the Web Interface
Open your web browser and navigate to:

http://127.0.0.1:3000/
You'll see the chat interface where you can interact with the AI assistant.

## Technical Considerations

- **Model Selection**: Using quantized models (GGUF format) for better performance on MacBook hardware
- **Memory Management**: Dynamic loading/unloading of model components
- **Privacy**: All data remains local by default
- **Performance**: Implementing caching and batched processing
- **Extensibility**: Plugin architecture for future capabilities

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.