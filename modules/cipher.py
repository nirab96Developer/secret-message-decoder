from typing import List, Tuple, Optional
import string


# Common English words for detection
COMMON_ENGLISH_WORDS = {"the", "and", "is", "message", "secret", "to", "of", 
                       "in", "for", "on", "with", "at", "by", "from", "this"}


def encrypt_text(text: str, shift: int) -> str:
    """
    Encrypt text using Caesar cipher
    
    Args:
        text: The text to encrypt
        shift: Number of positions to shift (0-25)
    
    Returns:
        Encrypted text with the given shift
    """
    shift = shift % 26  # Ensure shift is within 0-25
    result = []
    
    for ch in text:
        if ch.isalpha():
            # Determine if uppercase (65) or lowercase (97)
            base = 65 if ch.isupper() else 97
            # Apply shift and wrap around alphabet
            encrypted_ch = chr((ord(ch) - base + shift) % 26 + base)
            result.append(encrypted_ch)
        else:
            # Keep non-alphabetic characters as-is
            result.append(ch)
    
    return ''.join(result)


def decrypt_text(text: str, shift: int) -> str:
    """
    Decrypt text - essentially encryption with negative shift
    
    Args:
        text: The encrypted text
        shift: The shift value used for encryption
    
    Returns:
        Decrypted text
    """
    return encrypt_text(text, -shift)


def check_english_words(text, min_matches=3):
    """
    Check if text contains enough common English words
    
    Args:
        text: Text to check
        min_matches: Minimum number of matches required
    
    Returns:
        Tuple of (is_valid, match_count)
    """
    words = text.lower().split()
    
    # Clean punctuation from words
    clean_words = []
    for w in words:
        cleaned = w.strip(string.punctuation)
        if cleaned:
            clean_words.append(cleaned)
    
    # Count matches with common words
    matches = sum(1 for w in clean_words if w in COMMON_ENGLISH_WORDS)
    
    # Check if meets minimum threshold
    is_valid = matches >= min_matches
    
    return is_valid, matches


def calculate_word_score(text):
    """
    Calculate score based on percentage of common English words
    
    Args:
        text: Text to analyze
    
    Returns:
        Score between 0.0 and 1.0
    """
    words = text.lower().split()
    if not words:
        return 0.0
    
    # Clean punctuation
    cleaned = [w.strip(string.punctuation) for w in words]
    cleaned = [w for w in cleaned if w]  # Remove empty strings
    
    if not cleaned:
        return 0.0
    
    # Calculate percentage of common words
    matches = sum(1 for w in cleaned if w in COMMON_ENGLISH_WORDS)
    score = matches / len(cleaned)
    
    return score


def brute_force_decrypt(encrypted_text, verbose=False):
    """
    Brute force decryption - tries all possible shifts
    
    Args:
        encrypted_text: The encrypted text to decrypt
        verbose: Whether to print progress
    
    Returns:
        Tuple of (best_text, best_shift, all_attempts)
    """
    best_score = 0.0
    best_shift = None
    best_text = None
    attempts = []
    
    if verbose:
        print("Trying all shifts...")
        print("-" * 50)
    
    # Try every possible shift (0-25)
    for shift in range(26):
        decrypted = decrypt_text(encrypted_text, shift)
        
        # Check if it looks like English
        is_eng, match_cnt = check_english_words(decrypted)
        score = calculate_word_score(decrypted)
        
        # Store attempt for later use
        attempts.append((shift, decrypted, score))
        
        if verbose and (is_eng or shift == 0):
            # Show preview of decrypted text
            preview = decrypted[:50]
            if len(decrypted) > 50:
                preview += "..."
            print(f"Shift {shift:2d}: {preview}")
            print(f"          Matches: {match_cnt}, Score: {score:.2f}")
        
        # Update best result if score is higher
        if score > best_score:
            best_score = score
            best_shift = shift
            best_text = decrypted
    
    # Sort attempts by score (highest first)
    attempts.sort(key=lambda x: x[2], reverse=True)
    
    if verbose:
        print("-" * 50)
        if best_shift is not None:
            print(f"Best: shift {best_shift} (score: {best_score:.2f})")
        else:
            print("Failed to find valid text")
    
    return best_text, best_shift, attempts


def get_shift_between_texts(original, encrypted):
    """
    Find the shift value between original and encrypted text
    
    Args:
        original: Original plain text
        encrypted: Encrypted version of the text
    
    Returns:
        Shift value if found, None otherwise
    """
    for orig_ch, enc_ch in zip(original, encrypted):
        if orig_ch.isalpha() and enc_ch.isalpha():
            # Check if they have the same case
            if orig_ch.isupper() != enc_ch.isupper():
                return None
            
            # Calculate the shift
            if orig_ch.isupper():
                shift = (ord(enc_ch) - ord(orig_ch)) % 26
            else:
                shift = (ord(enc_ch) - ord(orig_ch)) % 26
            
            # Verify shift works for entire text
            if encrypt_text(original, shift) == encrypted:
                return shift
            else:
                return None
    
    return None


class CaesarCipher:
    """
    Class for working with Caesar cipher encryption/decryption
    
    Provides methods for encryption, decryption, and automatic
    brute force decryption with score calculation.
    """
    
    def __init__(self):
        """Initialize cipher with empty attempts list"""
        self.last_attempts = []  # Store last decryption attempts for visualization
    
    def encrypt(self, text, shift):
        """
        Encrypt text with given shift
        
        Args:
            text: Text to encrypt
            shift: Shift value (0-25)
        
        Returns:
            Encrypted text
        """
        return encrypt_text(text, shift)
    
    def decrypt(self, text, shift):
        """
        Decrypt text with known shift
        
        Args:
            text: Encrypted text
            shift: Known shift value
        
        Returns:
            Decrypted text
        """
        return decrypt_text(text, shift)
    
    def brute_force_decrypt(self, encrypted_text):
        """
        Automatic decryption - finds best shift and decrypts
        
        Args:
            encrypted_text: Text to decrypt
        
        Returns:
            Tuple of (best_shift, decrypted_text)
        """
        decrypted, shift, attempts = brute_force_decrypt(encrypted_text)
        self.last_attempts = attempts  # Save for graph visualization
        return shift, decrypted
    
    def calculate_score(self, text):
        """
        Calculate how much the text looks like English
        
        Args:
            text: Text to analyze
        
        Returns:
            Score between 0.0 and 1.0
        """
        return calculate_word_score(text)