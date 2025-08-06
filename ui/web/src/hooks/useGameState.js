import { useState, useCallback, useEffect } from 'react'

// Function to fetch words from a reliable source
const fetchWordList = async () => {
  try {
    // Try to fetch from a reliable Wordle word list API
    const response = await fetch('https://raw.githubusercontent.com/tabatkins/wordle-list/main/words')
    if (response.ok) {
      const text = await response.text()
      const words = text.split('\n')
        .map(word => word.trim().toUpperCase())
        .filter(word => word.length === 5 && /^[A-Z]+$/.test(word))
      return words
    }
  } catch (error) {
    // Fallback to local word list
  }
  
  // Fallback: Use a comprehensive 5-letter word list
  return [
    'ABOUT', 'ABOVE', 'ABUSE', 'ACTOR', 'ACUTE', 'ADMIT', 'ADOPT', 'ADULT', 'AFTER', 'AGAIN', 'AGENT', 'AGREE',
    'AHEAD', 'ALARM', 'ALBUM', 'ALERT', 'ALIKE', 'ALIVE', 'ALLOW', 'ALONE', 'ALONG', 'ALTER', 'AMONG', 'ANGER',
    'ANGLE', 'ANGRY', 'APART', 'APPLE', 'APPLY', 'ARENA', 'ARGUE', 'ARISE', 'ARRAY', 'ASIDE', 'ASSET', 'AUDIO',
    'AUDIT', 'AVOID', 'AWARD', 'AWARE', 'BADLY', 'BAKER', 'BASES', 'BASIC', 'BASIS', 'BEACH', 'BEGAN', 'BEGIN',
    'BEING', 'BELOW', 'BENCH', 'BILLY', 'BIRTH', 'BLACK', 'BLAME', 'BLIND', 'BLOCK', 'BLOOD', 'BOARD', 'BOOST',
    'BOOTH', 'BOUND', 'BRAIN', 'BRAND', 'BREAD', 'BREAK', 'BREED', 'BRIEF', 'BRING', 'BROAD', 'BROKE', 'BROWN',
    'BUILD', 'BUILT', 'BUYER', 'CABLE', 'CALIF', 'CARRY', 'CATCH', 'CAUSE', 'CHAIN', 'CHAIR', 'CHART', 'CHASE',
    'CHEAP', 'CHECK', 'CHEST', 'CHIEF', 'CHILD', 'CHINA', 'CHOSE', 'CIVIL', 'CLAIM', 'CLASS', 'CLEAN', 'CLEAR',
    'CLICK', 'CLIMB', 'CLOCK', 'CLOSE', 'COACH', 'COAST', 'COULD', 'COUNT', 'COURT', 'COVER', 'CRAFT', 'CRASH',
    'CREAM', 'CRIME', 'CROSS', 'CROWD', 'CROWN', 'CURVE', 'CYCLE', 'DAILY', 'DANCE', 'DATED', 'DEALT', 'DEATH',
    'DEBUT', 'DELAY', 'DEPTH', 'DOING', 'DOUBT', 'DOZEN', 'DRAFT', 'DRAMA', 'DRAWN', 'DREAM', 'DRESS', 'DRINK',
    'DRIVE', 'DROVE', 'DYING', 'EAGER', 'EARLY', 'EARTH', 'EIGHT', 'ELITE', 'EMPTY', 'ENEMY', 'ENJOY', 'ENTER',
    'ENTRY', 'EQUAL', 'ERROR', 'EVENT', 'EVERY', 'EXACT', 'EXIST', 'EXTRA', 'FAITH', 'FALSE', 'FAULT', 'FIBER',
    'FIELD', 'FIFTH', 'FIFTY', 'FIGHT', 'FINAL', 'FIRST', 'FIXED', 'FLASH', 'FLEET', 'FLOOR', 'FLUID', 'FOCUS',
    'FORCE', 'FORTH', 'FORTY', 'FORUM', 'FOUND', 'FRAME', 'FRANK', 'FRAUD', 'FRESH', 'FRONT', 'FRUIT', 'FULLY',
    'FUNNY', 'GIANT', 'GIVEN', 'GLASS', 'GLOBE', 'GOING', 'GRACE', 'GRADE', 'GRAND', 'GRANT', 'GRASS', 'GRAVE',
    'GREAT', 'GREEN', 'GROSS', 'GROUP', 'GROWN', 'GUARD', 'GUESS', 'GUEST', 'GUIDE', 'HARRY', 'HEAVY', 'HENCE',
    'HENRY', 'HORSE', 'HOTEL', 'HOUSE', 'HUMAN', 'IDEAL', 'IMAGE', 'INDEX', 'INNER', 'ISSUE', 'JAPAN', 'JIMMY',
    'JOINT', 'JONES', 'JUDGE', 'KNOWN', 'LABEL', 'LARGE', 'LASER', 'LATER', 'LAUGH', 'LAYER', 'LEARN', 'LEASE',
    'LEAST', 'LEAVE', 'LEGAL', 'LEWIS', 'LIMIT', 'LINKS', 'LIVES', 'LOCAL', 'LOOSE', 'LOWER', 'LUCKY', 'LUNCH',
    'LYING', 'MAGIC', 'MAJOR', 'MAKER', 'MARCH', 'MARIA', 'MAYBE', 'MAYOR', 'MEDIA', 'METAL', 'MIGHT', 'MINOR',
    'MINUS', 'MIXED', 'MODEL', 'MONEY', 'MONTH', 'MORAL', 'MOTOR', 'MOUNT', 'MOUSE', 'MOUTH', 'MOVED', 'NEEDS',
    'NEVER', 'NEWLY', 'NIGHT', 'NOISE', 'NORTH', 'NOTED', 'NOVEL', 'NURSE', 'OCCUR', 'OCEAN', 'OFFER', 'OFFIC',
    'ORDER', 'OTHER', 'OUGHT', 'PAINT', 'PANEL', 'PAPER', 'PETER', 'PHASE', 'PHONE', 'PHOTO', 'PIECE', 'PILOT',
    'PITCH', 'PLACE', 'PLAIN', 'PLANE', 'PLANT', 'PLATE', 'POUND', 'PRESS', 'PRICE', 'PRIDE', 'PRIME', 'PRINT',
    'PRIOR', 'PRIZE', 'PROOF', 'PROUD', 'PROVE', 'QUEEN', 'QUICK', 'QUIET', 'QUITE', 'RADIO', 'RAISE', 'RANGE',
    'RAPID', 'RATIO', 'REACH', 'READY', 'REALM', 'REBEL', 'REFER', 'RELAX', 'REPLY', 'RIVAL', 'ROBIN', 'ROGER',
    'ROMAN', 'ROUGH', 'ROUTE', 'ROYAL', 'RURAL', 'SADLY', 'SAFER', 'SALLY', 'SALON', 'SAUCE', 'SCALE', 'SCENE',
    'SCOPE', 'SCORE', 'SENSE', 'SEVEN', 'SHALL', 'SHAPE', 'SHARE', 'SHARP', 'SHEET', 'SHELF', 'SHELL', 'SHIFT',
    'SHIRT', 'SHOCK', 'SHOOT', 'SHOWN', 'SIGHT', 'SINCE', 'SIXTH', 'SIXTY', 'SIZED', 'SKILL', 'SLEEP', 'SLIDE',
    'SMART', 'SMITH', 'SMOKE', 'SORRY', 'SOUTH', 'SPEAK', 'SPEED', 'SPEND', 'SPENT', 'SPLIT', 'SPORT', 'STAFF',
    'STAGE', 'STAKE', 'STAND', 'STEAM', 'STEEL', 'STEEP', 'STEER', 'STEMS', 'STEPS', 'STICK', 'STILL', 'STOCK',
    'STONE', 'STOOD', 'STORE', 'STORM', 'STORY', 'STUCK', 'STUDY', 'STUFF', 'SUGAR', 'SUITE', 'SUPER', 'SWEET',
    'TABLE', 'TAKEN', 'TASTE', 'TAXES', 'TEACH', 'TEETH', 'TERRY', 'TEXAS', 'THANK', 'THEFT', 'THEIR', 'THEME',
    'THERE', 'THESE', 'THICK', 'THING', 'THINK', 'THIRD', 'THOSE', 'THREE', 'THREW', 'THROW', 'THUMB', 'TIGER',
    'TIGHT', 'TIMER', 'TIRED', 'TITLE', 'TOPIC', 'TOTAL', 'TOUCH', 'TOUGH', 'TOWER', 'TRACK', 'TRADE', 'TRAIN',
    'TREAT', 'TREND', 'TRIAL', 'TRIBE', 'TRICK', 'TRIED', 'TRIES', 'TRUCK', 'TRULY', 'TRUNK', 'TRUST', 'TRUTH',
    'TWICE', 'UNDER', 'UNDUE', 'UNION', 'UNITY', 'UNTIL', 'UPPER', 'UPSET', 'URBAN', 'USAGE', 'USUAL', 'VALID',
    'VALUE', 'VIDEO', 'VIRUS', 'VISIT', 'VITAL', 'WASTE', 'WATCH', 'WHEEL', 'WHILE', 'WHITE', 'WHOLE', 'WHOSE',
    'WOMEN', 'WORRY', 'WORSE', 'WORST', 'WORTH', 'WOUND', 'WRITE', 'WRONG', 'WROTE'
  ]
}

