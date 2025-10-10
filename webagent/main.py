import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
from webagent.agent import WebAgent

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Navigator AI Agent")
        self.root.geometry("600x400")
        self.agent = WebAgent()
        self.setup_ui()

    def setup_ui(self):
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(input_frame, text="Enter Instruction:").pack(side=tk.LEFT, padx=5)
        self.input_box = tk.Entry(input_frame, width=50)
        self.input_box.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(buttons_frame, text="Execute", command=self.execute).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Voice Input", command=self.voice_input).pack(side=tk.LEFT, padx=5)

        # Output frame
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.output_box = scrolledtext.ScrolledText(output_frame, width=60, height=20)
        self.output_box.pack(fill=tk.BOTH, expand=True)

    def execute(self):
        instruction = self.input_box.get().strip()
        if not instruction:
            messagebox.showwarning("Input", "Please enter an instruction.")
            return

        self.output_box.insert(tk.END, f"\n> Processing: {instruction}\n", 'user')
        self.output_box.see(tk.END)

        try:
            plan = self.agent.parse_and_plan(instruction)
            self.output_box.insert(tk.END, f"Plan: {plan}\n", 'plan')

            results = self.agent.execute_plan(plan)
            self.output_box.insert(tk.END, "Results:\n", 'results')
            for result in results['results']:
                if isinstance(result, list):
                    for item in result:
                        self.output_box.insert(tk.END, f"• {item}\n", 'results')
                else:
                    self.output_box.insert(tk.END, f"• {result}\n", 'results')

            self.output_box.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

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
            except Exception as e:
                messagebox.showwarning("Voice", f"Error: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
