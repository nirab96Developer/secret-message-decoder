import os
import datetime
from typing import Optional, Tuple, List
import json


class FileHandler:
    """
    Handles file operations - reading, writing, and logging
    
    Manages encrypted/decrypted files, analysis reports, and operation logs.
    """
    
    def __init__(self, base_dir="."):
        """
        Initialize file handler with directory structure
        
        Args:
            base_dir: Base directory for all file operations
        """
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        self.decrypted_dir = os.path.join(self.data_dir, "decrypted")
        self.encrypted_file = os.path.join(self.data_dir, "encrypted_message.txt")
        self.log_file = os.path.join(self.data_dir, "operations.log")
        
        # Ensure directories exist
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """Create required directories if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.decrypted_dir, exist_ok=True)
    
    def _log_operation(self, op_type, details):
        """
        Write operation to log file
        
        Args:
            op_type: Type of operation (READ, SAVE, ERROR, etc.)
            details: Details about the operation
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {op_type}: {details}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_line)
        except:
            pass  # Don't fail if logging fails
    
    def read_encrypted_message(self, filepath=None):
        """
        Read encrypted message from file
        
        Args:
            filepath: Path to encrypted file (uses default if None)
        
        Returns:
            Tuple of (success, content/error, filepath)
        """
        if filepath is None:
            filepath = self.encrypted_file
        
        try:
            # Read file content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Check if file is empty
            if not content:
                return False, "File is empty", filepath
            
            # Log successful read
            self._log_operation("READ", f"Read from {filepath}")
            return True, content, filepath
            
        except FileNotFoundError:
            err = f"File not found: {filepath}"
            self._log_operation("ERROR", err)
            return False, err, filepath
            
        except Exception as e:
            err = f"Error reading: {str(e)}"
            self._log_operation("ERROR", err)
            return False, err, filepath
    
    def save_decrypted_message(self, text, shift, filename=None):
        """
        Save decrypted text to file
        
        Args:
            text: Decrypted text to save
            shift: Shift value used for decryption
            filename: Optional custom filename
        
        Returns:
            Tuple of (success, filepath/error)
        """
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"decrypted_shift{shift}_{timestamp}.txt"
        
        # Ensure .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        filepath = os.path.join(self.decrypted_dir, filename)
        
        try:
            # Create content with header information
            content = f"""DECRYPTED MESSAGE
================
Shift Used: {shift}
Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
================

{text}"""
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Log operation
            self._log_operation("SAVE", f"Saved to {filepath}")
            return True, filepath
            
        except Exception as e:
            err = f"Save failed: {str(e)}"
            self._log_operation("ERROR", err)
            return False, err
    
    def save_analysis_report(self, analysis_data, filename=None):
        """
        Save analysis report as JSON
        
        Args:
            analysis_data: Dictionary containing analysis results
            filename: Optional custom filename
        
        Returns:
            Tuple of (success, filepath/error)
        """
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analysis_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            # Create report structure
            report = {
                "timestamp": datetime.datetime.now().isoformat(),
                "analysis": analysis_data
            }
            
            # Write JSON file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Log operation
            self._log_operation("SAVE", f"Analysis saved to {filepath}")
            return True, filepath
            
        except Exception as e:
            err = f"Failed to save analysis: {str(e)}"
            self._log_operation("ERROR", err)
            return False, err
    
    def list_decrypted_files(self):
        """
        Get list of decrypted files
        
        Returns:
            List of file paths, sorted newest first
        """
        try:
            files = []
            # Scan decrypted directory
            for fname in os.listdir(self.decrypted_dir):
                if fname.endswith('.txt'):
                    files.append(os.path.join(self.decrypted_dir, fname))
            
            # Return sorted list (newest first)
            return sorted(files, reverse=True)
            
        except Exception as e:
            self._log_operation("ERROR", f"List failed: {str(e)}")
            return []
    
    def get_file_info(self, filepath):
        """
        Get information about a file
        
        Args:
            filepath: Path to the file
        
        Returns:
            Dictionary with file info or None if error
        """
        try:
            stat = os.stat(filepath)
            return {
                "path": filepath,
                "filename": os.path.basename(filepath),
                "size": stat.st_size,
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime),
                "created": datetime.datetime.fromtimestamp(stat.st_ctime)
            }
        except:
            return None
    
    def create_sample_encrypted_file(self, text, shift):
        """
        Create a sample encrypted file for testing
        
        Args:
            text: Plain text to encrypt
            shift: Shift value for encryption
        
        Returns:
            Tuple of (success, filepath/error)
        """
        try:
            # Import only when needed to avoid circular imports
            from modules.cipher import encrypt_text
            
            # Encrypt the text
            encrypted = encrypt_text(text, shift)
            
            # Write to file
            with open(self.encrypted_file, 'w', encoding='utf-8') as f:
                f.write(encrypted)
            
            # Log operation
            self._log_operation("CREATE", f"Sample file with shift {shift}")
            return True, self.encrypted_file
            
        except Exception as e:
            err = f"Failed to create sample: {str(e)}"
            self._log_operation("ERROR", err)
            return False, err
    
    def export_session_data(self, enc_text, dec_text, shift, analysis):
        """
        Export all session data to JSON
        
        Args:
            enc_text: Encrypted text
            dec_text: Decrypted text
            shift: Shift value used
            analysis: Analysis results dictionary
        
        Returns:
            Tuple of (success, filepath/error)
        """
        # Generate timestamp filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"session_{timestamp}.json"
        fpath = os.path.join(self.data_dir, fname)
        
        try:
            # Create session data structure
            data = {
                "export_time": datetime.datetime.now().isoformat(),
                "encrypted": enc_text,
                "decrypted": dec_text,
                "shift": shift,
                "analysis": analysis
            }
            
            # Write to JSON file
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Log operation
            self._log_operation("EXPORT", f"Session exported to {fpath}")
            return True, fpath
            
        except Exception as e:
            err = f"Export failed: {str(e)}"
            self._log_operation("ERROR", err)
            return False, err


# Helper functions
def ensure_file_extension(filename, ext):
    """
    Ensure filename has the correct extension
    
    Args:
        filename: File name to check
        ext: Extension to ensure (with or without dot)
    
    Returns:
        Filename with extension
    """
    # Add dot if missing
    if not ext.startswith('.'):
        ext = '.' + ext
    
    # Add extension if missing
    if not filename.endswith(ext):
        filename += ext
    
    return filename


def sanitize_filename(filename):
    """
    Remove illegal characters from filename
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename safe for file system
    """
    # Characters not allowed in filenames
    bad_chars = '<>:"/\\|?*'
    for ch in bad_chars:
        filename = filename.replace(ch, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Default name if empty
    if not filename:
        filename = "unnamed"
    
    return filename