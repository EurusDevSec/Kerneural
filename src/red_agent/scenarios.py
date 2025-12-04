ATTACK_SCENARIOS = {
    "T1059.004": {
        "name": "Command and Scripting Interpreter: Unix Shell",
        "description": "Executes simple shell commands to test visibility.",
        "commands": [
            "echo 'Simulating T1059.004 Attack'",
            "id",
            "whoami",
            "ls -la /tmp"
        ]
    },
    "T1555": {
        "name": "Credentials from Password Stores",
        "description": "Attempts to read sensitive files like /etc/shadow.",
        "commands": [
            "echo 'Simulating T1555 Attack'",
            "cat /etc/shadow",
            "cat /etc/passwd"
        ]
    },
    "T1070.004": {
        "name": "Indicator Removal on Host: File Deletion",
        "description": "Deletes file to hide tracks.",
        "commands": [
            "touch /tmp/evidence.txt",
            "rm -f /tmp/evidence.txt"
        ]
    }
}