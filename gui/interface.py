import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from pathlib import Path
import threading
import time
from datetime import datetime

from modules.cipher import CaesarCipher
from modules.text_analyzer import TextAnalyzer
from modules.file_handler import FileHandler
from modules.visualizer import TextVisualizer


class SecretMessageApp:
    """Main application class for the Secret Message Decoder GUI"""
    
    def __init__(self):
        """Initialize the application window and components"""
        # Create main window
        self.window = tk.Tk()
        self.window.title("Secret Message Decoder")
        self.window.geometry("1200x750")
        
        # Initialize modules
        self.cipher = CaesarCipher()
        self.analyzer = TextAnalyzer()
        self.file_handler = FileHandler()
        
        # Initialize variables
        self.current_shift = tk.IntVar(value=0)  # Stores detected shift
        self.new_shift = tk.IntVar(value=1)      # For re-encryption
        self.analysis_results = {}               # Stores analysis data
        self.history = []                        # Stores decryption history
        
        # Color scheme for UI
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#2196F3',
            'success': '#4CAF50',
            'danger': '#f44336',
            'text': '#212121',
            'light': '#fafafa'
        }
        
        # Apply background color
        self.window.configure(bg=self.colors['bg'])
        
        # Setup UI components
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        """Setup all UI components"""
        self.create_header()
        self.create_menu()
        
        # Create tab container
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.setup_decrypt_tab()
        self.setup_analysis_tab()
        self.setup_graphs_tab()
        
        # Status bar at bottom
        self.status_text = tk.StringVar(value="Ready")
        statusbar = tk.Label(self.window, textvariable=self.status_text,
                            bd=1, relief='sunken', anchor='w',
                            bg='white', padx=5)
        statusbar.pack(side='bottom', fill='x')
        
    def create_header(self):
        """Create application header with title"""
        # Blue header frame
        header_frame = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)  # Maintain fixed height
        
        # Title label
        lbl_title = tk.Label(header_frame, text="🔐 Secret Message Decoder",
                        font=('Arial', 20, 'bold'),
                        bg=self.colors['primary'], fg='white')
        lbl_title.pack(expand=True)
        
    def create_menu(self):
        """Create menu bar"""
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        
        # File menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.load_file)
        file_menu.add_command(label="Save Decrypted", command=self.save_result)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.quit)
        
        # Help menu
        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        
    def setup_decrypt_tab(self):
        """Setup the decryption tab"""
        tab_decrypt = ttk.Frame(self.notebook)
        self.notebook.add(tab_decrypt, text="Decrypt")
        
        # Encrypted message area
        encrypted_frame = tk.LabelFrame(tab_decrypt, text="Encrypted Message",
                                 padx=10, pady=10, font=('Arial', 11, 'bold'))
        encrypted_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text widget for encrypted input
        self.txt_encrypted = scrolledtext.ScrolledText(encrypted_frame, height=8,
                                                      wrap=tk.WORD,
                                                      font=('Consolas', 11))
        self.txt_encrypted.pack(fill='both', expand=True)
        
        # Button panel
        buttons_panel = tk.Frame(encrypted_frame)
        buttons_panel.pack(fill='x', pady=(10, 0))
        
        # Load file button
        tk.Button(buttons_panel, text="Load File",
                 command=self.load_file,
                 bg=self.colors['light']).pack(side='left', padx=5)
        
        # Auto decrypt button (main action)
        self.btn_decrypt = tk.Button(buttons_panel, text="Auto Decrypt",
                                    command=self.start_decryption,
                                    bg=self.colors['primary'], fg='white',
                                    font=('Arial', 10, 'bold'))
        self.btn_decrypt.pack(side='left', padx=5)
        
        # Clear button
        tk.Button(buttons_panel, text="Clear",
                 command=self.clear_enc_text).pack(side='left', padx=5)
        
        # Shift display on the right
        shift_display = tk.Frame(buttons_panel)
        shift_display.pack(side='right', padx=10)
        
        tk.Label(shift_display, text="Detected Shift: ",
                font=('Arial', 10)).pack(side='left')
        
        self.lbl_shift = tk.Label(shift_display, text="--",
                                  font=('Arial', 14, 'bold'),
                                  fg=self.colors['primary'])
        self.lbl_shift.pack(side='left')
        
        # Create decrypted message area
        self._create_decrypted_section(tab_decrypt)
        
    def _create_decrypted_section(self, parent):
        """Create the decrypted text area with action buttons"""
        # Decrypted message frame
        dec_frame = tk.LabelFrame(parent, text="Decrypted Message",
                                 padx=10, pady=10, font=('Arial', 11, 'bold'))
        dec_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Text widget with light green background
        self.txt_decrypted = scrolledtext.ScrolledText(dec_frame, height=8,
                                                       wrap=tk.WORD,
                                                       font=('Consolas', 11),
                                                       bg='#e8f5e9')  # Light green for decrypted text
        self.txt_decrypted.pack(fill='both', expand=True)
        
        # Action buttons panel
        actions = tk.Frame(dec_frame)
        actions.pack(fill='x', pady=(10, 0))
        
        # Save button with success color
        tk.Button(actions, text="Save",
                 command=self.save_result,
                 bg=self.colors['success'], fg='white').pack(side='left', padx=5)
        
        # Copy button
        tk.Button(actions, text="Copy",
                 command=self.copy_to_clipboard).pack(side='left', padx=5)
        
        # Analyze button
        tk.Button(actions, text="Analyze",
                 command=self.analyze_decrypted_text).pack(side='left', padx=5)
        
        # Re-encryption panel on the right
        reencrypt_panel = tk.Frame(actions)
        reencrypt_panel.pack(side='right', padx=10)
        
        tk.Label(reencrypt_panel, text="New Shift:").pack(side='left', padx=5)
        
        # Spinbox for shift value (1-25)
        spin = tk.Spinbox(reencrypt_panel, from_=1, to=25,
                              textvariable=self.new_shift,
                              width=5)
        spin.pack(side='left', padx=5)
        
        tk.Button(reencrypt_panel, text="Re-encrypt",
                 command=self.reencrypt).pack(side='left', padx=5)
        
    def setup_analysis_tab(self):
        """Setup the text analysis tab"""
        tab_analysis = ttk.Frame(self.notebook)
        self.notebook.add(tab_analysis, text="Analysis")
        
        # Control buttons
        controls = tk.Frame(tab_analysis)
        controls.pack(fill='x', padx=10, pady=10)
        
        # Run analysis button
        tk.Button(controls, text="Run Analysis",
                 command=self.analyze_decrypted_text,
                 bg=self.colors['primary'], fg='white',
                 font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Export button
        tk.Button(controls, text="Export Report",
                 command=self.export_results).pack(side='left', padx=5)
        
        # Text widget for analysis results
        self.txt_analysis = scrolledtext.ScrolledText(tab_analysis,
                                                      wrap=tk.WORD,
                                                      font=('Consolas', 10))
        self.txt_analysis.pack(fill='both', expand=True, padx=10, pady=5)
        
    def setup_graphs_tab(self):
        """Setup the visualizations tab"""
        tab_visual = ttk.Frame(self.notebook)
        self.notebook.add(tab_visual, text="Visualizations")
        
        # Graph selection buttons
        graph_buttons = tk.Frame(tab_visual)
        graph_buttons.pack(fill='x', padx=10, pady=10)
        
        # List of available graphs
        graphs = [
            ("Word Length", self.draw_word_length),
            ("Character Types", self.draw_chars),
            ("Word Frequency", self.draw_frequency),
            ("Shift Analysis", self.draw_shifts)
        ]
        
        # Create button for each graph type
        for name, func in graphs:
            tk.Button(graph_buttons, text=name, command=func,
                     width=15).pack(side='left', padx=5)
        
        # Canvas for drawing graphs
        self.canvas = tk.Canvas(tab_visual, bg='white')
        self.canvas.pack(fill='both', expand=True, padx=10, pady=5)
        
    def load_file(self):
        """Load encrypted file from disk"""
        # Show file dialog
        fname = filedialog.askopenfilename(
            title="Select encrypted file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if fname:
            try:
                # Read file using file handler
                ok, data, _ = self.file_handler.read_encrypted_message(fname)
                if ok:
                    # Clear and insert new text
                    self.txt_encrypted.delete('1.0', tk.END)
                    self.txt_encrypted.insert('1.0', data)
                    # Update status
                    self.status_text.set(f"Loaded: {Path(fname).name}")
                else:
                    messagebox.showerror("Error", data)
            except Exception as err:
                messagebox.showerror("Error", f"Failed to load: {err}")
                
    def start_decryption(self):
        """Start the brute force decryption process"""
        # Get encrypted text
        enc_text = self.txt_encrypted.get('1.0', tk.END).strip()
        
        # Validate input
        if not enc_text:
            messagebox.showwarning("Empty", "Please enter encrypted text!")
            return
            
        # Update UI state
        self.btn_decrypt.config(state='disabled', text="Working...")
        self.status_text.set("Trying all shifts...")
        
        # Decryption in separate thread to prevent UI freezing
        def decrypt_work():
            try:
                # Perform brute force decryption
                shift_found, decrypted_msg = self.cipher.brute_force_decrypt(enc_text)
                
                # Return to UI thread for updates
                self.window.after(0, self._on_decrypt_done, shift_found, decrypted_msg)
            except Exception as e:
                # Handle errors in UI thread
                self.window.after(0, self._on_decrypt_error, str(e))
                
        # Start worker thread
        threading.Thread(target=decrypt_work, daemon=True).start()
        
    def _on_decrypt_done(self, shift, text):
        """Handle successful decryption completion"""
        # Reset button state
        self.btn_decrypt.config(state='normal', text="Auto Decrypt")
        
        if shift is not None:
            # Update shift display
            self.lbl_shift.config(text=str(shift))
            self.current_shift.set(shift)
            
            # Display decrypted text
            self.txt_decrypted.delete('1.0', tk.END)
            self.txt_decrypted.insert('1.0', text)
            
            # Update status
            self.status_text.set(f"Success! Shift: {shift}")
            
            # Save to history
            self.history.append({
                'time': datetime.now(),
                'shift': shift,
                'preview': text[:50]  # First 50 chars
            })
        else:
            # No valid shift found
            messagebox.showwarning("Failed", "Could not decrypt!")
            self.status_text.set("Failed")
            
    def _on_decrypt_error(self, error_msg):
        """Handle decryption error"""
        # Reset button state
        self.btn_decrypt.config(state='normal', text="Auto Decrypt")
        # Show error message
        messagebox.showerror("Error", f"Error: {error_msg}")
        self.status_text.set("Error")
        
    def save_result(self):
        """Save decrypted text to file"""
        # Get decrypted content
        content = self.txt_decrypted.get('1.0', tk.END).strip()
        
        # Check if there's content to save
        if not content:
            messagebox.showwarning("Empty", "Nothing to save!")
            return
            
        try:
            # Save using file handler
            ok, fpath = self.file_handler.save_decrypted_message(
                content, self.current_shift.get()
            )
            if ok:
                messagebox.showinfo("Saved", f"File saved:\n{fpath}")
                self.status_text.set("Saved")
            else:
                messagebox.showerror("Error", fpath)
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")
            
    def copy_to_clipboard(self):
        """Copy decrypted text to clipboard"""
        content = self.txt_decrypted.get('1.0', tk.END).strip()
        if content:
            # Clear clipboard and add content
            self.window.clipboard_clear()
            self.window.clipboard_append(content)
            self.status_text.set("Copied")
            
    def clear_enc_text(self):
        """Clear encrypted text area"""
        self.txt_encrypted.delete('1.0', tk.END)
        self.lbl_shift.config(text="--")
        
    def analyze_decrypted_text(self):
        """Analyze the decrypted text"""
        # Get decrypted content
        content = self.txt_decrypted.get('1.0', tk.END).strip()
        
        # Validate input
        if not content:
            messagebox.showwarning("Empty", "Decrypt text first!")
            return
            
        self.status_text.set("Analyzing...")
        
        # Run analysis using analyzer module
        self.analysis_results = self.analyzer.full_analysis(content)
        
        # Format and display results
        output = self._format_results()
        self.txt_analysis.delete('1.0', tk.END)
        self.txt_analysis.insert('1.0', output)
        
        # Switch to analysis tab
        self.notebook.select(1)
        self.status_text.set("Analysis done")
        
    def _format_results(self):
        """Format analysis results for display"""
        if not self.analysis_results:
            return "No data"
            
        res = self.analysis_results
        txt = "TEXT ANALYSIS RESULTS\n"
        txt += "=" * 50 + "\n\n"
        
        # Basic statistics section
        txt += "BASIC STATS:\n"
        txt += f"Characters: {res['total_chars']}\n"
        txt += f"Words: {res['word_count']}\n"
        txt += f"Unique chars: {res['unique_characters']}\n"
        txt += f"Unique words: {res['unique_words']}\n\n"
        
        # Word analysis section
        txt += "WORDS:\n"
        txt += f"Longest: '{res['longest_word']}' ({len(res['longest_word'])} chars)\n"
        txt += f"Shortest: '{res['shortest_word']}'\n"
        txt += f"Average length: {res['average_word_length']:.2f}\n"
        if 'any_word_longer_than_7' in res:
            txt += f"Has long words: {'Yes' if res['any_word_longer_than_7'] else 'No'}\n"
        txt += "\n"
        
        # Character percentages
        txt += "PERCENTAGES:\n"
        txt += f"Vowels: {res['vowel_percentage']:.1f}%\n"
        txt += f"Letters: {res['letter_percentage']:.1f}%\n"
        txt += f"Digits: {res['digit_percentage']:.1f}%\n"
        txt += f"Spaces: {res['space_percentage']:.1f}%\n\n"
        
        # Word length distribution
        txt += "WORD LENGTHS:\n"
        for len_val, cnt in sorted(res['word_length_distribution'].items()):
            txt += f"  {len_val} letters: {cnt}\n"
            
        # Top frequent words
        if res.get('top_words'):
            txt += "\nTOP WORDS:\n"
            for i, (w, c) in enumerate(res['top_words'][:10], 1):
                txt += f"  {i}. '{w}' - {c}x\n"
                
        return txt
        
    def export_results(self):
        """Export analysis results to JSON file"""
        if not self.analysis_results:
            messagebox.showwarning("No data", "Run analysis first!")
            return
            
        try:
            # Save as JSON report
            ok, path = self.file_handler.save_analysis_report(self.analysis_results)
            if ok:
                messagebox.showinfo("Exported", f"Report saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")
            
    def reencrypt(self):
        """Re-encrypt text with new shift value"""
        # Get decrypted content
        content = self.txt_decrypted.get('1.0', tk.END).strip()
        
        if not content:
            messagebox.showwarning("Empty", "No text to encrypt!")
            return
            
        # Get new shift value
        sh = self.new_shift.get()
        
        # Encrypt with new shift
        enc = self.cipher.encrypt(content, sh)
        
        # Create result window
        win = tk.Toplevel(self.window)
        win.title(f"Re-encrypted (Shift: {sh})")
        win.geometry("500x300")
        
        # Text widget for encrypted result
        txt = scrolledtext.ScrolledText(win, font=('Consolas', 11))
        txt.pack(fill='both', expand=True, padx=10, pady=10)
        txt.insert('1.0', enc)
        
        # Copy and close button
        def copy_close():
            self.window.clipboard_clear()
            self.window.clipboard_append(enc)
            win.destroy()
            
        tk.Button(win, text="Copy & Close",
                 command=copy_close).pack(pady=5)
                 
    def draw_word_length(self):
        """Draw word length histogram"""
        if not self.analysis_results:
            messagebox.showwarning("No data", "Analyze first!")
            return
            
        # Clear canvas and draw new graph
        self.canvas.delete("all")
        v = TextVisualizer(self.canvas)
        v.plot_word_length_histogram(self.analysis_results['word_length_distribution'])
        # Switch to visualizations tab
        self.notebook.select(2)
        
    def draw_chars(self):
        """Draw character type distribution pie chart"""
        if not self.analysis_results:
            messagebox.showwarning("No data", "Analyze first!")
            return
            
        self.canvas.delete("all")
        v = TextVisualizer(self.canvas)
        
        # Prepare data for pie chart
        d = {
            'Letters': self.analysis_results['letter_percentage'],
            'Digits': self.analysis_results['digit_percentage'],  
            'Spaces': self.analysis_results['space_percentage'],
            'Other': 100 - sum([  # Calculate remainder
                self.analysis_results['letter_percentage'],
                self.analysis_results['digit_percentage'],
                self.analysis_results['space_percentage']
            ])
        }
        
        v.plot_character_distribution(d)
        self.notebook.select(2)
        
    def draw_frequency(self):
        """Draw word frequency graph"""
        # Check if analysis has been performed and has top words
        if not self.analysis_results or not self.analysis_results.get('top_words'):
            messagebox.showwarning("No data", "Analyze first!")
            return
            
        self.canvas.delete("all")
        v = TextVisualizer(self.canvas)
        
        # Get top 10 words
        freqs = dict(self.analysis_results['top_words'][:10])
        v.plot_word_frequency(freqs)
        self.notebook.select(2)
        
    def draw_shifts(self):
        """Draw shift analysis graph showing scores for each shift"""
        # Check if decryption has been performed
        if not hasattr(self.cipher, 'last_attempts'):
            messagebox.showwarning("No data", "Decrypt first!")
            return
            
        self.canvas.delete("all")
        v = TextVisualizer(self.canvas)
        
        # Collect shift scores from last decryption
        data = {}
        for s, txt, score in self.cipher.last_attempts:
            data[s] = score
            
        # Draw graph with best shift highlighted
        v.plot_shift_attempts(data, self.current_shift.get())
        self.notebook.select(2)
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        # Ctrl+O: Open file
        self.window.bind('<Control-o>', lambda e: self.load_file())
        # Ctrl+S: Save result
        self.window.bind('<Control-s>', lambda e: self.save_result())
        # Ctrl+D: Start decryption
        self.window.bind('<Control-d>', lambda e: self.start_decryption())
        
    def show_about_dialog(self):
        """Show about dialog with project information"""
        messagebox.showinfo(
            "About",
            "Secret Message Decoder\n\n"
            "Caesar Cipher Project\n"
            "Python Final Project\n\n"
            "Features:\n"
            "• Auto decrypt (brute force)\n"
            "• Text analysis\n"
            "• Graphs & visualizations\n"
            "• File I/O"
        )
        
    def run(self):
        """Start the application main loop"""
        self.window.mainloop()


if __name__ == "__main__":
    app = SecretMessageApp()
    app.run()