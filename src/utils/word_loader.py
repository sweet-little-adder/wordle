"""
Word list loading and management utilities.

This module provides functions for loading word lists from files
and managing word list operations.
"""

import os
from typing import List, Set
from pathlib import Path


def load_word_list(file_path: str) -> List[str]:
    """
    Load a word list from a file.
    
    Args:
        file_path: Path to the word list file
        
    Returns:
        List of words from the file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is empty or contains invalid words
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Word list file not found: {file_path}")
    
    words = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            word = line.strip().upper()
            if word:  # Skip empty lines
                if not word.isalpha() or len(word) != 5:
                    raise ValueError(f"Invalid word at line {line_num}: {word}")
                words.append(word)
    
    if not words:
        raise ValueError("Word list file is empty")
    
    return words


def get_default_word_list() -> List[str]:
    """
    Get the default word list for the game.
    
    Returns:
        List of common 5-letter English words
    """
    # Common 5-letter words for Wordle
    default_words = [
        "ABOUT", "ABOVE", "ABUSE", "ACTOR", "ACUTE", "ADMIT", "ADOPT", "ADULT",
        "AFTER", "AGAIN", "AGENT", "AGREE", "AHEAD", "ALARM", "ALBUM", "ALERT",
        "ALIKE", "ALIVE", "ALLOW", "ALONE", "ALONG", "ALTER", "AMONG", "ANGER",
        "ANGLE", "ANGRY", "APART", "APPLE", "APPLY", "ARENA", "ARGUE", "ARISE",
        "ARRAY", "ASIDE", "ASSET", "AUDIO", "AUDIT", "AVOID", "AWARD", "AWARE",
        "BADLY", "BAKER", "BASES", "BASIC", "BASIS", "BEACH", "BEGAN", "BEGIN",
        "BEING", "BELOW", "BENCH", "BILLY", "BIRTH", "BLACK", "BLAME", "BLIND",
        "BLOCK", "BLOOD", "BOARD", "BOOST", "BOOTH", "BOUND", "BRAIN", "BRAND",
        "BREAD", "BREAK", "BREED", "BRIEF", "BRING", "BROAD", "BROKE", "BROWN",
        "BUILD", "BUILT", "BUYER", "CABLE", "CALIF", "CARRY", "CATCH", "CAUSE",
        "CHAIN", "CHAIR", "CHART", "CHASE", "CHEAP", "CHECK", "CHEST", "CHIEF",
        "CHILD", "CHINA", "CHOSE", "CIVIL", "CLAIM", "CLASS", "CLEAN", "CLEAR",
        "CLICK", "CLIMB", "CLOCK", "CLOSE", "COACH", "COAST", "COULD", "COUNT",
        "COURT", "COVER", "CRAFT", "CRASH", "CREAM", "CRIME", "CROSS", "CROWD",
        "CROWN", "CURVE", "CYCLE", "DAILY", "DANCE", "DATED", "DEALT", "DEATH",
        "DEBUT", "DELAY", "DEPTH", "DOING", "DOUBT", "DOZEN", "DRAFT", "DRAMA",
        "DRAWN", "DREAM", "DRESS", "DRINK", "DRIVE", "DROVE", "DYING", "EAGER",
        "EARLY", "EARTH", "EIGHT", "ELITE", "EMPTY", "ENEMY", "ENJOY", "ENTER",
        "ENTRY", "EQUAL", "ERROR", "EVENT", "EVERY", "EXACT", "EXIST", "EXTRA",
        "FAITH", "FALSE", "FAULT", "FIBER", "FIELD", "FIFTH", "FIFTY", "FIGHT",
        "FINAL", "FIRST", "FIXED", "FLASH", "FLEET", "FLOOR", "FLUID", "FOCUS",
        "FORCE", "FORTH", "FORTY", "FORUM", "FOUND", "FRAME", "FRANK", "FRAUD",
        "FRESH", "FRONT", "FRUIT", "FULLY", "FUNNY", "GIANT", "GIVEN", "GLASS",
        "GLOBE", "GOING", "GRACE", "GRADE", "GRAND", "GRANT", "GRASS", "GRAVE",
        "GREAT", "GREEN", "GROSS", "GROUP", "GROWN", "GUARD", "GUESS", "GUEST",
        "GUIDE", "HAPPY", "HARRY", "HEART", "HEAVY", "HENCE", "HENRY", "HORSE",
        "HOTEL", "HOUSE", "HUMAN", "IDEAL", "IMAGE", "INDEX", "INNER", "INPUT",
        "ISSUE", "JAPAN", "JIMMY", "JOINT", "JONES", "JUDGE", "KNOWN", "LABEL",
        "LARGE", "LASER", "LATER", "LAUGH", "LAYER", "LEARN", "LEASE", "LEAST",
        "LEAVE", "LEGAL", "LEVEL", "LEWIS", "LIGHT", "LIMIT", "LINKS", "LIVES",
        "LOCAL", "LOOSE", "LOWER", "LUCKY", "LUNCH", "LYING", "MAGIC", "MAJOR",
        "MAKER", "MARCH", "MARIA", "MATCH", "MAYBE", "MAYOR", "MEANT", "MEDIA",
        "METAL", "MIGHT", "MINOR", "MINUS", "MIXED", "MODEL", "MONEY", "MONTH",
        "MORAL", "MOTOR", "MOUNT", "MOUSE", "MOUTH", "MOVED", "MOVIE", "MUSIC",
        "NEEDS", "NEVER", "NEWLY", "NIGHT", "NOISE", "NORTH", "NOTED", "NOVEL",
        "NURSE", "OCCUR", "OCEAN", "OFFER", "OFFIC", "ORDER", "OTHER", "OUGHT",
        "PAINT", "PANEL", "PAPER", "PARTY", "PEACE", "PETER", "PHASE", "PHONE",
        "PHOTO", "PIECE", "PILOT", "PITCH", "PLACE", "PLAIN", "PLANE", "PLANT",
        "PLATE", "POINT", "POUND", "POWER", "PRESS", "PRICE", "PRIDE", "PRIME",
        "PRINT", "PRIOR", "PRIZE", "PROOF", "PROUD", "PROVE", "QUEEN", "QUICK",
        "QUIET", "QUITE", "RADIO", "RAISE", "RANGE", "RAPID", "RATIO", "REACH",
        "READY", "REALM", "REBEL", "REFER", "RELAX", "REPLY", "RIGHT", "RIVAL",
        "RIVER", "ROBIN", "ROGER", "ROMAN", "ROUGH", "ROUND", "ROUTE", "ROYAL",
        "RURAL", "SADLY", "SAFER", "SALLY", "SALON", "SAUCE", "SCALE", "SCENE",
        "SCOPE", "SCORE", "SENSE", "SERVE", "SEVEN", "SHALL", "SHAPE", "SHARE",
        "SHARP", "SHEET", "SHELF", "SHELL", "SHIFT", "SHIRT", "SHOCK", "SHOOT",
        "SHORT", "SHOWN", "SIGHT", "SINCE", "SIXTH", "SIXTY", "SIZED", "SKILL",
        "SLEEP", "SLIDE", "SMALL", "SMART", "SMILE", "SMITH", "SMOKE", "SOLID",
        "SOLVE", "SORRY", "SOUND", "SOUTH", "SPACE", "SPARE", "SPEAK", "SPEED",
        "SPEND", "SPENT", "SPLIT", "SPOKE", "SPORT", "STAFF", "STAGE", "STAKE",
        "STAND", "START", "STATE", "STEAM", "STEEL", "STEEP", "STEER", "STEMS",
        "STEPS", "STICK", "STILL", "STOCK", "STONE", "STOOD", "STORE", "STORM",
        "STORY", "STRIP", "STRUCK", "STUCK", "STUDY", "STUFF", "STYLE", "SUGAR",
        "SUITE", "SUPER", "SWEET", "TABLE", "TAKEN", "TASTE", "TAXES", "TEACH",
        "TEETH", "TERRY", "TEXAS", "THANK", "THEFT", "THEIR", "THEME", "THERE",
        "THESE", "THICK", "THING", "THINK", "THIRD", "THOSE", "THREE", "THREW",
        "THROW", "THUMB", "TIGER", "TIGHT", "TIMER", "TIRED", "TITLE", "TODAY",
        "TOPIC", "TOTAL", "TOUCH", "TOUGH", "TOWER", "TRACK", "TRADE", "TRAIN",
        "TREAT", "TREND", "TRIAL", "TRIBE", "TRICK", "TRIED", "TRIES", "TRUCK",
        "TRULY", "TRUNK", "TRUST", "TRUTH", "TWICE", "UNDER", "UNDUE", "UNION",
        "UNITY", "UNTIL", "UPPER", "UPSET", "URBAN", "USAGE", "USUAL", "VALID",
        "VALUE", "VIDEO", "VIRUS", "VISIT", "VITAL", "VOICE", "WASTE", "WATCH",
        "WATER", "WHEEL", "WHERE", "WHICH", "WHILE", "WHITE", "WHOLE", "WHOSE",
        "WOMAN", "WOMEN", "WORLD", "WORRY", "WORSE", "WORST", "WORTH", "WOULD",
        "WOUND", "WRITE", "WRONG", "WROTE", "YIELD", "YOUNG", "YOUTH"
    ]
    
    return default_words


def create_word_list_file(file_path: str, words: List[str]) -> None:
    """
    Create a word list file with the given words.
    
    Args:
        file_path: Path where to create the file
        words: List of words to write to the file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(f"{word.upper()}\n")


