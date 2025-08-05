from typing import Dict, List, Tuple, Any
import string
from collections import Counter


def analyze_text(text):
    """
    Comprehensive text analysis using built-in Python functions
    
    Uses 10+ built-in functions: len, set, max, min, sum, sorted, any, all,
    zip, map, filter, enumerate, Counter
    
    Args:
        text: Text string to analyze
    
    Returns:
        Dictionary containing all analysis results
    """
    words = text.split()
    
    # Basic statistics
    word_count = len(words)
    char_count = len(text)
    unique_chars = len(set(text))
    
    # Find longest and shortest words
    longest = max(words, key=len) if words else ""
    shortest = min(filter(None, words), key=len) if words else ""
    
    # Calculate average word length
    avg_length = sum(map(len, words)) / len(words) if words else 0.0
    
    # Calculate vowel percentage
    vowels = 'aeiouAEIOU'
    vowel_count = sum(1 for ch in text if ch in vowels)
    alpha_count = sum(1 for ch in text if ch.isalpha())
    vowel_percent = (vowel_count / alpha_count * 100) if alpha_count > 0 else 0.0
    
    # Word checks using all() and any()
    all_lower = all(w.islower() or not w.isalpha() for w in words)
    has_long_word = any(len(w) > 7 for w in words)
    
    # Create lists using enumerate() and zip()
    indexed = list(enumerate(words))
    word_lengths = list(zip(words, map(len, words)))
    
    # Word length distribution
    length_dist = {}
    for w in words:
        l = len(w)
        length_dist[l] = length_dist.get(l, 0) + 1
    
    # Count unique words
    unique_words = len(set(w.lower() for w in words))
    
    # Find most common word using Counter
    if words:
        word_counter = Counter([w.lower() for w in words])
        most_common = word_counter.most_common(1)[0] if word_counter else ("", 0)
    else:
        most_common = ("", 0)
    
    # Count character types
    digit_count = sum(1 for ch in text if ch.isdigit())
    punct_count = sum(1 for ch in text if ch in string.punctuation)
    
    # Count words starting with vowel
    vowel_start = sum(1 for w in words if w and w[0] in vowels)
    
    # Find palindromes (words that read same forwards and backwards)
    palindromes = []
    for w in words:
        clean = ''.join(ch.lower() for ch in w if ch.isalpha())
        if clean and clean == clean[::-1] and len(clean) > 1:
            palindromes.append(w)
    
    # Compile all results into dictionary
    results = {
        'original_text': text,
        'word_count': word_count,
        'character_count': char_count,
        'unique_characters': unique_chars,
        'longest_word': longest,
        'shortest_word': shortest,
        'average_word_length': avg_length,
        'vowel_percentage': vowel_percent,
        'words_sorted_by_length': sorted(words, key=len),
        'all_lowercase': all_lower,
        'any_word_longer_than_7': has_long_word,
        'indexed_words': indexed,
        'word_length_pairs': word_lengths,
        'word_length_distribution': dict(sorted(length_dist.items())),
        'unique_words_count': unique_words,
        'most_common_word': most_common,
        'alphabetic_character_count': alpha_count,
        'digit_count': digit_count,
        'punctuation_count': punct_count,
        'words_starting_with_vowel': vowel_start,
        'palindrome_words': palindromes
    }
    
    return results


def count_words(text):
    """
    Simple word count function
    
    Args:
        text: Input text string
    
    Returns:
        Number of words in text
    """
    return len(text.split())


def count_unique_characters(text):
    """
    Count unique characters in text
    
    Args:
        text: Input text string
    
    Returns:
        Number of unique characters
    """
    return len(set(text))


def find_longest_word(words):
    """
    Find the longest word in a list
    
    Args:
        words: List of words
    
    Returns:
        Longest word or empty string if list is empty
    """
    if not words:
        return ""
    return max(words, key=len)


def find_shortest_word(words):
    """
    Find the shortest non-empty word in a list
    
    Args:
        words: List of words
    
    Returns:
        Shortest word or empty string if list is empty
    """
    if not words:
        return ""
    clean_words = list(filter(None, words))  # Remove empty strings
    if not clean_words:
        return ""
    return min(clean_words, key=len)


def calculate_average_word_length(words):
    """
    Calculate average word length
    
    Args:
        words: List of words
    
    Returns:
        Average length as float
    """
    if not words:
        return 0.0
    lengths = list(map(len, words))  # Map words to their lengths
    return sum(lengths) / len(words)


