import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import json
import csv
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webagent.agent import WebNavigatorAgent
from webagent.browser_controller import BrowserController

def export_results(results, format_type='json'):
    """Export results to JSON or CSV."""
    if format_type == 'json':
        with open('results.json', 'w') as f:
            json.dump(results, f, indent=2)
    elif format_type == 'csv':
        with open('results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Link'])
            for result in results:
                writer.writerow([result.get('title', ''), result.get('link', '')])

def process_input(input_text):
    """Process user input and execute the task."""
    if not input_text.strip():
        messagebox.showerror("Error", "Please enter a command")
        return
    agent = WebNavigatorAgent()
    plan = agent.parse_instruction(input_text)
    browser = BrowserController(headless=False)  # Set to False for debugging
    try:
        results = agent.execute_plan(plan, browser)
        agent.save_task(input_text, json.dumps(plan))  # Save task to memory.json
        export_results(results, 'json')
        export_results(results, 'csv')
        output_text.set(json.dumps(results, indent=2))
    except Exception as e:
        messagebox.showerror("Error", f"Execution failed: {str(e)}")
    finally:
        browser.close()

def voice_input():
    """Capture voice input and convert to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", "Speak now...")
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)  # Requires internet
            entry.delete(0, tk.END)
            entry.insert(0, text)
        except sr.UnknownValueError:
            messagebox.showerror("Voice Error", "Could not understand audio")
        except sr.RequestError as e:
            messagebox.showerror("Voice Error", f"Speech recognition failed: {e}")

# GUI Setup
root = tk.Tk()
root.title("WebNavigatorAI")
root.geometry("600x400")

tk.Label(root, text="Enter Command:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, width=50, font=("Arial", 10))
entry.pack(pady=5)

tk.Button(root, text="Execute", command=lambda: process_input(entry.get()), font=("Arial", 10)).pack(pady=5)
tk.Button(root, text="Voice Input", command=voice_input, font=("Arial", 10)).pack(pady=5)

tk.Label(root, text="Output:", font=("Arial", 12)).pack(pady=10)
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, font=("Arial", 10), wraplength=550, justify="left")
output_label.pack(pady=5)

root.mainloop()
