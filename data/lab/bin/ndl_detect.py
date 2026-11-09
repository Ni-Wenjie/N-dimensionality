#!/usr/bin/env python3
"""data/lab/bin/ndl_detect.py — F3 可复现检测器（TEST PROFILE）
对节点工作区做客观检测，输出 JSON 到 stdout，不写入任何业务文件。
用法: ndl_detect.py <node_workspace_path>
"""
import hashlib
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
files = sorted(
    p for p in root.rglob("*")
    if p.is_file() and not ({".git", "node_modules", "coverage"} & set(p.parts))
)
rel = [str(p.relative_to(root)) for p in files]

community = [
    "README.md", "LICENSE", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "SECURITY.md", "SUPPORT.md", "CHANGELOG.md", ".gitignore",
    ".github/ISSUE_TEMPLATE", ".github/PULL_REQUEST_TEMPLATE.md",
]
community_status = {
    f: ("present" if (root / f).exists() else "missing") for f in community
}

ci = sorted(
    p.name for p in (root / ".github/workflows").glob("*")
) if (root / ".github/workflows").is_dir() else []

src = (root / "src/index.ts").read_text(encoding="utf-8") if (root / "src/index.ts").exists() else ""
limit = re.search(r"str\.length\s*>\s*(\d+)", src)
msg = re.search(r"length between 1 and (\d+)", src)
tests = {}
case_count = 0
for p in sorted((root / "src").glob("*.test.ts")):
    t = p.read_text(encoding="utf-8")
    n = len(re.findall(r"\b(?:it|test)\s*\(", t))
    tests[p.name] = {"lines": len(t.splitlines()), "cases": n}
    case_count += n

pkg = json.loads((root / "package.json").read_text(encoding="utf-8"))
license_head = " ".join((root / "LICENSE").read_text(encoding="utf-8").split()[:6]) if (root / "LICENSE").exists() else ""

out = {
    "file_count": len(files),
    "files": rel,
    "community": community_status,
    "community_missing": [k for k, v in community_status.items() if v == "missing"],
    "ci_workflows": ci,
    "source": {
        "index_ts_lines": len(src.splitlines()),
        "parse_length_guard": int(limit.group(1)) if limit else None,
        "parse_error_message_upper": int(msg.group(1)) if msg else None,
        "inconsistent": bool(limit and msg and limit.group(1) != msg.group(1)),
    },
    "tests": tests,
    "total_test_cases": case_count,
    "package": {"name": pkg.get("name"), "version": pkg.get("version"),
                "license": pkg.get("license"), "scripts": sorted(pkg.get("scripts", {}))},
    "license_head": license_head,
}
print(json.dumps(out, ensure_ascii=False, indent=2))
