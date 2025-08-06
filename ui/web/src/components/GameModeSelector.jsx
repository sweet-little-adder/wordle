import React from 'react'

const GameModeSelector = ({ onSelectMode }) => {
  const gameModes = [
    {
      id: 'single',
      title: 'Single Player',
      description: '',
      color: 'bg-pink-500 hover:bg-pink-600',
      status: 'Ready'
    },
    {
      id: 'multiplayer',
      title: 'Multiplayer',
      description: '',
      color: 'bg-pink-700 hover:bg-pink-800',
      status: 'Ready'
    },
    {
      id: 'cheating',
      title: 'Cheating Host',
      description: 'The host adapts the answer to make it harder. Like Absurdle!',
      color: 'bg-pink-600 hover:bg-pink-700',
      status: 'Ready'
    },
    {
      id: 'server',
      title: 'Server/Client',
      description: 'Play over the network with client-server architecture.',
      color: 'bg-pink-400 hover:bg-pink-500',
      status: 'Ready'
    }
  ]

  return (
    <div className="max-w-4xl mx-auto">


      <div className="flex flex-col items-center gap-4 max-w-sm mx-auto">
        {gameModes.map((mode) => (
          <div key={mode.id} className="relative group w-full flex justify-center">
            <button
              className={`w-1/2 p-4 rounded-full transition-all duration-300 hover:scale-105 ${
                mode.status === 'Coming Soon' 
                  ? 'opacity-60 cursor-not-allowed bg-gray-600' 
                  : 'cursor-pointer bg-pink-500 hover:bg-pink-600 text-white font-semibold text-lg'
              }`}
              onClick={() => mode.status === 'Ready' && onSelectMode(mode.id)}
              disabled={mode.status !== 'Ready'}
            >
              <div className="text-center">
                <h3 className="text-xl font-bold">
                  {mode.title}
                </h3>
              </div>
            </button>
            
            {/* Hover Tooltip */}
            {mode.description && (
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
                {mode.description}
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default GameModeSelector 