import React from 'react'

const WordleGrid = ({ guesses, results, currentGuess, maxRounds, shakeAnimation = false }) => {
  const getTileClass = (row, col, letter, result) => {
    let classes = 'wordle-tile'
    
    if (letter) {
      classes += ' filled'
      
      if (result) {
        if (result === 'HIT') classes += ' correct'
        else if (result === 'PRESENT') classes += ' present'
        else if (result === 'MISS') classes += ' absent'
      }
    }
    
    return classes
  }

  const getTileContent = (row, col) => {
    if (row < guesses.length) {
      return guesses[row][col] || ''
    } else if (row === guesses.length) {
      return currentGuess[col] || ''
    }
    return ''
  }

  const getTileResult = (row, col) => {
    if (row < results.length && results[row]) {
      return results[row][col]
    }
    return null
  }

  return (
    <div className="flex justify-center">
      <div className="grid grid-rows-6 gap-2">
        {Array.from({ length: maxRounds }, (_, row) => {
          const isCurrentRow = row === guesses.length
          const shouldShake = shakeAnimation && isCurrentRow
          
          return (
            <div key={row} className={`grid grid-cols-5 gap-2 ${shouldShake ? 'animate-shake' : ''}`}>
              {Array.from({ length: 5 }, (_, col) => {
                const letter = getTileContent(row, col)
                const result = getTileResult(row, col)
                
                return (
                  <div
                    key={`${row}-${col}`}
                    className={getTileClass(row, col, letter, result)}
                    style={{
                      animationDelay: `${(row * 5 + col) * 0.1}s`
                    }}
                  >
                    {letter}
                  </div>
                )
              })}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default WordleGrid 