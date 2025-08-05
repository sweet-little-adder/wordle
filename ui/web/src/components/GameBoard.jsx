import React, { useState, useEffect } from 'react'
import WordleGrid from './WordleGrid'
import Keyboard from './Keyboard'
import GameStats from './GameStats'
import GameOverModal from './GameOverModal'

const GameBoard = ({ gameState, onMakeGuess, gameMode }) => {
  const [currentGuess, setCurrentGuess] = useState('')
  const [showStats, setShowStats] = useState(false)
  const [showGameOver, setShowGameOver] = useState(false)

  useEffect(() => {
    if (gameState.isGameOver) {
      setShowGameOver(true)
    }
  }, [gameState.isGameOver])

  const handleKeyPress = (key) => {
    if (gameState.isGameOver) return

    if (key === 'ENTER') {
      if (currentGuess.length === 5) {
        const result = onMakeGuess(currentGuess)
        if (result.success) {
          setCurrentGuess('')
        }
      }
    } else if (key === 'BACKSPACE') {
      setCurrentGuess(prev => prev.slice(0, -1))
    } else if (currentGuess.length < 5) {
      setCurrentGuess(prev => prev + key)
    }
  }

  const handleKeyDown = (e) => {
    if (gameState.isGameOver) return

    const key = e.key.toUpperCase()
    
    if (key === 'ENTER') {
      e.preventDefault()
      if (currentGuess.length === 5) {
        const result = onMakeGuess(currentGuess)
        if (result.success) {
          setCurrentGuess('')
        }
      }
    } else if (key === 'BACKSPACE') {
      e.preventDefault()
      setCurrentGuess(prev => prev.slice(0, -1))
    } else if (/^[A-Z]$/.test(key) && currentGuess.length < 5) {
      e.preventDefault()
      setCurrentGuess(prev => prev + key)
    }
  }

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [currentGuess, gameState.isGameOver])

  return (
    <div className="max-w-md mx-auto space-y-8">
      {/* Game Info */}
      <div className="text-center">
        <div className="flex justify-between items-center mb-4">
          <div className="text-sm text-gray-300">
            Round {gameState.currentRound}/{gameState.maxRounds}
          </div>
          <div className="text-sm text-gray-300">
            {gameMode === 'cheating' && gameState.candidatesRemaining && (
              <span>🎯 {gameState.candidatesRemaining} candidates</span>
            )}
          </div>
        </div>
      </div>

      {/* Wordle Grid */}
      <WordleGrid
        guesses={gameState.guesses}
        results={gameState.results}
        currentGuess={currentGuess}
        maxRounds={gameState.maxRounds}
      />

      {/* Game Stats Button */}
      <div className="text-center">
        <button
          onClick={() => setShowStats(true)}
          className="px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded-md transition-colors text-sm"
        >
          📊 View Stats
        </button>
      </div>

      {/* Keyboard */}
      <Keyboard
        onKeyPress={handleKeyPress}
        letterStates={gameState.letterStates || {}}
      />

      {/* Modals */}
      {showStats && (
        <GameStats
          gameState={gameState}
          onClose={() => setShowStats(false)}
        />
      )}

      {showGameOver && (
        <GameOverModal
          gameState={gameState}
          onClose={() => setShowGameOver(false)}
          onPlayAgain={() => {
            setShowGameOver(false)
            // Reset game logic would go here
          }}
        />
      )}
    </div>
  )
}

export default GameBoard 