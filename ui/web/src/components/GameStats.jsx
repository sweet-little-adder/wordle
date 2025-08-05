import React from 'react'

const GameStats = ({ gameState, onClose }) => {
  const stats = {
    gamesPlayed: 1,
    gamesWon: gameState.gameState === 'won' ? 1 : 0,
    currentStreak: gameState.gameState === 'won' ? 1 : 0,
    maxStreak: gameState.gameState === 'won' ? 1 : 0,
    guessDistribution: {
      1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0
    }
  }

  if (gameState.gameState === 'won') {
    stats.guessDistribution[gameState.currentRound] = 1
  }

  const winRate = stats.gamesPlayed > 0 ? Math.round((stats.gamesWon / stats.gamesPlayed) * 100) : 0

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-white">Statistics</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white text-2xl"
          >
            ×
          </button>
        </div>

        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{stats.gamesPlayed}</div>
            <div className="text-sm text-gray-300">Played</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{winRate}%</div>
            <div className="text-sm text-gray-300">Win Rate</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{stats.currentStreak}</div>
            <div className="text-sm text-gray-300">Current Streak</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-white">{stats.maxStreak}</div>
            <div className="text-sm text-gray-300">Max Streak</div>
          </div>
        </div>

        <div className="mb-4">
          <h3 className="text-lg font-semibold text-white mb-2">Guess Distribution</h3>
          {Object.entries(stats.guessDistribution).map(([guess, count]) => (
            <div key={guess} className="flex items-center mb-1">
              <span className="text-sm text-gray-300 w-4">{guess}</span>
              <div className="flex-1 bg-gray-700 rounded h-4 mx-2 relative">
                {count > 0 && (
                  <div 
                    className="bg-wordle-green h-full rounded"
                    style={{ width: `${Math.max(count * 20, 10)}%` }}
                  />
                )}
              </div>
              <span className="text-sm text-gray-300 w-8 text-right">{count}</span>
            </div>
          ))}
        </div>

        <div className="text-center">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-wordle-green hover:bg-green-600 text-white rounded-md transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  )
}

export default GameStats 