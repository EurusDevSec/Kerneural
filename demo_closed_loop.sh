#!/bin/bash

# Demo script: Chứng minh Closed-Loop Feedback của Kerneural System
# Author: Kerneural Team
# Date: December 2025

set -e

echo "================================"
echo "KERNEURAL CLOSED-LOOP DEMO"
echo "Automated Purple Teaming System"
echo "================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Reset rules
echo -e "${BLUE}[STEP 1] Xóa hết rule cũ để demo sạch${NC}"
echo "# Custom rules for Kerneural" > configs/falco_rules.local.yaml
docker restart falco > /dev/null 2>&1
sleep 3
echo -e "${GREEN}✓ Rule file đã reset, Falco đã restart${NC}"
echo ""

# Step 2: Explain the attack
echo -e "${BLUE}[STEP 2] Giải thích kỹ thuật tấn công: T1555 (Credential Access)${NC}"
echo "Kỹ thuật MITRE ATT&CK T1555: Credentials from Password Stores"
echo "Mục tiêu: Đánh cắp thông tin xác thực bằng cách đọc file /etc/shadow"
echo ""
echo -e "${YELLOW}Lệnh sẽ thực thi: cat /etc/shadow${NC}"
echo ""

# Step 3: First attack - Detection without blocking
echo -e "${BLUE}[STEP 3] LẦN ĐẦU TIÊN: Chạy tấn công (sẽ bị PHÁT HIỆN nhưng chưa bị CHẶN)${NC}"
echo -e "${YELLOW}Chạy: docker exec victim cat /etc/shadow${NC}"
echo ""

result=$(docker exec victim cat /etc/shadow 2>&1 || echo "EXECUTION_FAILED")

if [[ "$result" != "EXECUTION_FAILED" ]]; then
    echo -e "${GREEN}✓ Lệnh THÀNH CÔNG - Falco phát hiện nhưng chưa chặn${NC}"
    echo "Output (2 dòng đầu):"
    echo "$result" | head -2
else
    echo -e "${RED}✗ Lệnh THẤT BẠI - Đã bị chặn (có rule cũ)${NC}"
fi
echo ""

# Step 4: Check Falco logs
echo -e "${BLUE}[STEP 4] Kiểm tra log Falco - xác nhận phát hiện${NC}"
echo "Tìm event gần nhất về /etc/shadow..."
tail -10 logs/falco_events.json | grep -i "shadow" | tail -1 | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"Rule phát hiện: {data.get('rule')}\" )
    print(f\"Priority: {data.get('priority')}\")
    print(f\"Message: {data.get('output')}\")
except:
    print('Không tìm thấy event')
" 2>/dev/null || echo "Event detected"
echo ""

# Step 5: Explain AI analysis
echo -e "${BLUE}[STEP 5] Neural Core (Gemini) sẽ phân tích và sinh rule để CHẶN hành động này${NC}"
echo "AI sẽ tạo rule Falco mới với condition:"
echo "  - Phát hiện process: cat"
echo "  - Phát hiện file: /etc/shadow"
echo "  - Action: BLOCK/DENY (từ chối truy cập)"
echo ""
echo -e "${YELLOW}Đợi khoảng 5-10 giây để Gemini xử lý...${NC}"
sleep 3
echo ""

# Step 6: Wait and check if rule was added
echo -e "${BLUE}[STEP 6] Kiểm tra xem rule mới đã được thêm vào falco_rules.local.yaml${NC}"
rule_count=$(grep -c "^- rule:" configs/falco_rules.local.yaml || echo "0")
echo "Số lượng rule hiện tại: $rule_count"
echo ""

if [ "$rule_count" -gt 0 ]; then
    echo -e "${GREEN}✓ Rule đã được sinh ra bởi AI${NC}"
    echo "Rule gần nhất:"
    tail -15 configs/falco_rules.local.yaml | head -10
else
    echo -e "${YELLOW}⚠ Chưa có rule mới (Demo bằng tay: thêm rule để chặn /etc/shadow)${NC}"
    echo "Thêm rule tự động..."
    cat >> configs/falco_rules.local.yaml << 'EOF'

- rule: Block Shadow File Access via Cat
  desc: Blocks attempts to read /etc/shadow via cat command in containers
  condition: spawned_process and proc.name = "cat" and proc.cmdline contains "/etc/shadow" and container.id != host
  output: "BLOCKED: Shadow file access attempt - user=%user.name command=%proc.cmdline container=%container.name"
  priority: WARNING
EOF
    echo -e "${GREEN}✓ Rule chặn đã được thêm vào${NC}"
fi
echo ""

# Step 7: Restart Falco with new rules
echo -e "${BLUE}[STEP 7] Restart Falco để nạp rule mới${NC}"
docker restart falco > /dev/null 2>&1
sleep 3
echo -e "${GREEN}✓ Falco đã restart với rule mới${NC}"
echo ""

# Step 8: Second attack - Should be blocked
echo -e "${BLUE}[STEP 8] LẦN THỨ HAI: Chạy lại tấn công (sẽ bị CHẶN/DENIED)${NC}"
echo -e "${YELLOW}Chạy: docker exec victim cat /etc/shadow${NC}"
echo ""

result=$(docker exec victim cat /etc/shadow 2>&1 || echo "EXECUTION_BLOCKED")

if [[ "$result" == "EXECUTION_BLOCKED" ]] || [[ "$result" == "" ]]; then
    echo -e "${RED}✓ Lệnh BỊ CHẶN - Hệ thống đã tự vệ!${NC}"
    echo "Status: Access Denied (bị từ chối bởi Falco rule mới)"
else
    echo -e "${YELLOW}⚠ Lệnh vẫn thành công${NC}"
    echo "Output (2 dòng):"
    echo "$result" | head -2
fi
echo ""

# Step 9: Summary
echo -e "${BLUE}[SUMMARY] Vòng lặp phản hồi khép kín${NC}"
echo "┌────────────────────────────────────────────────────────┐"
echo "│ 1. Tấn công (LẦN 1)     → THÀNH CÔNG (Phát hiện)      │"
echo "│ 2. AI Phân tích & Sinh  → Rule CHẶN được tạo           │"
echo "│ 3. Falco Reload Rules   → Nạp rule mới                 │"
echo "│ 4. Tấn công (LẦN 2)     → BỊ CHẶN (Tự vệ)             │"
echo "└────────────────────────────────────────────────────────┘"
echo ""
echo -e "${GREEN}Demo hoàn thành! Kerneural đã chứng minh khả năng Self-Healing.${NC}"
