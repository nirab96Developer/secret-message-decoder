import tkinter as tk
from tkinter import Canvas
import math
from collections import Counter


class TextVisualizer:
    """
    Class for creating text analysis visualizations
    
    Creates various graphs and charts for displaying text analysis results
    including histograms, pie charts, and line graphs.
    """
    
    def __init__(self, canvas):
        """
        Initialize visualizer with a canvas
        
        Args:
            canvas: Tkinter Canvas widget for drawing
        """
        self.canvas = canvas
        
        # Simple color scheme
        self.colors = {
            'bar': '#4287f5',      # Blue for main bars
            'bar2': '#f54242',     # Red for secondary bars
            'text': '#333333',     # Dark gray for text
            'bg': '#ffffff',       # White background
            'line': '#666666'      # Gray for lines
        }
    
    def plot_word_length_histogram(self, word_length_dist):
        """
        Create histogram showing word length distribution
        
        Args:
            word_length_dist: Dictionary mapping word length to count
        """
        # Clear canvas
        self.canvas.delete("all")
        
        # Check if data exists
        if not word_length_dist:
            self.canvas.create_text(400, 250, text="No data", font=("Arial", 16))
            return
        
        # Canvas dimensions
        width = 800
        height = 500
        margin = 60
        
        # Calculate maximum height for scaling
        max_count = max(word_length_dist.values())
        sorted_items = sorted(word_length_dist.items())
        num_bars = len(sorted_items)
        
        if num_bars == 0:
            return
        
        # Calculate bar dimensions
        bar_width = (width - 2 * margin) / num_bars * 0.8  # 80% for bars
        spacing = (width - 2 * margin) / num_bars * 0.2   # 20% for spacing
        
        # Draw title
        self.canvas.create_text(width // 2, 30,
                               text="Word Length Distribution",
                               font=("Arial", 18, "bold"))
        
        # Draw bars
        for i, (length, count) in enumerate(sorted_items):
            # Calculate bar height proportionally
            bar_height = (count / max_count) * (height - 100)
            
            # Calculate bar position
            x = margin + i * (bar_width + spacing)
            y_bottom = height - 50
            y_top = y_bottom - bar_height
            
            # Draw bar
            self.canvas.create_rectangle(x, y_top, x + bar_width, y_bottom,
                                        fill=self.colors['bar'], outline="")
            
            # Draw count above bar
            self.canvas.create_text(x + bar_width / 2, y_top - 10,
                                   text=str(count), font=("Arial", 10))
            
            # Draw length below bar
            self.canvas.create_text(x + bar_width / 2, y_bottom + 15,
                                   text=str(length), font=("Arial", 10))
        
        # Draw baseline
        self.canvas.create_line(margin, height - 50, width - margin, height - 50,
                               width=2, fill=self.colors['line'])
        
        # X-axis label
        self.canvas.create_text(width // 2, height - 10,
                               text="Word Length (characters)",
                               font=("Arial", 10))
    
    def plot_character_distribution(self, char_data):
        """
        Create pie chart showing character type distribution
        
        Args:
            char_data: Dictionary with character type percentages
        """
        # Clear canvas
        self.canvas.delete("all")
        
        # Check if data exists
        if not char_data or sum(char_data.values()) == 0:
            self.canvas.create_text(400, 250, text="No data", font=("Arial", 16))
            return
        
        # Center and radius for pie chart
        cx = 400
        cy = 250
        radius = 150
        
        # Calculate percentages
        total = sum(char_data.values())
        percentages = {k: (v / total) * 100 for k, v in char_data.items()}
        
        # Color scheme for different character types
        type_colors = {
            'Letters': '#4287f5',  # Blue
            'Digits': '#42f554',   # Green
            'Spaces': '#cccccc',   # Light gray
            'Other': '#f5a442'     # Orange
        }
        
        # Draw title
        self.canvas.create_text(cx, 50,
                               text="Character Type Distribution",
                               font=("Arial", 18, "bold"))
        
        start = 0
        legend_y = 420
        
        # Draw pie slices
        for char_type, percent in percentages.items():
            if percent > 0:
                # Calculate slice angle
                extent = (percent / 100) * 360
                color = type_colors.get(char_type, '#999999')
                
                # Draw pie slice
                self.canvas.create_arc(cx - radius, cy - radius,
                                      cx + radius, cy + radius,
                                      start=start, extent=extent,
                                      fill=color, outline="white", width=2)
                
                # Add percentage label if slice is large enough
                if percent > 10:
                    # Calculate label position
                    angle = math.radians(start + extent / 2)
                    label_x = cx + radius * 0.6 * math.cos(angle)
                    label_y = cy - radius * 0.6 * math.sin(angle)
                    self.canvas.create_text(label_x, label_y,
                                          text=f"{percent:.1f}%",
                                          font=("Arial", 11, "bold"),
                                          fill="white")
                
                start += extent
        
        # Draw legend
        x_legend = 100
        i = 0
        for char_type, percent in percentages.items():
            if percent > 0:
                color = type_colors.get(char_type, '#999999')
                y = legend_y + i * 25
                
                # Color square
                self.canvas.create_rectangle(x_legend, y - 8, x_legend + 20, y + 8,
                                            fill=color, outline="")
                
                # Label text
                self.canvas.create_text(x_legend + 30, y,
                                      text=f"{char_type}: {percent:.1f}%",
                                      font=("Arial", 10), anchor="w")
                i += 1
    
    def plot_word_frequency(self, word_freq):
        """
        Create horizontal bar chart for word frequency
        
        Args:
            word_freq: Dictionary mapping words to their frequency counts
        """
        # Clear canvas
        self.canvas.delete("all")
        
        # Check if data exists
        if not word_freq:
            self.canvas.create_text(400, 250, text="No data", font=("Arial", 16))
            return
        
        # Get top 10 words
        top_words = list(word_freq.items())[:10]
        
        if not top_words:
            return
        
        # Canvas dimensions
        width = 800
        height = 500
        margin = 100
        
        # Draw title
        self.canvas.create_text(width // 2, 30,
                               text=f"Top {len(top_words)} Most Frequent Words",
                               font=("Arial", 18, "bold"))
        
        # Calculate bar dimensions
        bar_height = (height - 100) / len(top_words) * 0.7  # 70% for bars
        spacing = (height - 100) / len(top_words) * 0.3     # 30% for spacing
        
        # Find maximum frequency for scaling
        max_freq = max(freq for _, freq in top_words)
        
        # Draw horizontal bars
        for i, (word, freq) in enumerate(top_words):
            # Calculate bar position
            y = 80 + i * (bar_height + spacing)
            # Calculate bar width proportionally
            bar_width = (freq / max_freq) * (width - 2 * margin - 100)
            
            # Draw bar
            self.canvas.create_rectangle(margin, y, margin + bar_width, y + bar_height,
                                        fill=self.colors['bar2'], outline="")
            
            # Word label on left
            self.canvas.create_text(margin - 10, y + bar_height / 2,
                                   text=word[:15],  # Truncate long words
                                   font=("Arial", 10), anchor="e")
            
            # Frequency count on right
            self.canvas.create_text(margin + bar_width + 10, y + bar_height / 2,
                                   text=str(freq), font=("Arial", 10), anchor="w")
    
    def plot_shift_attempts(self, shifts_data, best_shift):
        """
        Create line graph showing Caesar cipher shift analysis
        
        Args:
            shifts_data: Dictionary mapping shift values to scores
            best_shift: The optimal shift value found
        """
        # Clear canvas
        self.canvas.delete("all")
        
        if not shifts_data:
            return
        
        # Canvas dimensions
        width = 800
        height = 500
        margin = 60
        
        # Sort shifts by value
        sorted_shifts = sorted(shifts_data.items())
        max_score = max(score for _, score in sorted_shifts) if sorted_shifts else 1
        
        # Draw title
        self.canvas.create_text(width // 2, 30,
                               text="Caesar Cipher Shift Analysis",
                               font=("Arial", 18, "bold"))
        
        # Calculate points for line graph
        points = []
        x_step = (width - 2 * margin) / 25  # 26 possible shifts (0-25)
        
        for shift, score in sorted_shifts:
            # Calculate x position based on shift value
            x = margin + shift * x_step
            # Calculate y position based on score
            y = height - 50 - (score / max_score) * (height - 100)
            points.extend([x, y])
        
        # Draw line connecting points
        if len(points) >= 4:
            self.canvas.create_line(points, fill=self.colors['bar'], width=2)
        
        # Draw individual points
        for i in range(0, len(points), 2):
            x, y = points[i], points[i + 1]
            shift = i // 2
            
            if shift == best_shift:
                # Highlight best shift with larger point
                self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6,
                                      fill='#00ff00', outline="black", width=2)
                # Label for best shift
                self.canvas.create_text(x, y - 15,
                                      text=f"Best: {shift}",
                                      font=("Arial", 10, "bold"),
                                      fill='#00ff00')
            else:
                # Regular point for other shifts
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                      fill=self.colors['bar'], outline="")
        
        # Draw axes
        # X-axis
        self.canvas.create_line(margin, height - 50, width - margin, height - 50,
                               width=2)
        # Y-axis
        self.canvas.create_line(margin, 80, margin, height - 50,
                               width=2)
        
        # X-axis numbers (every 5 shifts)
        for shift in range(0, 26, 5):
            x = margin + shift * x_step
            self.canvas.create_text(x, height - 30,
                                   text=str(shift), font=("Arial", 9))
        
        # X-axis label
        self.canvas.create_text(width // 2, height - 10,
                               text="Shift Value",
                               font=("Arial", 10))
        
        # Y-axis label (rotated)
        self.canvas.create_text(30, height // 2,
                               text="Score", font=("Arial", 10), angle=90)


# Helper function
def create_simple_chart(canvas, title, data):
    """
    Create a simple text-based chart
    
    Args:
        canvas: Canvas widget to draw on
        title: Chart title
        data: Dictionary with data to display
    
    Returns:
        Canvas with the chart drawn
    """
    # Clear canvas
    canvas.delete("all")
    
    # Draw title
    canvas.create_text(400, 30, text=title, font=("Arial", 16, "bold"))
    
    # Draw data as text list
    y = 80
    for key, value in data.items():
        canvas.create_text(100, y, text=f"{key}: {value}", 
                          font=("Arial", 11), anchor="w")
        y += 30
    
    return canvas