// Global word list state
let DEFAULT_WORDS = []
let isWordListLoaded = false

// Simple game logic for demo (in a real app, this would communicate with the Python backend)
const calculateResult = (guess, answer) => {
  const result = ['MISS', 'MISS', 'MISS', 'MISS', 'MISS']
  const answerLetters = answer.split('')
  const guessLetters = guess.split('')
  
  // First pass: mark hits
  for (let i = 0; i < 5; i++) {
    if (guessLetters[i] === answerLetters[i]) {
      result[i] = 'HIT'
      answerLetters[i] = null
      guessLetters[i] = null
    }
  }
  
  // Second pass: mark presents
  for (let i = 0; i < 5; i++) {
    if (guessLetters[i] !== null) {
      const index = answerLetters.indexOf(guessLetters[i])
      if (index !== -1) {
        result[i] = 'PRESENT'
        answerLetters[index] = null
      }
    }
  }
  
  return result
}

export const useGameState = () => {
  const [gameState, setGameState] = useState({
    gameState: 'waiting',
    currentRound: 0,
    maxRounds: 6,
    remainingRounds: 6,
    guesses: [],
    results: [],
    answer: null,
    isGameOver: false,
    letterStates: {},
    candidatesRemaining: null,
    gameMode: null
  })

  const [currentAnswer, setCurrentAnswer] = useState(null)
  const [candidateWords, setCandidateWords] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  // Load word list on component mount
  useEffect(() => {
    const loadWordList = async () => {
      if (!isWordListLoaded) {
        DEFAULT_WORDS = await fetchWordList()
        isWordListLoaded = true
      }
      setCandidateWords([...DEFAULT_WORDS])
      setIsLoading(false)
    }
    
    loadWordList()
  }, [])

  const startGame = useCallback((mode) => {
    let answer
    if (mode === 'cheating') {
      // For cheating mode, we'll determine the answer after the first guess
      answer = null
    } else if (mode === 'server') {
      // For server mode, we'll use a simple implementation for now
      answer = DEFAULT_WORDS[Math.floor(Math.random() * DEFAULT_WORDS.length)]
    } else if (mode === 'multiplayer') {
      // For multiplayer mode, we'll use a simple implementation for now
      answer = DEFAULT_WORDS[Math.floor(Math.random() * DEFAULT_WORDS.length)]
    } else {
      // For single player, pick a random word
      answer = DEFAULT_WORDS[Math.floor(Math.random() * DEFAULT_WORDS.length)]
    }

    setCurrentAnswer(answer)
    setCandidateWords([...DEFAULT_WORDS])
    
    setGameState({
      gameState: 'playing',
      currentRound: 0,
      maxRounds: 6,
      remainingRounds: 6,
      guesses: [],
      results: [],
      answer: null,
      isGameOver: false,
      letterStates: {},
      candidatesRemaining: mode === 'cheating' ? DEFAULT_WORDS.length : null,
      gameMode: mode
    })
  }, [])

  const makeGuess = useCallback((guess) => {
    const upperGuess = guess.toUpperCase()
    
    // Check if word list is loaded
    if (DEFAULT_WORDS.length === 0) {
      return { success: false, error: 'Word list not loaded yet' }
    }
    
    // Validate guess
    if (!DEFAULT_WORDS.includes(upperGuess)) {
      return { success: false, error: 'Not in word list' }
    }

    let result
    let answer = currentAnswer
    
    if (gameState.gameState === 'cheating' && currentAnswer === null) {
      // This is the first guess in cheating mode
      // Find the worst possible result
      let worstScore = -1
      let worstResult = null
      let worstAnswer = null

      for (const candidate of candidateWords) {
        const candidateResult = calculateResult(upperGuess, candidate)
        const score = candidateResult.filter(r => r === 'HIT').length * 10 + 
                     candidateResult.filter(r => r === 'PRESENT').length
        
        if (score < worstScore || worstScore === -1) {
          worstScore = score
          worstResult = candidateResult
          worstAnswer = candidate
        }
      }

      result = worstResult
      answer = worstAnswer
      setCurrentAnswer(worstAnswer)
      
      // Filter candidates
      const newCandidates = candidateWords.filter(word => {
        const wordResult = calculateResult(upperGuess, word)
        return wordResult.every((r, i) => r === worstResult[i])
      })
      setCandidateWords(newCandidates)
    } else if (gameState.gameMode === 'server') {
      // Server mode - simulate network communication
      result = calculateResult(upperGuess, answer)
    } else if (gameState.gameMode === 'multiplayer') {
      // Multiplayer mode - simulate multiple players
      result = calculateResult(upperGuess, answer)
    } else {
      result = calculateResult(upperGuess, answer)
    }

    const newRound = gameState.currentRound + 1
    const isCorrect = upperGuess === answer
    const isGameOver = isCorrect || newRound >= gameState.maxRounds

    // Update letter states
    const newLetterStates = { ...gameState.letterStates }
    upperGuess.split('').forEach((letter, index) => {
      const currentState = newLetterStates[letter]
      const newState = result[index]
      
      // Only upgrade the state (correct > present > absent)
      if (!currentState || 
          (newState === 'HIT' && currentState !== 'HIT') ||
          (newState === 'PRESENT' && currentState === 'MISS')) {
        newLetterStates[letter] = newState.toLowerCase()
      }
    })

    const newGameState = {
      ...gameState,
      currentRound: newRound,
      remainingRounds: Math.max(0, gameState.maxRounds - newRound),
      guesses: [...gameState.guesses, upperGuess],
      results: [...gameState.results, result],
      answer: isGameOver ? answer : null,
      isGameOver,
      letterStates: newLetterStates,
      candidatesRemaining: gameState.candidatesRemaining ? candidateWords.length : null
    }

    if (isCorrect) {
      newGameState.gameState = 'won'
    } else if (isGameOver) {
      newGameState.gameState = 'lost'
    }

    setGameState(newGameState)

    return { success: true, result, isCorrect }
  }, [gameState, currentAnswer, candidateWords])

  const resetGame = useCallback(() => {
    setGameState({
      gameState: 'playing',
      currentRound: 0,
      maxRounds: 6,
      remainingRounds: 6,
      guesses: [],
      results: [],
      answer: null,
      isGameOver: false,
      letterStates: {},
      candidatesRemaining: null
    })
    setCurrentAnswer(null)
    setCandidateWords([...DEFAULT_WORDS])
  }, [])

  return {
    gameState,
    startGame,
    makeGuess,
    resetGame,
    isLoading,
    wordListSize: DEFAULT_WORDS.length
  }
} 