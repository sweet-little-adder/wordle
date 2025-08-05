import React from 'react'

const Keyboard = ({ onKeyPress, letterStates = {} }) => {
  const keyboardLayout = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'BACKSPACE']
  ]

  const getKeyClass = (key) => {
    let classes = 'keyboard-key'
    
    if (key === 'ENTER' || key === 'BACKSPACE') {
      classes += ' px-4 text-sm'
    }
    
    const state = letterStates[key]
    if (state === 'correct') {
      classes += ' correct'
    } else if (state === 'present') {
      classes += ' present'
    } else if (state === 'absent') {
      classes += ' absent'
    }
    
    return classes
  }

  const getKeyContent = (key) => {
    if (key === 'BACKSPACE') {
      return '⌫'
    }
    if (key === 'ENTER') {
      return 'Enter'
    }
    return key
  }

  return (
    <div className="space-y-2">
      {keyboardLayout.map((row, rowIndex) => (
        <div key={rowIndex} className="flex justify-center space-x-1">
          {row.map((key) => (
            <button
              key={key}
              className={getKeyClass(key)}
              onClick={() => onKeyPress(key)}
            >
              {getKeyContent(key)}
            </button>
          ))}
        </div>
      ))}
    </div>
  )
}

export default Keyboard 