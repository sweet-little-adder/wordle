import React, { useState, useEffect } from 'react'
import WordleGrid from './WordleGrid'
import Keyboard from './Keyboard'
import GameOverModal from './GameOverModal'

const GameBoard = ({ gameState, onMakeGuess, gameMode }) => {
  const [currentGuess, setCurrentGuess] = useState('')
  const [showGameOver, setShowGameOver] = useState(false)
  const [showInvalidWord, setShowInvalidWord] = useState(false)
  const [shakeAnimation, setShakeAnimation] = useState(false)

  useEffect(() => {
    if (gameState.isGameOver) {
      setShowGameOver(true)
    }
  }, [gameState.isGameOver])

  const showInvalidWordFeedback = () => {
    setShowInvalidWord(true)
    setShakeAnimation(true)
    
    // Hide the tooltip after 2 seconds
    setTimeout(() => {
      setShowInvalidWord(false)
    }, 2000)
    
    // Remove shake animation after animation completes
    setTimeout(() => {
      setShakeAnimation(false)
    }, 500)
  }

  const handleGuess = (guess) => {
    const result = onMakeGuess(guess)
    
    if (result.success) {
      setCurrentGuess('')
    } else {
      // Show invalid word feedback
      showInvalidWordFeedback()
    }
  }

  const handleKeyPress = (key) => {
    if (gameState.isGameOver) return

    if (key === 'ENTER') {
      if (currentGuess.length === 5) {
        handleGuess(currentGuess)
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
        handleGuess(currentGuess)
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
  }, [currentGuess, gameState.isGameOver, onMakeGuess])

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
            {gameMode === 'server' && (
              <span>🌐 Connected to server</span>
            )}
            {gameMode === 'multiplayer' && (
              <span>👥 Multiplayer mode</span>
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
        shakeAnimation={shakeAnimation}
      />

      {/* Invalid Word Tooltip */}
      {showInvalidWord && (
        <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50">
          <div className="bg-pink-500 text-white px-4 py-2 rounded-full shadow-lg animate-bounce">
            <div className="text-center font-medium">
              Not in word list
            </div>
          </div>
        </div>
      )}

      {/* Keyboard */}
      <Keyboard
        onKeyPress={handleKeyPress}
        letterStates={gameState.letterStates || {}}
      />

      {/* Modals */}
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