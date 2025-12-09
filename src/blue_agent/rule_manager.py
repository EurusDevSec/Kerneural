import os
import subprocess
import yaml

RULE_FILE_PATH="configs/falco_rules.local.yaml"

class RuleManager:
    def validate_rule(self, rule_yaml):
        """
        Validate YAML syntax and basic Falco rule structure before adding.
        """
        try:
            # 1. Check YAML syntax
            rules = yaml.safe_load(rule_yaml)
            
            # If it's a single dict, wrap in list
            if isinstance(rules, dict):
                rules = [rules]
                
            if not isinstance(rules, list):
                print("Validation Error: Rule must be a list or dict")
                return False

            for rule in rules:
                # 2. Check required fields
                required_fields = ['rule', 'desc', 'condition', 'output', 'priority']
                for field in required_fields:
                    if field not in rule:
                        print(f"Validation Error: Missing field '{field}' in rule '{rule.get('rule', 'unknown')}'")
                        return False
                
                # 3. Check for forbidden fields (like 'actions' which caused issues)
                if 'actions' in rule:
                    print(f"Validation Warning: Field 'actions' is not supported in standard Falco rules. Removing it.")
                    del rule['actions'] # Auto-fix: remove forbidden field

                # 4. Basic validation: Check for common syntax errors
                output = rule.get('output', '')
                condition = rule.get('condition', '')
                
                # Check that condition and output are not empty
                if not condition.strip():
                    print(f"Validation Error: Empty condition in rule '{rule.get('rule')}'")
                    return False
                if not output.strip():
                    print(f"Validation Error: Empty output in rule '{rule.get('rule')}'")
                    return False
                
                # Check priority is valid
                valid_priorities = ['EMERGENCY', 'ALERT', 'CRITICAL', 'ERROR', 'WARNING', 'NOTICE', 'INFO', 'DEBUG']
                if rule.get('priority') not in valid_priorities:
                    print(f"Validation Warning: Invalid priority '{rule.get('priority')}' in rule '{rule.get('rule')}'. Using WARNING.")
                    rule['priority'] = 'WARNING'

            return True
        except yaml.YAMLError as e:
            print(f"YAML Syntax Error: {e}")
            return False
        except Exception as e:
            print(f"Validation Unexpected Error: {e}")
            return False

    def add_rule(self, rule_yaml):
        """
        Docstring for add_rule
        
        them rule moi vao file local config
        """
        # Validate before writing
        if not self.validate_rule(rule_yaml):
            print("Rule validation failed. Skipping rule addition to prevent Falco crash.")
            return

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
            