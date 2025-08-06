# Wordle Game with Multiple Game Modes

A modern implementation of the popular Wordle game with multiple game modes, built with React frontend and Python backend.

## 🌟 Features

### Game Modes
- **Single Player**: Classic Wordle experience
- **Multiplayer**: Compete against other players in real-time
- **Cheating Host**: The host adapts the answer to make it harder (like Absurdle!)
- **Server/Client**: Play over the network with client-server architecture

### Technical Features
- **Modern UI**: Beautiful pinkish theme with gradients and animations
- **Word Validation**: Comprehensive 5-letter word list with API integration
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Feedback**: Visual feedback for invalid words with shake animations
- **Accessibility**: Keyboard and mouse input support

## 🚀 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sweet-little-adder/wordle
   cd wordle
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd ui/web
   npm install
   ```

4. **Start the development server**
   ```bash
   # Terminal 1: Start the frontend
   cd ui/web
   npm run dev
   
   # Terminal 2: Start the backend (optional)
   cd ../..
   python api_server.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 🛠️ Technology Stack

### Frontend
- **React 18** with Vite
- **Tailwind CSS** for styling
- **Custom hooks** for state management
- **Responsive design** with mobile-first approach

### Backend
- **Python 3.8+** with Flask
- **Multiple game modes** with extensible architecture
- **Word validation** and game logic
- **RESTful API** for server-client communication

### Development Tools
- **Pytest** for testing
- **ESLint** for code quality
- **Hot Module Replacement** for fast development

## 📁 Project Structure

```
wordle/
├── src/                    # Python backend
│   ├── core/              # Core game logic
│   ├── game_modes/        # Different game modes
│   ├── ui/                # Text-based UI
│   └── utils/             # Utility functions
├── ui/web/                # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   └── utils/         # Frontend utilities
│   └── public/            # Static assets
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🧪 Testing

### Run Python Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html
```

### Run Frontend Tests
```bash
cd ui/web
npm test
```

## 🎨 Customization

### Changing the Theme
The app uses a pinkish theme by default. To customize:

1. Edit `ui/web/tailwind.config.js` for color changes
2. Modify `ui/web/src/index.css` for styling updates

### Adding New Game Modes
1. Create a new class in `src/game_modes/`
2. Extend `BaseGameMode` class
3. Add the mode to the frontend selector

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the original Wordle game
- Built with modern web technologies
- Designed for educational purposes

---

**Enjoy playing Wordle! 🎉** 