def validate_word_list(words: List[str]) -> bool:
    """
    Validate a list of words.
    
    Args:
        words: List of words to validate
        
    Returns:
        True if all words are valid, False otherwise
    """
    for word in words:
        if not word.isalpha() or len(word) != 5:
            return False
    return True


def filter_words_by_pattern(words: List[str], pattern: str, result: List[str]) -> List[str]:
    """
    Filter words based on a guess pattern and result.
    
    This is used for the cheating host mode to maintain candidate words.
    
    Args:
        words: List of words to filter
        pattern: The guessed word
        result: List of LetterResult for the pattern
        
    Returns:
        Filtered list of words that match the pattern and result
    """
    from ..core.game_engine import LetterResult
    
    filtered_words = []
    
    for word in words:
        # Check if this word could have produced the given result
        if _word_matches_pattern(word, pattern, result):
            filtered_words.append(word)
    
    return filtered_words


def _word_matches_pattern(word: str, pattern: str, result: List[str]) -> bool:
    """
    Check if a word matches a given pattern and result.
    
    Args:
        word: The word to check
        pattern: The guessed pattern
        result: List of LetterResult for the pattern
        
    Returns:
        True if the word matches the pattern and result
    """
    from ..core.game_engine import LetterResult
    
    # Create a copy of the word for checking
    word_letters = list(word)
    pattern_letters = list(pattern)
    
    # First pass: Check hits
    for i in range(5):
        if result[i] == LetterResult.HIT:
            if word_letters[i] != pattern_letters[i]:
                return False
            word_letters[i] = None
            pattern_letters[i] = None
    
    # Second pass: Check presents and misses
    for i in range(5):
        if pattern_letters[i] is not None:
            if result[i] == LetterResult.PRESENT:
                # Letter should be in word but not at this position
                if pattern_letters[i] not in word_letters:
                    return False
                # Remove the first occurrence
                if pattern_letters[i] in word_letters:
                    word_letters[word_letters.index(pattern_letters[i])] = None
            elif result[i] == LetterResult.MISS:
                # Letter should not be in word
                if pattern_letters[i] in word_letters:
                    return False
    
    return True 