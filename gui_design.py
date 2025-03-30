import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import platform

class ModernUI:
    def __init__(self, send_message_callback):
        """
        Creates a modern GUI for the Medical AI Assistant.
        send_message_callback: A function to be called when the "Send" button is clicked.
        """
        self.send_message_callback = send_message_callback
        self.setup_root()
        self.create_styles()
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        
    def setup_root(self):
        """Set up the main window with proper sizing and icon"""
        self.root = tk.Tk()
        self.root.title("Medical AI Assistant")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Set system-specific configurations
        if platform.system() == "Windows":
            self.root.iconbitmap("medical_icon.ico") if os.path.exists("medical_icon.ico") else None
        elif platform.system() == "Darwin":  # macOS
            # macOS handles icons differently
            pass
        
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # Menu
        self.root.grid_rowconfigure(1, weight=1)  # Content
        self.root.grid_rowconfigure(2, weight=0)  # Status bar
        
    def create_styles(self):
        """Create ttk styles for a modern look"""
        self.style = ttk.Style()
        
        # Configure the theme - use 'clam' as it's more customizable
        if platform.system() == "Windows":
            self.style.theme_use('vista')
        else:
            self.style.theme_use('clam')
            
        # Configure button style
        self.style.configure('TButton', padding=6, relief="flat", background="#4a7abc")
        self.style.map('TButton',
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '!disabled', '#3d6ca8'), ('active', '#5a8adc')])
                  
        # Configure frame style
        self.style.configure('Main.TFrame', background='#f0f0f0')
        self.style.configure('Header.TFrame', background='#e0e0e0')
        
        # Configure label style
        self.style.configure('Header.TLabel', background='#e0e0e0', font=('Arial', 12, 'bold'))
        self.style.configure('Status.TLabel', background='#e0e0e0', relief='sunken', anchor='w')
        
    def create_menu(self):
        """Create a menu bar with options"""
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Conversation", command=self.new_conversation)
        file_menu.add_command(label="Save Conversation", command=self.save_conversation)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label="Clear Input", command=self.clear_input)
        edit_menu.add_command(label="Clear Output", command=self.clear_output)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Help", command=self.show_help)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=self.menu_bar)
        
    def create_main_frame(self):
        """Create the main content frame with input and output areas"""
        # Main content frame
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Configure rows for content
        self.main_frame.grid_rowconfigure(0, weight=0)  # Input header
        self.main_frame.grid_rowconfigure(1, weight=1)  # Input area
        self.main_frame.grid_rowconfigure(2, weight=0)  # Button area
        self.main_frame.grid_rowconfigure(3, weight=0)  # Output header
        self.main_frame.grid_rowconfigure(4, weight=2)  # Output area
        
        # Input section
        input_header = ttk.Frame(self.main_frame, style='Header.TFrame')
        input_header.grid(row=0, column=0, sticky="ew", pady=(5, 0))
        input_label = ttk.Label(input_header, text="Enter your medical query:", style='Header.TLabel')
        input_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Input text area with modern styling
        self.input_text = scrolledtext.ScrolledText(
            self.main_frame, 
            height=5, 
            width=60, 
            font=('Arial', 10),
            wrap=tk.WORD,
            borderwidth=1,
            relief="solid"
        )
        self.input_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        
        # Clear button
        self.clear_btn = ttk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_input,
            style='TButton'
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Send button
        self.send_btn = ttk.Button(
            button_frame, 
            text="Send", 
            command=self.send_message,
            style='TButton'
        )
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_header = ttk.Frame(self.main_frame, style='Header.TFrame')
        output_header.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        output_label = ttk.Label(output_header, text="AI Assistant's Response:", style='Header.TLabel')
        output_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        # View log button in the output header
        self.log_btn = ttk.Button(
            output_header, 
            text="View Log", 
            command=self.show_log,
            style='TButton'
        )
        self.log_btn.pack(side=tk.RIGHT, padx=5)
        
        # Output text area with modern styling
        self.output_text = scrolledtext.ScrolledText(
            self.main_frame, 
            height=15, 
            width=60, 
            font=('Arial', 10),
            wrap=tk.WORD,
            borderwidth=1,
            relief="solid",
            state="disabled"  # Make it read-only initially
        )
        self.output_text.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)
        
    def create_status_bar(self):
        """Create a status bar at the bottom of the window"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.grid(row=2, column=0, sticky="ew")
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(
            self.status_frame, 
            text="Ready", 
            style='Status.TLabel'
        )
        self.status_label.grid(row=0, column=0, sticky="ew")
        
    def send_message(self):
        """Handle the send button click"""
        # Enable the output text for modification
        self.output_text.config(state="normal")
        
        # Update status
        self.status_label.config(text="Processing request...")
        self.root.update_idletasks()
        
        # Call the callback function
        self.send_message_callback(self.input_text, self.output_text)
        
        # Update status
        self.status_label.config(text="Ready")
        
        # Disable the output text to make it read-only
        self.output_text.config(state="disabled")
        
    def show_log(self):
        """Creates a new window to display the log."""
        log_window = tk.Toplevel(self.root)
        log_window.title("AI Conversation Log")
        log_window.geometry("700x500")
        log_window.minsize(500, 400)
        
        # Make the window modal
        log_window.transient(self.root)
        log_window.grab_set()
        
        # Configure the grid
        log_window.grid_columnconfigure(0, weight=1)
        log_window.grid_rowconfigure(0, weight=1)
        log_window.grid_rowconfigure(1, weight=0)
        
        # Get content from output
        self.output_text.config(state="normal")
        log_content = self.output_text.get("1.0", tk.END)
        self.output_text.config(state="disabled")
        
        # Log text area
        log_text = scrolledtext.ScrolledText(
            log_window, 
            height=20, 
            width=80,
            font=('Arial', 10),
            wrap=tk.WORD
        )
        log_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        log_text.insert(tk.END, log_content)
        log_text.config(state="disabled")  # Make it read-only
        
        # Button frame
        button_frame = ttk.Frame(log_window)
        button_frame.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        
        # Close button
        close_btn = ttk.Button(
            button_frame, 
            text="Close", 
            command=log_window.destroy,
            style='TButton'
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Save button
        save_btn = ttk.Button(
            button_frame, 
            text="Save Log", 
            command=lambda: self.save_log(log_content),
            style='TButton'
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
    def save_log(self, content):
        """Save the log content to a file"""
        from tkinter import filedialog
        import datetime
        
        # Generate default filename with timestamp
        default_filename = f"medical_ai_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Open file dialog
        filename = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(content)
            messagebox.showinfo("Save Log", f"Log saved successfully to {filename}")
            
    def clear_input(self):
        """Clear the input text area"""
        self.input_text.delete("1.0", tk.END)
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        
    def new_conversation(self):
        """Start a new conversation by clearing both input and output"""
        if messagebox.askyesno("New Conversation", "Start a new conversation? This will clear current conversation."):
            self.clear_input()
            self.clear_output()
            
    def save_conversation(self):
        """Save the current conversation"""
        self.output_text.config(state="normal")
        content = self.output_text.get("1.0", tk.END)
        self.output_text.config(state="disabled")
        self.save_log(content)
        
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Medical AI Assistant",
            "Medical AI Assistant v1.0\n\n"
            "A modern interface for AI-powered medical assistance.\n\n"
            "© 2025 Your Organization"
        )
        
    def show_help(self):
        """Show help dialog"""
        messagebox.showinfo(
            "Help",
            "How to use the Medical AI Assistant:\n\n"
            "1. Type your medical query in the input box\n"
            "2. Click 'Send' or press Enter to get a response\n"
            "3. View the AI's response in the output area\n"
            "4. Use 'View Log' to see the full conversation history\n\n"
            "For more assistance, please contact support."
        )
        
    def run(self):
        """Run the application"""
        # Bind Enter key to send message
        self.input_text.bind("<Return>", lambda event: self.send_message())
        
        # Start the main loop
        self.root.mainloop()
        
    def get_widgets(self):
        """Return the main widgets for external access"""
        return self.root, self.input_text, self.output_text


def create_gui(send_message_callback):
    """
    Creates the main GUI window.
    send_message_callback: A function to be called when the "Send" button is clicked.
    """
    ui = ModernUI(send_message_callback)
    return ui.get_widgets()


# Add this function back for backward compatibility
def add_clear_button(root, text_widget):
    """
    Adds a clear button to clear the content of a text widget.
    This function is maintained for backward compatibility.
    
    root: The parent widget for the button
    text_widget: The text widget to clear
    """
    clear_button = ttk.Button(
        root, 
        text="Clear", 
        command=lambda: text_widget.delete("1.0", tk.END),
        style='TButton' if hasattr(ttk, 'Style') else None
    )
    clear_button.pack()
    return clear_button


def show_log(log_content):
    """
    Creates a new window to display the log.
    This function is maintained for backward compatibility.
    """
    log_window = tk.Toplevel()
    log_window.title("AI Log")
    log_window.geometry("700x500")
    
    log_text = scrolledtext.ScrolledText(
        log_window, 
        height=20, 
        width=80,
        font=('Arial', 10) if 'Arial' in tk.font.families() else None
    )
    log_text.insert(tk.END, log_content)
    log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Close button
    close_btn = ttk.Button(
        log_window, 
        text="Close", 
        command=log_window.destroy,
        style='TButton' if hasattr(ttk, 'Style') else None
    )
    close_btn.pack(pady=10)


# For testing purposes
if __name__ == "__main__":
    def dummy_callback(input_text, output_text):
        """Test callback function"""
        query = input_text.get("1.0", tk.END).strip()
        output_text.config(state="normal")
        output_text.insert(tk.END, f"Query: {query}\n")
        output_text.insert(tk.END, "Response: This is a test response from the Medical AI Assistant.\n\n")
        output_text.see(tk.END)  # Scroll to the end
        
    ui = ModernUI(dummy_callback)
    ui.run()