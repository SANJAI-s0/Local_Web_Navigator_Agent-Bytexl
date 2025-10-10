# webagent/main.py
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import speech_recognition as sr
import json
from webagent.agent import WebAgent

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Navigator AI Agent")
        self.root.geometry("800x600")  # Larger window for better visibility
        self.root.configure(bg='#f0f0f0')  # Light background
        self.agent = WebAgent()
        self.setup_ui()

    def setup_ui(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')  # Modern theme
        style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=10, background='#4CAF50', foreground='white')
        style.configure('TLabel', font=('Helvetica', 14, 'bold'), background='#f0f0f0')
        style.configure('TEntry', font=('Helvetica', 12), padding=5)

        # Input frame
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(input_frame, text="Enter Instruction:", style='TLabel').pack(side=tk.LEFT, padx=5)
        self.input_box = ttk.Entry(input_frame, width=60, font=('Helvetica', 12))
        self.input_box.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Buttons frame
        buttons_frame = ttk.Frame(self.root, padding=10)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(buttons_frame, text="Execute", command=self.execute, style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Voice Input", command=self.voice_input, style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Clear Output", command=self.clear_output, style='TButton').pack(side=tk.LEFT, padx=10)

        # Output frame with separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=5)

        output_frame = ttk.Frame(self.root, padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.output_box = scrolledtext.ScrolledText(output_frame, width=70, height=25, font=('Helvetica', 11), wrap=tk.WORD, bg='#ffffff', fg='#333333', relief='flat', borderwidth=2, highlightthickness=1, highlightbackground='#cccccc')
        self.output_box.pack(fill=tk.BOTH, expand=True)

        # Enhanced tags for attractive output
        self.output_box.tag_config('user', foreground='#2196F3', font=('Helvetica', 12, 'bold'))  # Blue for user input
        self.output_box.tag_config('plan', foreground='#4CAF50', font=('Helvetica', 12, 'italic'))  # Green for plan
        self.output_box.tag_config('results', foreground='#FF5722', font=('Helvetica', 12, 'bold'))  # Orange for results headers
        self.output_box.tag_config('item', foreground='#333333', font=('Helvetica', 11))  # Normal for items

    def clear_output(self):
        self.output_box.delete(1.0, tk.END)

    def execute(self):
        instruction = self.input_box.get().strip()
        if not instruction:
            messagebox.showwarning("Input", "Please enter an instruction.")
            return

        self.output_box.insert(tk.END, f"\n> Processing: {instruction}\n", 'user')
        self.output_box.see(tk.END)

        try:
            plan = self.agent.parse_and_plan(instruction)
            self.output_box.insert(tk.END, f"Plan: {json.dumps(plan, indent=2)}\n\n", 'plan')

            results = self.agent.execute_plan(plan)
            self.output_box.insert(tk.END, "Results:\n", 'results')
            for result in results['results']:
                if isinstance(result, list):
                    for item in result:
                        if isinstance(item, dict):
                            self.output_box.insert(tk.END, f"• Title: {item.get('title', 'N/A')} | Price: {item.get('price', 'N/A')}\n", 'item')
                        else:
                            self.output_box.insert(tk.END, f"• {item}\n", 'item')
                else:
                    self.output_box.insert(tk.END, f"• {result}\n", 'item')
            self.output_box.insert(tk.END, "\n" + "-" * 50 + "\n", 'results')  # Separator for visual appeal

            self.output_box.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Execution failed: {str(e)}")

    def voice_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.output_box.insert(tk.END, "Listening...\n")
            try:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio)
                self.input_box.delete(0, tk.END)
                self.input_box.insert(0, text)
                self.output_box.insert(tk.END, f"Voice Input: {text}\n")
            except sr.UnknownValueError:
                messagebox.showwarning("Voice", "Could not understand audio")
            except sr.RequestError:
                messagebox.showwarning("Voice", "Speech recognition service unavailable")
            except Exception as e:
                messagebox.showerror("Voice", f"Voice input error: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
