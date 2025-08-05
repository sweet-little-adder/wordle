# Wordle Web UI

A modern, responsive Wordle game interface built with React and Tailwind CSS.

## Features

- 🎮 **Multiple Game Modes**: Single Player and Cheating Host modes
- 🎨 **Beautiful UI**: Modern design with Tailwind CSS
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- ⌨️ **Virtual Keyboard**: Full keyboard support with visual feedback
- 📊 **Statistics**: Track your performance and share results
- 🎯 **Real-time Feedback**: Immediate visual feedback for guesses
- 🌙 **Dark Theme**: Easy on the eyes with dark mode

## Tech Stack

- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server
- **Custom Hooks** - Clean state management

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Navigate to the web UI directory:
```bash
cd ui/web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
ui/web/
├── src/
│   ├── components/     # React components
│   │   ├── GameBoard.jsx
│   │   ├── GameModeSelector.jsx
│   │   ├── GameOverModal.jsx
│   │   ├── GameStats.jsx
│   │   ├── Header.jsx
│   │   ├── Keyboard.jsx
│   │   └── WordleGrid.jsx
│   ├── hooks/         # Custom React hooks
│   │   └── useGameState.js
│   ├── utils/         # Utility functions
│   ├── App.jsx        # Main app component
│   ├── main.jsx       # React entry point
│   └── index.css      # Global styles
├── public/            # Static assets
├── index.html         # HTML template
├── package.json       # Dependencies and scripts
├── tailwind.config.js # Tailwind configuration
└── vite.config.js     # Vite configuration
```

## Game Modes

### Single Player
Classic Wordle experience with a randomly selected word.

### Cheating Host (Absurdle-style)
The host adapts the answer based on your guesses to make the game more challenging.

## Customization

### Colors
The game uses custom Tailwind colors defined in `tailwind.config.js`:
- `wordle-green`: #6aaa64 (correct letters)
- `wordle-yellow`: #c9b458 (present letters)
- `wordle-gray`: #787c7e (absent letters)
- `wordle-dark`: #121213 (background)

### Animations
Custom CSS animations for tile flips and keyboard interactions.

## Development

### Adding New Game Modes
1. Update the `gameModes` array in `GameModeSelector.jsx`
2. Add the mode logic in `useGameState.js`
3. Update the game state handling in `GameBoard.jsx`

### Styling
- Use Tailwind utility classes for styling
- Custom components are defined in `index.css`
- Follow the existing color scheme and design patterns

### State Management
The game state is managed through the `useGameState` hook, which provides:
- `gameState`: Current game state object
- `startGame(mode)`: Start a new game
- `makeGuess(guess)`: Submit a guess
- `resetGame()`: Reset the game

## Integration with Python Backend

This UI is designed to work with the Python backend. To integrate:

1. Start the Python backend server
2. Update the API calls in `useGameState.js` to communicate with the backend
3. Configure the proxy in `vite.config.js` for development

## Contributing

1. Follow the existing code style and patterns
2. Use Tailwind classes for styling
3. Add proper TypeScript types if converting to TypeScript
4. Test on different screen sizes
5. Ensure keyboard accessibility

## License

This project is part of the Wordle assignment and is for educational purposes. 