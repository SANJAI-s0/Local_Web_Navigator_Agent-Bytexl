# quick_test_model.py
"""
Quick test to verify a local GPT4All model can be loaded and used.

Usage:
  python quick_test_model.py
  python quick_test_model.py --model-path models/gpt4all-model.bin
"""

import argparse
import sys
import traceback

DEFAULT_MODEL = "models/gpt4all-model.bin"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", "-m", type=str, default=DEFAULT_MODEL,
                        help="Path to local GPT4All model (ggml/gguf).")
    args = parser.parse_args()

    model_path = args.model_path
    print(f"[info] Testing GPT4All model at: {model_path}")

    try:
        # Import inside try so we can give a clear error if not installed
        from gpt4all import GPT4All  # type: ignore
    except Exception as e:
        print("[error] Could not import GPT4All Python binding.")
        print("Please install it in your virtual env with:")
        print("  pip install pygpt4all")
        print("Or install the package you use for local models (e.g., llama-cpp-python).")
        print()
        print("Import error details:")
        traceback.print_exc()
        sys.exit(2)

    try:
        model = GPT4All(model=model_path)
        print("[ok] GPT4All object created.")
    except Exception as e:
        print("[error] Failed to initialize GPT4All with the provided model path.")
        print("Possible causes: model file missing, corrupted, or incompatible binding.")
        print("Check that the file exists and is a valid ggml/gguf model.")
        print()
        traceback.print_exc()
        sys.exit(3)

    try:
        prompt = "Say hello in one short sentence."
        print(f"[info] Generating from model with prompt: {prompt!r}")
        # many GPT4All bindings expose a `generate` method; if yours differs adjust accordingly
        out = model.generate(prompt, max_tokens=40)
        print("[ok] Model generation successful. Output:")
        # `out` may be a string or list-like depending on binding/version
        if isinstance(out, (list, tuple)):
            print("".join(map(str, out)))
        else:
            print(out)
    except Exception as e:
        print("[error] Generation failed. See traceback:")
        traceback.print_exc()
        sys.exit(4)

if __name__ == "__main__":
    main()
