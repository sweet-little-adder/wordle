import { useState, useCallback } from 'react'

// Default word list for demo purposes
const DEFAULT_WORDS = [
  'ABOUT', 'ABOVE', 'ABUSE', 'ACTOR', 'ACUTE', 'ADMIT', 'ADOPT', 'ADULT',
  'AFTER', 'AGAIN', 'AGENT', 'AGREE', 'AHEAD', 'ALARM', 'ALBUM', 'ALERT',
  'ALIKE', 'ALIVE', 'ALLOW', 'ALONE', 'ALONG', 'ALTER', 'AMONG', 'ANGER',
  'ANGLE', 'ANGRY', 'APART', 'APPLE', 'APPLY', 'ARENA', 'ARGUE', 'ARISE',
  'ARRAY', 'ASIDE', 'ASSET', 'AUDIO', 'AUDIT', 'AVOID', 'AWARD', 'AWARE',
  'BADLY', 'BAKER', 'BASES', 'BASIC', 'BASIS', 'BEACH', 'BEGAN', 'BEGIN',
  'BEING', 'BELOW', 'BENCH', 'BILLY', 'BIRTH', 'BLACK', 'BLAME', 'BLIND',
  'BLOCK', 'BLOOD', 'BOARD', 'BOOST', 'BOOTH', 'BOUND', 'BRAIN', 'BRAND',
  'BREAD', 'BREAK', 'BREED', 'BRIEF', 'BRING', 'BROAD', 'BROKE', 'BROWN',
  'BUILD', 'BUILT', 'BUYER', 'CABLE', 'CALIF', 'CARRY', 'CATCH', 'CAUSE',
  'CHAIN', 'CHAIR', 'CHART', 'CHASE', 'CHEAP', 'CHECK', 'CHEST', 'CHIEF',
  'CHILD', 'CHINA', 'CHOSE', 'CIVIL', 'CLAIM', 'CLASS', 'CLEAN', 'CLEAR',
  'CLICK', 'CLIMB', 'CLOCK', 'CLOSE', 'COACH', 'COAST', 'COULD', 'COUNT',
  'COURT', 'COVER', 'CRAFT', 'CRASH', 'CREAM', 'CRIME', 'CROSS', 'CROWD',
  'CROWN', 'CURVE', 'CYCLE', 'DAILY', 'DANCE', 'DATED', 'DEALT', 'DEATH',
  'DEBUT', 'DELAY', 'DEPTH', 'DOING', 'DOUBT', 'DOZEN', 'DRAFT', 'DRAMA',
  'DRAWN', 'DREAM', 'DRESS', 'DRINK', 'DRIVE', 'DROVE', 'DYING', 'EAGER',
  'EARLY', 'EARTH', 'EIGHT', 'ELITE', 'EMPTY', 'ENEMY', 'ENJOY', 'ENTER',
  'ENTRY', 'EQUAL', 'ERROR', 'EVENT', 'EVERY', 'EXACT', 'EXIST', 'EXTRA',
  'FAITH', 'FALSE', 'FAULT', 'FIBER', 'FIELD', 'FIFTH', 'FIFTY', 'FIGHT',
  'FINAL', 'FIRST', 'FIXED', 'FLASH', 'FLEET', 'FLOOR', 'FLUID', 'FOCUS',
  'FORCE', 'FORTH', 'FORTY', 'FORUM', 'FOUND', 'FRAME', 'FRANK', 'FRAUD',
  'FRESH', 'FRONT', 'FRUIT', 'FULLY', 'FUNNY', 'GIANT', 'GIVEN', 'GLASS',
  'GLOBE', 'GOING', 'GRACE', 'GRADE', 'GRAND', 'GRANT', 'GRASS', 'GRAVE',
  'GREAT', 'GREEN', 'GROSS', 'GROUP', 'GROWN', 'GUARD', 'GUESS', 'GUEST',
  'GUIDE', 'HAPPY', 'HARRY', 'HEART', 'HEAVY', 'HENCE', 'HENRY', 'HORSE',
  'HOTEL', 'HOUSE', 'HUMAN', 'IDEAL', 'IMAGE', 'INDEX', 'INNER', 'INPUT',
  'ISSUE', 'JAPAN', 'JIMMY', 'JOINT', 'JONES', 'JUDGE', 'KNOWN', 'LABEL',
  'LARGE', 'LASER', 'LATER', 'LAUGH', 'LAYER', 'LEARN', 'LEASE', 'LEAST',
  'LEAVE', 'LEGAL', 'LEVEL', 'LEWIS', 'LIGHT', 'LIMIT', 'LINKS', 'LIVES',
  'LOCAL', 'LOOSE', 'LOWER', 'LUCKY', 'LUNCH', 'LYING', 'MAGIC', 'MAJOR',
  'MAKER', 'MARCH', 'MARIA', 'MATCH', 'MAYBE', 'MAYOR', 'MEANT', 'MEDIA',
  'METAL', 'MIGHT', 'MINOR', 'MINUS', 'MIXED', 'MODEL', 'MONEY', 'MONTH',
  'MORAL', 'MOTOR', 'MOUNT', 'MOUSE', 'MOUTH', 'MOVED', 'MOVIE', 'MUSIC',
  'NEEDS', 'NEVER', 'NEWLY', 'NIGHT', 'NOISE', 'NORTH', 'NOTED', 'NOVEL',
  'NURSE', 'OCCUR', 'OCEAN', 'OFFER', 'OFFIC', 'ORDER', 'OTHER', 'OUGHT',
  'PAINT', 'PANEL', 'PAPER', 'PARTY', 'PEACE', 'PETER', 'PHASE', 'PHONE',
  'PHOTO', 'PIECE', 'PILOT', 'PITCH', 'PLACE', 'PLAIN', 'PLANE', 'PLANT',
  'PLATE', 'POINT', 'POUND', 'POWER', 'PRESS', 'PRICE', 'PRIDE', 'PRIME',
  'PRINT', 'PRIOR', 'PRIZE', 'PROOF', 'PROUD', 'PROVE', 'QUEEN', 'QUICK',
  'QUIET', 'QUITE', 'RADIO', 'RAISE', 'RANGE', 'RAPID', 'RATIO', 'REACH',
  'READY', 'REALM', 'REBEL', 'REFER', 'RELAX', 'REPLY', 'RIGHT', 'RIVAL',
  'RIVER', 'ROBIN', 'ROGER', 'ROMAN', 'ROUGH', 'ROUND', 'ROUTE', 'ROYAL',
  'RURAL', 'SADLY', 'SAFER', 'SALLY', 'SALON', 'SAUCE', 'SCALE', 'SCENE',
  'SCOPE', 'SCORE', 'SENSE', 'SERVE', 'SEVEN', 'SHALL', 'SHAPE', 'SHARE',
  'SHARP', 'SHEET', 'SHELF', 'SHELL', 'SHIFT', 'SHIRT', 'SHOCK', 'SHOOT',
  'SHORT', 'SHOWN', 'SIGHT', 'SINCE', 'SIXTH', 'SIXTY', 'SIZED', 'SKILL',
  'SLEEP', 'SLIDE', 'SMALL', 'SMART', 'SMILE', 'SMITH', 'SMOKE', 'SOLID',
  'SOLVE', 'SORRY', 'SOUND', 'SOUTH', 'SPACE', 'SPARE', 'SPEAK', 'SPEED',
  'SPEND', 'SPENT', 'SPLIT', 'SPOKE', 'SPORT', 'STAFF', 'STAGE', 'STAKE',
  'STAND', 'START', 'STATE', 'STEAM', 'STEEL', 'STEEP', 'STEER', 'STEMS',
  'STEPS', 'STICK', 'STILL', 'STOCK', 'STONE', 'STOOD', 'STORE', 'STORM',
  'STORY', 'STRIP', 'STRUCK', 'STUCK', 'STUDY', 'STUFF', 'STYLE', 'SUGAR',
  'SUITE', 'SUPER', 'SWEET', 'TABLE', 'TAKEN', 'TASTE', 'TAXES', 'TEACH',
  'TEETH', 'TERRY', 'TEXAS', 'THANK', 'THEFT', 'THEIR', 'THEME', 'THERE',
  'THESE', 'THICK', 'THING', 'THINK', 'THIRD', 'THOSE', 'THREE', 'THREW',
  'THROW', 'THUMB', 'TIGER', 'TIGHT', 'TIMER', 'TIRED', 'TITLE', 'TODAY',
  'TOPIC', 'TOTAL', 'TOUCH', 'TOUGH', 'TOWER', 'TRACK', 'TRADE', 'TRAIN',
  'TREAT', 'TREND', 'TRIAL', 'TRIBE', 'TRICK', 'TRIED', 'TRIES', 'TRUCK',
  'TRULY', 'TRUNK', 'TRUST', 'TRUTH', 'TWICE', 'UNDER', 'UNDUE', 'UNION',
  'UNITY', 'UNTIL', 'UPPER', 'UPSET', 'URBAN', 'USAGE', 'USUAL', 'VALID',
  'VALUE', 'VIDEO', 'VIRUS', 'VISIT', 'VITAL', 'VOICE', 'WASTE', 'WATCH',
  'WATER', 'WHEEL', 'WHERE', 'WHICH', 'WHILE', 'WHITE', 'WHOLE', 'WHOSE',
  'WOMAN', 'WOMEN', 'WORLD', 'WORRY', 'WORSE', 'WORST', 'WORTH', 'WOULD',
  'WOUND', 'WRITE', 'WRONG', 'WROTE', 'YIELD', 'YOUNG', 'YOUTH'
]

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

  const [currentAnswer, setCurrentAnswer] = useState(null)
  const [candidateWords, setCandidateWords] = useState([...DEFAULT_WORDS])

  const startGame = useCallback((mode) => {
    let answer
    if (mode === 'cheating') {
      // For cheating mode, we'll determine the answer after the first guess
      answer = null
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
      candidatesRemaining: mode === 'cheating' ? DEFAULT_WORDS.length : null
    })
  }, [])

  const makeGuess = useCallback((guess) => {
    const upperGuess = guess.toUpperCase()
    
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
    resetGame
  }
} 