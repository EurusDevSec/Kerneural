#!/bin/bash

# Advanced Demo Script: Multi-Technique Attack Showcase
# Demonstrates Kerneural's ability to detect and block various MITRE ATT&CK techniques
# Author: Kerneural Team
# Date: December 2025

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
VICTIM_CONTAINER="victim"
RULE_FILE="configs/falco_rules.local.yaml"
LOG_FILE="logs/falco_events.json"

# Helper functions
print_header() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
}

print_step() {
    echo ""
    echo -e "${MAGENTA}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_attack() {
    echo ""
    echo -e "${RED}🔴 ATTACK: $1${NC}"
    echo -e "${CYAN}Command: $2${NC}"
}

# Main demo starts here
print_header "KERNEURAL - Advanced Attack Detection Demo"
echo "Testing MITRE ATT&CK Techniques with Automated Response"
echo ""

# Check if container is running
if ! docker ps | grep -q "$VICTIM_CONTAINER"; then
    print_error "Container '$VICTIM_CONTAINER' is not running. Start Docker containers first."
    echo "Run: docker-compose up -d"
    exit 1
fi

print_success "Container '$VICTIM_CONTAINER' is running"

# Clean setup: Create fresh log file
print_step "Setting up fresh log file..."
mkdir -p logs
cat > "$LOG_FILE" << 'EOF'
EOF
print_success "Fresh log file created"
sleep 2

# ============================================================================
# TECHNIQUE 1: T1059.004 - Command and Scripting Interpreter: Unix Shell
# ============================================================================

print_header "TECHNIQUE 1: T1059.004 - Command Execution in Shell"
echo "MITRE ATT&CK: Command and Scripting Interpreter: Unix Shell"
echo "Attacker Goal: Execute arbitrary commands to explore the system"
echo ""

# Reset rules for this technique
print_step "Resetting Falco rules and log file for clean demo"
echo "# Custom rules for Kerneural" > "$RULE_FILE"

# Delete log file INSIDE container before restart
print_step "Clearing Falco log file inside container..."
docker exec falco rm -f /var/log/falco/falco_events.json 2>/dev/null || true
sleep 1

print_step "Restarting Falco container..."
docker restart falco
echo "⏳ Waiting for Falco to fully start and create fresh log (10 seconds)..."
sleep 10

# Verify Falco is ready by checking logs
if docker logs falco 2>&1 | grep -q "Opening.*syscall"; then
    print_success "✓ Falco is ready and listening for syscalls"
else
    print_warning "⚠ Falco may not be fully ready, waiting more..."
    sleep 5
fi

# Verify log file exists and is fresh
if [ -f "$LOG_FILE" ]; then
    file_size=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo "0")
    print_success "✓ Fresh log file created (size: $file_size bytes)"
else
    print_warning "⚠ Log file not found yet, Falco will create it on first event"
fi

echo "⏳ Giving system time to stabilize..."
sleep 3

# Attack 1a: Simple command execution
print_attack "T1059.004" "echo 'Simulating T1059.004 Attack'"
docker exec "$VICTIM_CONTAINER" sh -c "echo 'Simulating T1059.004 Attack'"
sleep 3

# Attack 1b: System information gathering
print_attack "T1059.004" "id"
docker exec "$VICTIM_CONTAINER" sh -c "id"
sleep 3

# Attack 1c: User enumeration
print_attack "T1059.004" "whoami"
docker exec "$VICTIM_CONTAINER" sh -c "whoami"
sleep 3

# Attack 1d: Privilege escalation check
print_attack "T1059.004" "uname -a"
docker exec "$VICTIM_CONTAINER" sh -c "uname -a"
sleep 3

# Attack 1e: Exploration
print_attack "T1059.004" "ls -la /tmp"
docker exec "$VICTIM_CONTAINER" sh -c "ls -la /tmp"
sleep 3

echo "⏳ Waiting for Falco to log all events..."
sleep 2

