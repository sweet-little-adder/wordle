# Wordle Project

A comprehensive implementation of the Wordle game with support for multiple game modes and features.

## Assignment Overview

This project implements a Wordle game with the following tasks:

1. **Task 1: Normal Wordle** - Basic Wordle game with configurable settings
2. **Task 2: Server/Client Wordle** - Network-based Wordle with client-server architecture
3. **Task 3: Host Cheating Wordle** - Absurdle-style cheating host that adapts answers
4. **Task 4: Multi-player Wordle** - Multiplayer version with player interaction

## Features

### Core Features
- 5-letter word guessing game
- Configurable word list and maximum rounds
- Hit/Present/Miss scoring system
- Win/lose condition detection
- Clean, modular architecture

### Game Modes
- **Single Player**: Classic Wordle experience
- **Server/Client**: Network-based gameplay
- **Cheating Host**: Host adapts answers based on player guesses
- **Multiplayer**: Multiple players competing

## Project Structure

```
wordle/
├── src/
│   ├── core/           # Core game logic
│   ├── game_modes/     # Different game implementations
│   ├── utils/          # Utility functions
│   └── config/         # Configuration files
├── ui/
│   └── web/            # React + Tailwind CSS web interface
├── data/               # Word lists and game data
├── tests/              # Unit tests
├── docs/               # Documentation
└── examples/           # Example usage and demonstrations
```

## Requirements

### Python Backend
- Python 3.8+
- No external dependencies for basic functionality
- Optional: `flask` for server/client mode

### Web Interface
- Node.js 16+
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd wordle
```

2. Install Python dependencies (optional):
```bash
pip install -r requirements.txt
```

3. Install web interface dependencies:
```bash
cd ui/web
npm install
```

## Usage

### Web Interface (Recommended)
The project includes a modern React web interface with Tailwind CSS:

```bash
# Navigate to the web UI directory
cd ui/web

# Install dependencies
npm install

# Start the development server
npm run dev
```

Then open your browser to `http://localhost:3000` to play the game with a beautiful, responsive interface.

### Command Line Interface

#### Task 1: Normal Wordle
```bash
python src/main.py --mode single
```

#### Task 2: Server/Client Wordle
```bash
# Start server
python src/main.py --mode server --port 8080

# Start client
python src/main.py --mode client --host localhost --port 8080
```

#### Task 3: Cheating Host Wordle
```bash
python src/main.py --mode cheating
```

#### Task 4: Multiplayer Wordle
```bash
python src/main.py --mode multiplayer --players 2
```

## Configuration

The game can be configured through:
- Command line arguments
- Configuration files in `src/config/`
- Environment variables

### Key Configuration Options
- `max_rounds`: Maximum number of guessing rounds (default: 6)
- `word_list`: Path to word list file
- `server_port`: Port for server/client mode
- `players`: Number of players for multiplayer mode

## Game Rules

### Scoring System
- **Hit (Green)**: Letter is in the correct position
- **Present (Yellow)**: Letter is in the word but wrong position
- **Miss (Gray)**: Letter is not in the word

### Win Conditions
- **Single Player**: Guess the word within max rounds
- **Multiplayer**: First player to guess correctly, or best score after max rounds
- **Cheating Host**: Same as single player, but host adapts answers

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines.

## Architecture Decisions

### Design Patterns
- **Strategy Pattern**: Different game modes implement the same interface
- **Factory Pattern**: Game mode creation based on configuration
- **Observer Pattern**: For multiplayer game state updates

### Trade-offs Made
1. **Language Choice**: Python for rapid development and readability
2. **Architecture**: Modular design for easy extension
3. **Dependencies**: Minimal external dependencies for portability
4. **UI**: Text-based interface for simplicity and cross-platform compatibility

## Documentation

- `docs/architecture.md`: Detailed architecture documentation
- `docs/api.md`: API documentation for server/client mode
- `docs/game_modes.md`: Detailed explanation of each game mode

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is created for educational purposes as part of a programming assignment. 