def calculate_vowel_percentage(text):
    """
    Calculate percentage of vowels in alphabetic characters
    
    Args:
        text: Input text string
    
    Returns:
        Percentage of vowels (0-100)
    """
    if not text:
        return 0.0
    
    vowels = 'aeiouAEIOU'
    vowel_cnt = sum(1 for c in text if c in vowels)
    alpha_cnt = sum(1 for c in text if c.isalpha())
    
    if alpha_cnt == 0:
        return 0.0
    
    return (vowel_cnt / alpha_cnt) * 100


def sort_words_by_length(words):
    """
    Sort words by their length
    
    Args:
        words: List of words
    
    Returns:
        Sorted list (shortest to longest)
    """
    return sorted(words, key=len)


def check_all_lowercase(words):
    """
    Check if all words are lowercase
    
    Args:
        words: List of words
    
    Returns:
        True if all words are lowercase (ignoring non-alphabetic)
    """
    if not words:
        return True
    return all(w.islower() or not w.isalpha() for w in words)


def check_any_word_longer_than(words, length):
    """
    Check if any word is longer than specified length
    
    Args:
        words: List of words
        length: Length threshold
    
    Returns:
        True if any word exceeds the length
    """
    return any(len(w) > length for w in words)


def get_indexed_words(words):
    """
    Create indexed list of words
    
    Args:
        words: List of words
    
    Returns:
        List of (index, word) tuples
    """
    return list(enumerate(words))


def create_word_length_pairs(words):
    """
    Create pairs of words with their lengths
    
    Args:
        words: List of words
    
    Returns:
        List of (word, length) tuples
    """
    lengths = map(len, words)
    return list(zip(words, lengths))


def get_word_length_distribution(words):
    """
    Get distribution of word lengths
    
    Args:
        words: List of words
    
    Returns:
        Dictionary mapping length to count
    """
    if not words:
        return {}
    
    dist = {}
    for w in words:
        l = len(w)
        dist[l] = dist.get(l, 0) + 1
    
    return dict(sorted(dist.items()))


def count_unique_words(words):
    """
    Count unique words (case-insensitive)
    
    Args:
        words: List of words
    
    Returns:
        Number of unique words
    """
    return len(set(w.lower() for w in words))


def find_most_common_word(words):
    """
    Find the most frequently occurring word
    
    Args:
        words: List of words
    
    Returns:
        Tuple of (word, count)
    """
    if not words:
        return ("", 0)
    
    lower_words = [w.lower() for w in words]
    counter = Counter(lower_words)
    
    if counter:
        return counter.most_common(1)[0]
    return ("", 0)


def count_alphabetic_characters(text):
    """
    Count alphabetic characters in text
    
    Args:
        text: Input text string
    
    Returns:
        Number of alphabetic characters
    """
    return sum(1 for c in text if c.isalpha())


def count_digits(text):
    """
    Count digit characters in text
    
    Args:
        text: Input text string
    
    Returns:
        Number of digits
    """
    return sum(1 for c in text if c.isdigit())


def count_punctuation(text):
    """
    Count punctuation characters in text
    
    Args:
        text: Input text string
    
    Returns:
        Number of punctuation marks
    """
    return sum(1 for c in text if c in string.punctuation)


def count_words_starting_with_vowel(words):
    """
    Count words that start with a vowel
    
    Args:
        words: List of words
    
    Returns:
        Number of words starting with vowels
    """
    vowels = 'aeiouAEIOU'
    return sum(1 for w in words if w and w[0] in vowels)


def find_palindrome_words(words):
    """
    Find palindrome words (read same forwards and backwards)
    
    Args:
        words: List of words
    
    Returns:
        List of palindrome words
    """
    palindromes = []
    for word in words:
        # Clean word of non-alphabetic characters
        clean = ''.join(c.lower() for c in word if c.isalpha())
        # Check if palindrome (length > 1)
        if clean and clean == clean[::-1] and len(clean) > 1:
            palindromes.append(word)
    return palindromes


