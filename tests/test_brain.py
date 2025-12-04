from src.neural_core.gemini_client import NeuralBrain
import json


# Giả lập một log tấn công
mock_log = {
    "output": "Sensitive file opened for reading by non-trusted program",
    "output_fields": {
        "proc.name": "cat",
        "fd.name": "/etc/shadow",
        "user.name": "root"
    }
}

def main():
    brain = NeuralBrain()
    print("Sending log to Gemini...")
    rule = brain.analyze_log_and_generate_rule(json.dumps(mock_log))

    print("\n--- GENERATED RULE ---")
    print(rule)
    print("----------------------")

if __name__ == "__main__":
    main()