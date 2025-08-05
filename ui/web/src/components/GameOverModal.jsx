import React from 'react'

const GameOverModal = ({ gameState, onClose, onPlayAgain }) => {
  const isWon = gameState.gameState === 'won'
  const answer = gameState.answer

  const generateShareText = () => {
    const emojiMap = {
      'HIT': '🟩',
      'PRESENT': '🟨',
      'MISS': '⬜'
    }

    let shareText = `Wordle ${gameState.currentRound}/6\n\n`
    
    gameState.results.forEach(result => {
      const line = result.map(r => emojiMap[r]).join('')
      shareText += line + '\n'
    })

    return shareText
  }

  const handleShare = async () => {
    const shareText = generateShareText()
    
    if (navigator.share) {
      try {
        await navigator.share({
          text: shareText
        })
      } catch (error) {
        console.log('Error sharing:', error)
      }
    } else {
      // Fallback to clipboard
      try {
        await navigator.clipboard.writeText(shareText)
        alert('Results copied to clipboard!')
      } catch (error) {
        console.log('Error copying to clipboard:', error)
      }
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <div className="text-center">
          <div className="text-6xl mb-4">
            {isWon ? '🎉' : '😔'}
          </div>
          
          <h2 className="text-2xl font-bold text-white mb-2">
            {isWon ? 'Congratulations!' : 'Game Over'}
          </h2>
          
          <p className="text-gray-300 mb-4">
            {isWon 
              ? `You got it in ${gameState.currentRound} ${gameState.currentRound === 1 ? 'try' : 'tries'}!`
              : `The word was ${answer}`
            }
          </p>

          {/* Share Results */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">Share Results</h3>
            <div className="bg-gray-700 rounded p-3 mb-3 font-mono text-sm">
              {gameState.results.map((result, index) => (
                <div key={index} className="flex justify-center space-x-1 mb-1">
                  {result.map((r, i) => (
                    <div
                      key={i}
                      className={`w-4 h-4 rounded ${
                        r === 'HIT' ? 'bg-wordle-green' :
                        r === 'PRESENT' ? 'bg-wordle-yellow' :
                        'bg-wordle-gray'
                      }`}
                    />
                  ))}
                </div>
              ))}
            </div>
            
            <button
              onClick={handleShare}
              className="px-6 py-2 bg-wordle-green hover:bg-green-600 text-white rounded-md transition-colors"
            >
              📤 Share Results
            </button>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              onClick={onPlayAgain}
              className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
            >
              Play Again
            </button>
            <button
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GameOverModal 