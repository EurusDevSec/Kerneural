import os
import subprocess

RULE_FILE_PATH="configs/falco_rules.local.yaml"

class RuleManager:
    def add_rule(self, rule_yaml):
        """
        Docstring for add_rule
        
        them rule moi vao file local config
        """
    # doc noi dung cu tranh trung lap
    if not os.path.exists(RULE_FILE_PATH):
        with open(RULE_FILE_PATH,'w') as f:
            f.write ("# Auto-generated rules\n")

    with open(RULE_FILE_PATH, 'a') as f:
        f.write("\n"+ rule_yaml + "\n")

    print(f"Rule added to {RULE_FILE_PATH}")


    def reload_falco(self):
        try:
            subprocess.run(["docker", "restart", "falco"], check=True)
            print("Falco restarted to apply new rules.")
        except Exception as e:
            print(f"Failed to reload Falco: {e}")
            