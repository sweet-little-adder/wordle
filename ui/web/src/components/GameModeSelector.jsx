import React from 'react'

const GameModeSelector = ({ onSelectMode }) => {
  const gameModes = [
    {
      id: 'single',
      title: 'Single Player',
      description: 'Classic Wordle experience. Guess the word in 6 tries.',
      icon: '🎯',
      color: 'bg-blue-600 hover:bg-blue-700',
      status: 'Ready'
    },
    {
      id: 'cheating',
      title: 'Cheating Host',
      description: 'The host adapts the answer to make it harder. Like Absurdle!',
      icon: '😈',
      color: 'bg-red-600 hover:bg-red-700',
      status: 'Ready'
    },
    {
      id: 'server',
      title: 'Server/Client',
      description: 'Play over the network with client-server architecture.',
      icon: '🌐',
      color: 'bg-green-600 hover:bg-green-700',
      status: 'Coming Soon'
    },
    {
      id: 'multiplayer',
      title: 'Multiplayer',
      description: 'Compete against other players in real-time.',
      icon: '👥',
      color: 'bg-purple-600 hover:bg-purple-700',
      status: 'Coming Soon'
    }
  ]

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-white mb-4">
          Choose Your Game Mode
        </h2>
        <p className="text-gray-300 text-lg">
          Select from different Wordle game modes and challenges
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {gameModes.map((mode) => (
          <div
            key={mode.id}
            className={`relative bg-gray-800 rounded-lg p-6 border border-gray-700 transition-all duration-300 hover:scale-105 ${
              mode.status === 'Coming Soon' ? 'opacity-60 cursor-not-allowed' : 'cursor-pointer hover:border-gray-500'
            }`}
            onClick={() => mode.status === 'Ready' && onSelectMode(mode.id)}
          >
            <div className="flex items-start space-x-4">
              <div className="text-4xl">{mode.icon}</div>
              <div className="flex-1">
                <h3 className="text-xl font-semibold text-white mb-2">
                  {mode.title}
                </h3>
                <p className="text-gray-300 mb-4">
                  {mode.description}
                </p>
                <div className="flex items-center justify-between">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    mode.status === 'Ready' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {mode.status}
                  </span>
                  {mode.status === 'Ready' && (
                    <button
                      className={`px-4 py-2 rounded-md text-white font-medium transition-colors ${mode.color}`}
                    >
                      Play Now
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-12 text-center">
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h3 className="text-xl font-semibold text-white mb-3">
            🎮 How to Play
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-300">
            <div>
              <div className="font-semibold text-white mb-2">Guess the Word</div>
              <p>Enter a 5-letter word and press Enter</p>
            </div>
            <div>
              <div className="font-semibold text-white mb-2">Get Feedback</div>
              <p>Green = correct letter & position<br/>
                 Yellow = correct letter, wrong position<br/>
                 Gray = letter not in word</p>
            </div>
            <div>
              <div className="font-semibold text-white mb-2">Win or Lose</div>
              <p>Guess correctly within 6 tries to win!</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GameModeSelector 