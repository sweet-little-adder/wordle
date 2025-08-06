import React from 'react'

const Header = () => {
  return (
    <header className="border-b border-gray-700 bg-wordle-dark">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-center">
          <div className="flex items-center space-x-3">
            <div className="flex space-x-1">
              <div className="w-8 h-8 bg-wordle-green rounded flex items-center justify-center text-white font-bold text-lg">
                W
              </div>
              <div className="w-8 h-8 bg-wordle-yellow rounded flex items-center justify-center text-white font-bold text-lg">
                O
              </div>
              <div className="w-8 h-8 bg-wordle-gray rounded flex items-center justify-center text-white font-bold text-lg">
                R
              </div>
              <div className="w-8 h-8 bg-wordle-green rounded flex items-center justify-center text-white font-bold text-lg">
                D
              </div>
              <div className="w-8 h-8 bg-wordle-yellow rounded flex items-center justify-center text-white font-bold text-lg">
                L
              </div>
              <div className="w-8 h-8 bg-wordle-gray rounded flex items-center justify-center text-white font-bold text-lg">
                E
              </div>
            </div>
        
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header 