def format_analysis_report(analysis):
    """
    Create formatted text report from analysis results
    
    Args:
        analysis: Dictionary with analysis results
    
    Returns:
        Formatted string report
    """
    lines = []
    lines.append("=" * 50)
    lines.append("TEXT ANALYSIS REPORT")
    lines.append("=" * 50)
    lines.append("")
    
    # Basic statistics section
    lines.append("BASIC STATS:")
    lines.append(f"  Words: {analysis['word_count']}")
    lines.append(f"  Characters: {analysis['character_count']}")
    lines.append(f"  Unique chars: {analysis['unique_characters']}")
    lines.append(f"  Unique words: {analysis['unique_words_count']}")
    lines.append("")
    
    # Character types section
    lines.append("CHARACTER TYPES:")
    lines.append(f"  Letters: {analysis['alphabetic_character_count']}")
    lines.append(f"  Digits: {analysis['digit_count']}")
    lines.append(f"  Punctuation: {analysis['punctuation_count']}")
    lines.append(f"  Vowels: {analysis['vowel_percentage']:.1f}%")
    lines.append("")
    
    # Word information section
    lines.append("WORD INFO:")
    lines.append(f"  Longest: '{analysis['longest_word']}' ({len(analysis['longest_word'])} chars)")
    lines.append(f"  Shortest: '{analysis['shortest_word']}' ({len(analysis['shortest_word'])} chars)")
    lines.append(f"  Average length: {analysis['average_word_length']:.1f}")
    lines.append(f"  All lowercase: {analysis['all_lowercase']}")
    lines.append(f"  Has long words (>7): {analysis['any_word_longer_than_7']}")
    lines.append(f"  Start with vowel: {analysis['words_starting_with_vowel']}")
    
    # Most common word
    if analysis['most_common_word'][0]:
        lines.append(f"  Most common: '{analysis['most_common_word'][0]}' ({analysis['most_common_word'][1]}x)")
    
    # Palindromes
    if analysis['palindrome_words']:
        lines.append(f"  Palindromes: {', '.join(analysis['palindrome_words'])}")
    
    lines.append("")
    
    # Word length distribution with bar chart
    lines.append("LENGTH DISTRIBUTION:")
    for length, count in sorted(analysis['word_length_distribution'].items()):
        bar = "█" * count  # Visual bar representation
        lines.append(f"  {length:2d} chars: {bar} ({count})")
    
    lines.append("")
    lines.append("=" * 50)
    
    return "\n".join(lines)


class TextAnalyzer:
    """
    Text analyzer class for GUI integration
    
    Provides full text analysis with additional metrics for visualization
    """
    
    def __init__(self):
        """Initialize analyzer (no state needed)"""
        pass  # Nothing to initialize
    
    def full_analysis(self, text):
        """
        Perform full analysis for GUI display
        
        Args:
            text: Text string to analyze
        
        Returns:
            Dictionary with comprehensive analysis results
        """
        # Call main analysis function
        analysis = analyze_text(text)
        
        # Add GUI-friendly aliases
        analysis['total_chars'] = analysis['character_count']
        analysis['unique_words'] = analysis['unique_words_count']
        
        # Calculate vowel count from percentage
        if analysis['alphabetic_character_count'] > 0:
            analysis['vowel_count'] = int(analysis['vowel_percentage'] * analysis['alphabetic_character_count'] / 100)
        else:
            analysis['vowel_count'] = 0
        
        # Calculate character type percentages
        total = len(text)
        if total > 0:
            analysis['letter_percentage'] = (analysis['alphabetic_character_count'] / total * 100)
            analysis['digit_percentage'] = (analysis['digit_count'] / total * 100)
            analysis['space_percentage'] = (text.count(' ') / total * 100)
        else:
            analysis['letter_percentage'] = 0.0
            analysis['digit_percentage'] = 0.0
            analysis['space_percentage'] = 0.0
        
        # Calculate word frequencies
        words = text.split()
        if words:
            # Top words by frequency
            word_freq = Counter(w.lower() for w in words if w.strip())
            analysis['top_words'] = word_freq.most_common(20)
            
            # Letter frequency
            letter_freq = Counter(c.lower() for c in text if c.isalpha())
            analysis['letter_frequency'] = letter_freq.most_common()
            
            # Ensure word length distribution exists
            if 'word_length_distribution' not in analysis:
                analysis['word_length_distribution'] = get_word_length_distribution(words)
        else:
            analysis['top_words'] = []
            analysis['letter_frequency'] = []
            analysis['word_length_distribution'] = {}
        
        return analysis