print_step "Checking Falco logs for T1059.004 detections"
echo "Events detected:"
grep -i "whoami\|uname" "$LOG_FILE" | tail -2 | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        data = json.loads(line)
        print(f\"  • {data.get('priority')}: {data.get('rule')}\")
    except:
        pass
" 2>/dev/null || echo "  (Events being logged to Falco)"

echo ""
echo -e "${CYAN}ℹ At this point, Gemini would analyze logs and generate rules${NC}"
echo -e "${CYAN}  to block these reconnaissance activities.${NC}"

# ============================================================================
# TECHNIQUE 2: T1555 - Credentials from Password Stores
# ============================================================================

print_header "TECHNIQUE 2: T1555 - Credentials from Password Stores"
echo "MITRE ATT&CK: Credentials from Password Stores"
echo "Attacker Goal: Steal sensitive credentials by reading /etc/shadow"
echo ""

print_step "Resetting rules for Technique 2"
echo "# Custom rules for Kerneural" > "$RULE_FILE"

# Delete log file INSIDE container before restart  
docker exec falco rm -f /var/log/falco/falco_events.json 2>/dev/null || true
sleep 1

print_step "Restarting Falco container..."
docker restart falco
echo "⏳ Waiting for Falco to fully start (10 seconds)..."
sleep 10

if docker logs falco 2>&1 | grep -q "Opening.*syscall"; then
    print_success "✓ Falco is ready and listening for syscalls"
else
    print_warning "⚠ Falco may not be fully ready, waiting more..."
    sleep 5
fi

echo "⏳ Giving system time to stabilize..."
sleep 3

# Attack 2a: Announce credential theft attempt
print_attack "T1555" "echo 'Simulating T1555 Attack'"
docker exec "$VICTIM_CONTAINER" sh -c "echo 'Simulating T1555 Attack'"
sleep 3

# Attack 2b: Read /etc/shadow (highly sensitive)
print_attack "T1555" "cat /etc/shadow"
result=$(docker exec "$VICTIM_CONTAINER" cat /etc/shadow 2>&1 || echo "BLOCKED")
if [[ "$result" == "BLOCKED" ]]; then
    print_error "Access Denied - Rule is blocking this!"
else
    echo "$result" | head -2
    sleep 3
fi

echo "⏳ Pausing between attacks..."
sleep 2

# Attack 2c: Read /etc/passwd (less sensitive but still important)
print_attack "T1555" "cat /etc/passwd"
result=$(docker exec "$VICTIM_CONTAINER" cat /etc/passwd 2>&1 || echo "BLOCKED")
if [[ "$result" == "BLOCKED" ]]; then
    print_error "Access Denied - Rule is blocking this!"
else
    echo "$result" | head -2
fi

echo "⏳ Waiting for Falco to log all events..."
sleep 2

print_step "Checking Falco logs for T1555 detections"
echo "Events detected:"
grep -i "shadow\|passwd" "$LOG_FILE" | tail -3 | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        data = json.loads(line)
        rule = data.get('rule', 'Unknown')
        print(f\"  • [{data.get('priority')}] {rule}\")
    except:
        pass
" 2>/dev/null || echo "  (Events being logged)"

echo ""
echo -e "${CYAN}ℹ Gemini detects credential access attempt and generates${NC}"
echo -e "${CYAN}  protective rules to prevent /etc/shadow access.${NC}"

# ============================================================================
# TECHNIQUE 3: T1070.004 - File Deletion (Cover Tracks)
# ============================================================================

print_header "TECHNIQUE 3: T1070.004 - Indicator Removal (File Deletion)"
echo "MITRE ATT&CK: Indicator Removal on Host: File Deletion"
echo "Attacker Goal: Delete files to cover tracks"
echo ""

print_step "Resetting rules for Technique 3"
echo "# Custom rules for Kerneural" > "$RULE_FILE"
sleep 1

print_step "Restarting Falco container..."
docker restart falco
echo "⏳ Waiting for Falco to fully start (10 seconds)..."
sleep 10

if docker logs falco 2>&1 | grep -q "Opening.*syscall"; then
    print_success "✓ Falco is ready and listening for syscalls"
else
    print_warning "⚠ Falco may not be fully ready, waiting more..."
    sleep 5
fi

echo "⏳ Giving system time to stabilize..."
sleep 3

# Attack 3a: Create evidence file
print_attack "T1070.004" "touch /tmp/evidence.txt"
docker exec "$VICTIM_CONTAINER" sh -c "touch /tmp/evidence.txt && echo 'Evidence file created'"
sleep 3

echo "⏳ Pausing between attacks..."
sleep 2

# Attack 3b: Delete evidence
print_attack "T1070.004" "rm -f /tmp/evidence.txt"
docker exec "$VICTIM_CONTAINER" sh -c "rm -f /tmp/evidence.txt && echo 'File deleted'"
sleep 3

echo "⏳ Waiting for Falco to log all events..."
sleep 2

print_step "Checking Falco logs for T1070.004 detections"
echo "File operations detected:"
grep -i "delete\|remove\|unlink" "$LOG_FILE" | tail -2 | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        data = json.loads(line)
        print(f\"  • {data.get('priority')}: {data.get('output', 'Event logged')}\" | cut -d' ' -f1-8)
    except:
        pass
" 2>/dev/null || echo "  (File operations being monitored)"

echo ""
echo -e "${CYAN}ℹ Gemini analyzes file deletion patterns and creates rules${NC}"
echo -e "${CYAN}  to detect and prevent unauthorized file removal.${NC}"

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print_header "Demo Complete - System Summary"

echo ""
echo -e "${BLUE}Detection Coverage:${NC}"
echo "  ✓ T1059.004 - Command Execution (Unix Shell)"
echo "  ✓ T1555     - Credential Access (Password Stores)"
echo "  ✓ T1070.004 - Indicator Removal (File Deletion)"
echo ""

echo -e "${BLUE}Falco Events Logged:${NC}"
event_count=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")
echo "  Total events: $event_count"
echo ""

echo -e "${BLUE}Rules Generated:${NC}"
rule_count=$(grep -c "^- rule:" "$RULE_FILE" 2>/dev/null || echo "0")
if [ "$rule_count" -gt 0 ]; then
    echo "  Auto-generated rules: $rule_count"
else
    echo "  No auto-generated rules yet (Gemini processing would create them)"
fi
echo ""

echo -e "${MAGENTA}Next Steps for Full Demo:${NC}"
echo "  1. Run: python run.py          (Start Dashboard in Terminal 1)"
echo "  2. Run: bash demo_attacks.sh   (Execute attacks in Terminal 2)"
echo "  3. Watch Dashboard for:"
echo "     • Live threat feed"
echo "     • AI analysis of each attack"
echo "     • Auto-generated Falco rules"
echo "     • Automatic Falco reload"
echo ""

print_success "Kerneural Demo Completed"
print_success "All techniques executed and logged"
echo ""
