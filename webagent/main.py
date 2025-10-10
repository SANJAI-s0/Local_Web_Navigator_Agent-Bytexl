import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr  # Optional voice input
from .agent import WebAgent

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web Navigator AI Agent")
        self.root.geometry("600x400")
        self.agent = WebAgent()
        # GUI Elements
        tk.Label(self.root, text="Enter Instruction:").pack(pady=5)
        self.input_box = tk.Entry(self.root, width=50)
        self.input_box.pack(pady=5)
        tk.Button(self.root, text="Execute", command=self.execute).pack(pady=5)
        tk.Button(self.root, text="Voice Input", command=self.voice_input).pack(pady=5)
        self.output_box = scrolledtext.ScrolledText(self.root, width=60, height=20)
        self.output_box.pack(pady=5)

    def execute(self):
        instruction = self.input_box.get().strip()
        if not instruction:
            messagebox.showwarning("Input", "Please enter an instruction.")
            return
        try:
            self.output_box.insert(tk.END, f"Processing: {instruction}\n")
            plan = self.agent.parse_and_plan(instruction)
            self.output_box.insert(tk.END, f"Plan: {plan}\n")
            results = self.agent.execute_plan(plan)
            self.output_box.insert(tk.END, f"Results: {results}\n\n")
            self.output_box.see(tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def voice_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.output_box.insert(tk.END, "Listening...\n")
            try:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio)  # Free API, internet required for this part
                self.input_box.delete(0, tk.END)
                self.input_box.insert(0, text)
                self.output_box.insert(tk.END, f"Voice Input: {text}\n")
            except sr.UnknownValueError:
                messagebox.showwarning("Voice", "Could not understand audio")
            except sr.RequestError:
                messagebox.showwarning("Voice", "Voice recognition service unavailable")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
