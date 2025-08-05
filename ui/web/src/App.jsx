import React, { useState } from 'react'
import GameBoard from './components/GameBoard'
import GameModeSelector from './components/GameModeSelector'
import Header from './components/Header'
import { useGameState } from './hooks/useGameState'

function App() {
  const [gameMode, setGameMode] = useState(null)
  const { gameState, startGame, makeGuess, resetGame } = useGameState()

  const handleGameModeSelect = (mode) => {
    setGameMode(mode)
    startGame(mode)
  }

  const handleReset = () => {
    setGameMode(null)
    resetGame()
  }

  return (
    <div className="min-h-screen bg-wordle-dark">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!gameMode ? (
          <GameModeSelector onSelectMode={handleGameModeSelect} />
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold capitalize">
                {gameMode} Mode
              </h2>
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-md transition-colors"
              >
                New Game
              </button>
            </div>
            
            <GameBoard
              gameState={gameState}
              onMakeGuess={makeGuess}
              gameMode={gameMode}
            />
          </div>
        )}
      </main>
    </div>
  )
}

export default App 