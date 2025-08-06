import React, { useState } from 'react'
import GameBoard from './components/GameBoard'
import GameModeSelector from './components/GameModeSelector'
import Header from './components/Header'
import { useGameState } from './hooks/useGameState'

function App() {
  const [gameMode, setGameMode] = useState(null)
  const { gameState, startGame, makeGuess, resetGame, isLoading, wordListSize } = useGameState()

  const handleGameModeSelect = (mode) => {
    setGameMode(mode)
    startGame(mode)
  }

  const handleReset = () => {
    setGameMode(null)
    resetGame()
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-wordle-dark flex items-center justify-center">
        <div className="text-center">
          <div className="text-2xl text-white mb-4">Loading Wordle...</div>
          <div className="text-gray-300">Fetching word list from API</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-wordle-dark">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {!gameMode ? (
          <div>
            <GameModeSelector onSelectMode={handleGameModeSelect} />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold capitalize">
                {gameMode} Mode
              </h2>
              <button
                onClick={handleReset}
                className="px-4 py-2 bg-pink-600 hover:bg-pink-700 rounded-md transition-colors"
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