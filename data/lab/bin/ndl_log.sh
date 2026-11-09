#!/usr/bin/env bash
# data/lab/bin/ndl_log.sh — 两级 append-only 日志写入器（TEST PROFILE）
# 用法: ndl_log.sh <node_id> <task_id> <status> <summary>
# 顺序: 节点日志 append -> MAIN.md 追加摘要 -> 覆写 STATUS BLOCK
# 时间戳一律取系统 date，禁止硬编码。
set -euo pipefail
R=/workspace
NODE_ID="$1"; TASK_ID="$2"; STATUS="$3"; SUMMARY="$4"
TS="$(date '+%Y-%m-%d %H:%M:%S %z')"
NODE_LOG="$R/logs/$NODE_ID.md"
MAIN="$R/logs/MAIN.md"

# 日志条目编号：按 MAIN.md 已有条目数递增，禁止编造
if [ -f "$MAIN" ]; then
  N=$(grep -c '^- \[L-' "$MAIN" 2>/dev/null || true)
else
  N=0
fi
N=${N:-0}
SEQ=$(printf 'L-%03d' $((N + 1)))

# 1) 节点日志 append-only
{
  echo "- [$SEQ] $TS | task=$TASK_ID | status=$STATUS | $SUMMARY"
} >> "$NODE_LOG"

# 2) 总日志追加摘要
{
  echo "- [$SEQ] $TS | node=$NODE_ID | task=$TASK_ID | status=$STATUS | $SUMMARY"
} >> "$MAIN"

# 3) 覆写 STATUS BLOCK（唯一允许覆写的区域）
python3 - "$MAIN" "$SEQ" "$TS" "$NODE_ID" "$TASK_ID" "$STATUS" "$SUMMARY" <<'PY'
import sys, re, pathlib
main, seq, ts, node, task, status, summary = sys.argv[1:8]
p = pathlib.Path(main)
text = p.read_text(encoding="utf-8")
# 统计任务完成数（以日志条目为准，不推测）
done = len(re.findall(r'^- \[L-\d+\].*status=passed', text, re.M))
block = (
    "<!-- STATUS BLOCK START -->\n"
    f"- 更新时间: {ts}\n"
    f"- 当前条目: {seq}\n"
    f"- NODE-ID: {node}\n"
    f"- 最近任务: {task} ({status})\n"
    f"- 摘要: {summary}\n"
    f"- 已通过任务数: {done}\n"
    "<!-- STATUS BLOCK END -->"
)
if "<!-- STATUS BLOCK START -->" in text:
    text = re.sub(r"<!-- STATUS BLOCK START -->.*?<!-- STATUS BLOCK END -->",
                  block, text, flags=re.S)
else:
    text = text.rstrip() + "\n\n" + block + "\n"
p.write_text(text, encoding="utf-8")
PY

echo "$SEQ"
