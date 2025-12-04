# System Prompt định hình vai trò của AI
SYSTEM_PROMPT = """
You are a Cyber Security Expert specializing in Falco Rule Engineering.
Your task is to analyze security logs and generate Falco rules to block malicious activities.
"""


# Template cho yêu cầu sinh rule
RULE_GENERATION_PROMPT = """
Based on the following Falco log event, generate a YAML Falco rule to BLOCK this specific activity.

LOG EVENT:
{log_json}

REQUIREMENTS:
1. The rule must detect the specific process and file/network activity mentioned in the log.
2. The output must be ONLY the YAML code block, no markdown formatting or explanation.
3. Set priority to 'WARNING'.
4. Use the 'kill' action if possible (or just alert for now).
5. The rule name should be unique and descriptive (e.g., "Block [Process] accessing [File]").

EXAMPLE OUTPUT FORMAT:
- rule: Rule Name
  desc: Description
  condition: ...
  output: ...
  priority: WARNING
"""