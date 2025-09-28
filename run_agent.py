# run_agent.py
import argparse
import json
import os
import sys
from agent.orchestrator import Orchestrator

def pretty_print(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Run Local Web Agent (CLI)")
    parser.add_argument("--instruction", "-i", type=str, help="Instruction to execute (put in quotes). If omitted you'll be prompted.")
    parser.add_argument("--model-path", "-m", type=str, default="models/gpt4all-model.bin", help="Path to local GPT4All model (ggml).")
    parser.add_argument("--headless", action="store_true", help="Run Playwright headless (default). Use --no-headless instead to show browser.")
    parser.add_argument("--no-headless", dest="headless", action="store_false", help="Run Playwright with GUI (headed).")
    parser.set_defaults(headless=True)
    args = parser.parse_args()

    instr = args.instruction
    if not instr:
        try:
            instr = input("Enter instruction (e.g. 'search for laptops under 50k and list top 5'): ").strip()
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit(0)

    if not instr:
        print("No instruction given; exiting.")
        sys.exit(1)

    model_path = args.model_path
    model_exists = os.path.exists(model_path)
    if model_exists:
        print(f"Using model at: {model_path}")
    else:
        print(f"Model not found at {model_path}. The planner will use the heuristic fallback (no LLM).")
        print("To use an LLM, download a GPT4All ggml model and place it at the path, or pass --model-path.")
        model_path = None  # let Orchestrator/Planner handle fallback

    print("Starting orchestrator...")
    orch = Orchestrator(headless=args.headless, model_path=model_path)
    try:
        result = orch.run(instr)
    except Exception as e:
        print("Execution error:", e)
        sys.exit(2)

    pretty_print(result)
    # Also save the last result JSON to disk for inspection
    out_file = "last_run_result.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Result saved to {out_file}")

if __name__ == "__main__":
    main()
