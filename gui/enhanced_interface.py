import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
from pathlib import Path
from typing import Dict, Any
import threading
import time
from datetime import datetime

from modules.cipher import CaesarCipher
from modules.text_analyzer import TextAnalyzer
from modules.file_handler import FileHandler
from modules.visualizer import TextVisualizer


class SecretMessageApp:
    """Main application class for Secret Message Decoder"""
    
    def __init__(self):
        # Initialize main window
        self.window = tk.Tk()
        self.window.title("Secret Message Decoder")
        self.window.geometry("1200x750")
        self.window.minsize(900, 600)
        
        # Initialize modules for different functionalities
        self.cipher = CaesarCipher()
        self.analyzer = TextAnalyzer()
        self.file_handler = FileHandler()
        
        # Variables to track current state
        self.current_shift = tk.IntVar(value=0)  # Stores detected shift value
        self.new_shift = tk.IntVar(value=1)      # For re-encryption
        self.analysis_results = {}               # Stores analysis data
        self.history_list = []                   # Stores decryption history
        
        # Build the UI
        self._init_ui()
        self._center_window()
        
    def _init_ui(self):
        """Initialize user interface components"""
        # Create header with title
        self._create_header()
        
        # Setup menu bar
        self._setup_menus()
        
        # Main container for tabs
        main_container = tk.Frame(self.window, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create notebook widget for tabs
        self.tabs = ttk.Notebook(main_container)
        self.tabs.pack(fill='both', expand=True)
        
        # Create individual tabs
        self._make_decrypt_tab()
        self._make_analysis_tab()
        self._make_graphs_tab()
        self._make_history_tab()
        
        # Status bar at bottom
        self.status_text = tk.StringVar(value="Ready")
        statusbar = tk.Label(self.window, textvariable=self.status_text,
                            bd=1, relief='sunken', anchor='w')
        statusbar.pack(side='bottom', fill='x')
    
    def _create_header(self):
        """Create application header"""
        # Create blue header panel
        header_panel = tk.Frame(self.window, bg='#4287f5', height=60)
        header_panel.pack(fill='x')
        header_panel.pack_propagate(False)  # Maintain fixed height
        
        # Add title label
        lbl = tk.Label(header_panel, text="🔐 Secret Message Decoder", 
                      font=('Arial', 20, 'bold'),
                      bg='#4287f5', fg='white')
        lbl.pack(expand=True)
    
    def _setup_menus(self):
        """Setup menu bar"""
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        
        # File menu
        filemenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=self.open_encrypted_file)
        filemenu.add_command(label="Save", command=self.save_result)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.window.quit)
        
        # Edit menu
        editmenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Clear", command=self.clear_everything)
        editmenu.add_command(label="Copy", command=self.copy_decrypted)
        
        # Help menu
        helpmenu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.about_dialog)
    
    def _make_decrypt_tab(self):
        """Create decryption tab"""
        decrypt_tab = tk.Frame(self.tabs, bg='#f0f0f0')
        self.tabs.add(decrypt_tab, text='Decrypt')
        
        # Upper section for encrypted text
        encrypted_section = tk.LabelFrame(decrypt_tab, text="Encrypted Message", 
                                         padx=10, pady=10)
        encrypted_section.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Text area for encrypted message
        self.encrypted_input = scrolledtext.ScrolledText(
            encrypted_section, height=8, wrap=tk.WORD, font=('Consolas', 11)
        )
        self.encrypted_input.pack(fill='both', expand=True)
        
        # Button row below text area
        buttons_row = tk.Frame(encrypted_section)
        buttons_row.pack(fill='x', pady=(10, 0))
        
        # Load file button
        load_btn = tk.Button(buttons_row, text="Load File", 
                            command=self.open_encrypted_file)
        load_btn.pack(side='left', padx=5)
        
        # Auto decrypt button (main action)
        self.decrypt_button = tk.Button(buttons_row, text="Auto Decrypt", 
                                       command=self.start_decryption,
                                       bg='#4287f5', fg='white',
                                       font=('Arial', 10, 'bold'))
        self.decrypt_button.pack(side='left', padx=5)
        
        # Clear button
        clear_btn = tk.Button(buttons_row, text="Clear", 
                            command=lambda: self.encrypted_input.delete('1.0', tk.END))
        clear_btn.pack(side='left', padx=5)
        
        # Shift display on the right side
        shift_display = tk.Frame(buttons_row)
        shift_display.pack(side='right', padx=10)
        
        tk.Label(shift_display, text="Shift:").pack(side='left')
        self.shift_number = tk.Label(shift_display, text="--", 
                                    font=('Arial', 14, 'bold'), fg='#4287f5')
        self.shift_number.pack(side='left', padx=5)
        
        # Progress bar (initially hidden)
        self.loading_bar = ttk.Progressbar(encrypted_section, mode='indeterminate')
        
        # Lower section for decrypted text
        self._create_decrypted_section(decrypt_tab)
    
    def _create_decrypted_section(self, parent):
        """Create decrypted message section"""
        decrypted_section = tk.LabelFrame(parent, text="Decrypted Message", 
                                         padx=10, pady=10)
        decrypted_section.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Text area with light green background for decrypted text
        self.decrypted_output = scrolledtext.ScrolledText(
            decrypted_section, height=8, wrap=tk.WORD, 
            font=('Consolas', 11), bg='#e8ffe8'
        )
        self.decrypted_output.pack(fill='both', expand=True)
        
        # Action buttons below text
        bottom_buttons = tk.Frame(decrypted_section)
        bottom_buttons.pack(fill='x', pady=(10, 0))
        
        # Save button with green color
        save_button = tk.Button(bottom_buttons, text="Save", 
                               command=self.save_result,
                               bg='#28a745', fg='white')
        save_button.pack(side='left', padx=5)
        
        copy_button = tk.Button(bottom_buttons, text="Copy", 
                               command=self.copy_decrypted)
        copy_button.pack(side='left', padx=5)
        
        analyze_button = tk.Button(bottom_buttons, text="Analyze", 
                                  command=self.run_analysis)
        analyze_button.pack(side='left', padx=5)
        
        # Re-encryption controls on the right
        reencrypt_area = tk.Frame(bottom_buttons)
        reencrypt_area.pack(side='right', padx=10)
        
        tk.Label(reencrypt_area, text="New shift:").pack(side='left')
        
        # Spinbox for selecting new shift value (1-25)
        spinbox_shift = tk.Spinbox(reencrypt_area, from_=1, to=25, width=5,
                                  textvariable=self.new_shift)
        spinbox_shift.pack(side='left', padx=5)
        
        reenc_btn = tk.Button(reencrypt_area, text="Re-encrypt",
                             command=self.do_reencrypt)
        reenc_btn.pack(side='left')
    
    def _make_analysis_tab(self):
        """Create analysis tab"""
        analysis_tab = tk.Frame(self.tabs, bg='#f0f0f0')
        self.tabs.add(analysis_tab, text='Analysis')
        
        # Control buttons at top
        top_panel = tk.Frame(analysis_tab)
        top_panel.pack(fill='x', padx=10, pady=10)
        
        # Analyze button
        analyze_btn = tk.Button(top_panel, text="Analyze Text",
                               command=self.run_analysis,
                               bg='#4287f5', fg='white',
                               font=('Arial', 10, 'bold'))
        analyze_btn.pack(side='left', padx=5)
        
        # Export button for saving results
        export_btn = tk.Button(top_panel, text="Export",
                              command=self.export_results)
        export_btn.pack(side='left', padx=5)
        
        # Results display area
        results_area = tk.LabelFrame(analysis_tab, text="Results", padx=10, pady=10)
        results_area.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Text widget for analysis results
        self.results_display = scrolledtext.ScrolledText(
            results_area, wrap=tk.WORD, font=('Consolas', 10)
        )
        self.results_display.pack(fill='both', expand=True)
    
    def _make_graphs_tab(self):
        """Create visualization tab"""
        graphs_tab = tk.Frame(self.tabs, bg='#f0f0f0')
        self.tabs.add(graphs_tab, text='Graphs')
        
        # Graph selection buttons
        graph_buttons = tk.Frame(graphs_tab)
        graph_buttons.pack(fill='x', padx=10, pady=10)
        
        # Create button for each graph type
        word_len_btn = tk.Button(graph_buttons, text="Word Length",
                                command=self.draw_word_length)
        word_len_btn.pack(side='left', padx=5)
        
        char_btn = tk.Button(graph_buttons, text="Characters",
                            command=self.draw_char_types)
        char_btn.pack(side='left', padx=5)
        
        freq_btn = tk.Button(graph_buttons, text="Frequency",
                            command=self.draw_word_freq)
        freq_btn.pack(side='left', padx=5)
        
        shifts_btn = tk.Button(graph_buttons, text="Shifts",
                              command=self.draw_shift_analysis)
        shifts_btn.pack(side='left', padx=5)
        
        # Canvas for drawing graphs
        graph_area = tk.LabelFrame(graphs_tab, text="Graph", padx=10, pady=10)
        graph_area.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.graph_canvas = tk.Canvas(graph_area, bg='white')
        self.graph_canvas.pack(fill='both', expand=True)
    
    def _make_history_tab(self):
        """Create history tab"""
        hist_tab = tk.Frame(self.tabs, bg='#f0f0f0')
        self.tabs.add(hist_tab, text='History')
        
        history_area = tk.LabelFrame(hist_tab, text="Previous Decryptions", 
                                    padx=10, pady=10)
        history_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview for table display
        cols = ('Time', 'Message', 'Shift')
        self.history_table = ttk.Treeview(history_area, columns=cols, 
                                         show='headings', height=15)
        
        # Configure columns
        self.history_table.heading('Time', text='Time')
        self.history_table.heading('Message', text='Message')
        self.history_table.heading('Shift', text='Shift')
        
        # Set column widths
        self.history_table.column('Time', width=150)
        self.history_table.column('Message', width=400)
        self.history_table.column('Shift', width=80)
        
        # Add scrollbar
        scroll = ttk.Scrollbar(history_area, orient='vertical', 
                              command=self.history_table.yview)
        self.history_table.configure(yscrollcommand=scroll.set)
        
        # Pack table and scrollbar
        self.history_table.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        
        # Clear history button
        clear_hist_btn = tk.Button(history_area, text="Clear", 
                                  command=self.clear_hist)
        clear_hist_btn.pack(pady=10)
    
    def _center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        
        # Get window dimensions
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        
        # Calculate center position
        x = (self.window.winfo_screenwidth() // 2) - (w // 2)
        y = (self.window.winfo_screenheight() // 2) - (h // 2)
        
        # Set window position
        self.window.geometry(f'{w}x{h}+{x}+{y}')
    
    def update_status(self, text):
        """Update status bar text"""
        self.status_text.set(text)
        self.window.update_idletasks()
    
    def open_encrypted_file(self):
        """Open and load encrypted file"""
        # Show file dialog
        fname = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[("Text", "*.txt"), ("All", "*.*")]
        )
        
        if fname:
            try:
                # Read file using file handler
                ok, data, _ = self.file_handler.read_encrypted_message(fname)
                if ok:
                    # Clear existing text
                    self.encrypted_input.delete('1.0', tk.END)
                    # Insert new text
                    self.encrypted_input.insert('1.0', data)
                    # Update status
                    self.update_status(f"Loaded: {Path(fname).name}")
                else:
                    messagebox.showerror("Error", data)
            except Exception as err:
                messagebox.showerror("Error", str(err))
    
    def start_decryption(self):
        """Start brute force decryption process"""
        # Get encrypted text from input
        enc_text = self.encrypted_input.get('1.0', tk.END).strip()
        
        # Validate input
        if not enc_text:
            messagebox.showwarning("Empty", "Enter encrypted text!")
            return
        
        # Show progress bar
        self.loading_bar.pack(fill='x', pady=5)
        self.loading_bar.start(10)  # Start animation
        self.decrypt_button.config(state='disabled')  # Disable button during process
        self.update_status("Working...")
        
        # Define worker function for threading
        def work():
            try:
                # Perform brute force decryption
                found_shift, decrypted_text = self.cipher.brute_force_decrypt(enc_text)
                time.sleep(0.5)  # Brief delay for visual feedback
                
                # Return to main thread for GUI update
                self.window.after(0, self._finish_decryption, 
                                 found_shift, decrypted_text, enc_text)
            except Exception as e:
                # Handle errors in main thread
                self.window.after(0, self._decryption_failed, str(e))
        
        # Start worker thread
        threading.Thread(target=work, daemon=True).start()
    
    def _finish_decryption(self, shift, text, original):
        """Complete decryption process"""
        # Stop and hide progress bar
        self.loading_bar.stop()
        self.loading_bar.pack_forget()
        self.decrypt_button.config(state='normal')  # Re-enable button
        
        if shift is not None:
            # Update shift display
            self.shift_number.config(text=str(shift))
            self.current_shift.set(shift)
            
            # Display decrypted text
            self.decrypted_output.delete('1.0', tk.END)
            self.decrypted_output.insert('1.0', text)
            
            # Save to history
            self._save_to_history(original, text, shift)
            
            # Update status
            self.update_status(f"Done! Shift: {shift}")
        else:
            # Decryption failed
            messagebox.showwarning("Failed", "Could not decrypt")
            self.update_status("Failed")
    
    def _decryption_failed(self, error_msg):
        """Handle decryption failure"""
        # Clean up progress bar
        self.loading_bar.stop()
        self.loading_bar.pack_forget()
        self.decrypt_button.config(state='normal')
        
        # Show error
        messagebox.showerror("Error", error_msg)
        self.update_status("Error")
    
    def save_result(self):
        """Save decrypted text to file"""
        # Get decrypted text
        content = self.decrypted_output.get('1.0', tk.END).strip()
        
        # Check if there's content to save
        if not content:
            messagebox.showwarning("Empty", "Nothing to save!")
            return
        
        try:
            # Save using file handler
            ok, path = self.file_handler.save_decrypted_message(
                content, self.current_shift.get()
            )
            if ok:
                messagebox.showinfo("Saved", f"File saved: {path}")
                self.update_status("Saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def copy_decrypted(self):
        """Copy decrypted text to clipboard"""
        content = self.decrypted_output.get('1.0', tk.END).strip()
        if content:
            # Clear clipboard and add new content
            self.window.clipboard_clear()
            self.window.clipboard_append(content)
            self.update_status("Copied")
    
    def clear_everything(self):
        """Clear all text fields"""
        # Clear all text areas
        self.encrypted_input.delete('1.0', tk.END)
        self.decrypted_output.delete('1.0', tk.END)
        self.results_display.delete('1.0', tk.END)
        
        # Reset shift display
        self.shift_number.config(text="--")
        self.current_shift.set(0)
        
        self.update_status("Cleared")
    
    def run_analysis(self):
        """Run text analysis on decrypted text"""
        # Get decrypted text
        content = self.decrypted_output.get('1.0', tk.END).strip()
        
        # Validate input
        if not content:
            messagebox.showwarning("Empty", "Decrypt text first!")
            return
        
        self.update_status("Analyzing...")
        
        # Perform analysis using analyzer module
        self.analysis_results = self.analyzer.full_analysis(content)
        
        # Format and display results
        output = self._build_analysis_text()
        self.results_display.delete('1.0', tk.END)
        self.results_display.insert('1.0', output)
        
        # Switch to analysis tab
        self.tabs.select(1)
        self.update_status("Analysis done")
    
    def _build_analysis_text(self):
        """Build formatted analysis text for display"""
        if not self.analysis_results:
            return ""
        
        res = self.analysis_results
        txt = "=== ANALYSIS RESULTS ===\n\n"
        
        # Basic statistics
        txt += f"Characters: {res['total_chars']}\n"
        txt += f"Words: {res['word_count']}\n"
        txt += f"Unique words: {res['unique_words']}\n\n"
        
        # Word analysis
        txt += f"Longest word: '{res['longest_word']}'\n"
        txt += f"Shortest: '{res['shortest_word']}'\n"
        txt += f"Avg length: {res['average_word_length']:.1f}\n\n"
        
        # Character percentages
        txt += f"Vowels: {res['vowel_percentage']:.1f}%\n"
        txt += f"Letters: {res['letter_percentage']:.1f}%\n"
        txt += f"Digits: {res['digit_percentage']:.1f}%\n"
        txt += f"Spaces: {res['space_percentage']:.1f}%\n\n"
        
        # Word length distribution
        txt += "Word lengths:\n"
        for l, c in sorted(res['word_length_distribution'].items()):
            txt += f"  {l}: {c} words\n"
        
        return txt
    
    def export_results(self):
        """Export analysis results to JSON file"""
        if not self.analysis_results:
            messagebox.showwarning("Empty", "No analysis!")
            return
        
        try:
            # Save as JSON using file handler
            ok, fpath = self.file_handler.save_analysis_report(self.analysis_results)
            if ok:
                messagebox.showinfo("Exported", f"Saved: {fpath}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def do_reencrypt(self):
        """Re-encrypt text with new shift"""
        # Get decrypted text
        content = self.decrypted_output.get('1.0', tk.END).strip()
        
        if not content:
            messagebox.showwarning("Empty", "No text!")
            return
        
        # Get new shift value
        sh = self.new_shift.get()
        
        # Encrypt with new shift
        encrypted_again = self.cipher.encrypt(content, sh)
        
        # Create popup window for result
        popup = tk.Toplevel(self.window)
        popup.title(f"Encrypted with shift {sh}")
        popup.geometry("500x300")
        
        # Add text widget to popup
        txt_widget = scrolledtext.ScrolledText(popup, wrap=tk.WORD)
        txt_widget.pack(fill='both', expand=True, padx=10, pady=10)
        txt_widget.insert('1.0', encrypted_again)
        
        # Add close button
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)
    
    def draw_word_length(self):
        """Draw word length histogram"""
        if not self.analysis_results:
            messagebox.showwarning("Empty", "Analyze first!")
            return
        
        # Clear canvas and draw new graph
        self.graph_canvas.delete("all")
        viz = TextVisualizer(self.graph_canvas)
        viz.plot_word_length_histogram(self.analysis_results['word_length_distribution'])
        
        # Switch to graphs tab
        self.tabs.select(2)
    
    def draw_char_types(self):
        """Draw character type distribution"""
        if not self.analysis_results:
            messagebox.showwarning("Empty", "Analyze first!")
            return
        
        self.graph_canvas.delete("all")
        viz = TextVisualizer(self.graph_canvas)
        
        # Calculate percentages for each character type
        data = {
            'Letters': self.analysis_results['letter_percentage'],
            'Digits': self.analysis_results['digit_percentage'],
            'Spaces': self.analysis_results['space_percentage'],
            'Other': 100 - sum([  # Calculate remainder
                self.analysis_results['letter_percentage'],
                self.analysis_results['digit_percentage'],
                self.analysis_results['space_percentage']
            ])
        }
        
        viz.plot_character_distribution(data)
        self.tabs.select(2)
    
    def draw_word_freq(self):
        """Draw word frequency graph"""
        if not self.analysis_results:
            messagebox.showwarning("Empty", "Analyze first!")
            return
        
        self.graph_canvas.delete("all")
        viz = TextVisualizer(self.graph_canvas)
        
        # Get top 10 words if available
        if self.analysis_results.get('top_words'):
            freqs = dict(self.analysis_results['top_words'][:10])
            viz.plot_word_frequency(freqs)
        
        self.tabs.select(2)
    
    def draw_shift_analysis(self):
        """Draw shift analysis graph"""
        # Get encrypted text
        enc = self.encrypted_input.get('1.0', tk.END).strip()
        
        # Check if decryption has been performed
        if not enc or not hasattr(self.cipher, 'last_attempts'):
            messagebox.showwarning("Empty", "Decrypt first!")
            return
        
        self.graph_canvas.delete("all")
        viz = TextVisualizer(self.graph_canvas)
        
        # Collect shift scores from last decryption attempt
        shift_scores = {}
        for s, t, score in self.cipher.last_attempts:
            shift_scores[s] = score
        
        # Draw graph with best shift highlighted
        viz.plot_shift_attempts(shift_scores, self.current_shift.get())
        self.tabs.select(2)
    
    def _save_to_history(self, enc, dec, sh):
        """Save decryption to history"""
        # Create history entry
        item = {
            'time': datetime.now(),
            'enc': enc[:50] + '...' if len(enc) > 50 else enc,  # Truncate long text
            'dec': dec[:50] + '...' if len(dec) > 50 else dec,
            'shift': sh
        }
        
        # Add to history list
        self.history_list.append(item)
        self._refresh_history_view()
    
    def _refresh_history_view(self):
        """Refresh history table display"""
        # Clear existing items
        for i in self.history_table.get_children():
            self.history_table.delete(i)
        
        # Add last 20 items in reverse order (newest first)
        for item in reversed(self.history_list[-20:]):
            self.history_table.insert('', 'end', values=(
                item['time'].strftime('%H:%M:%S'),
                item['dec'],
                item['shift']
            ))
    
    def clear_hist(self):
        """Clear history"""
        if messagebox.askyesno("Clear", "Delete history?"):
            self.history_list.clear()
            self._refresh_history_view()
    
    def about_dialog(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Secret Message Decoder\n"
            "Caesar cipher project\n"
            "Version 1.0"
        )
    
    def run(self):
        """Run the application"""
        self.window.mainloop()


if __name__ == "__main__":
    app = SecretMessageApp()
    app.run()