#!/usr/bin/env python3
"""data/lab/bin/ndl_verify.py — F5 可自动判定验收器（TEST PROFILE）
用法: ndl_verify.py <community|parse-msg|parse-runtime|ci-gate|all> [node_dir]
node_dir 缺省时从 data/lab/REGISTRY.yaml 读取第一个节点的 workspace_path。
退出码 0 = 断言全部通过；非 0 = 有断言失败。
"""
import pathlib
import subprocess
import sys
import yaml

W = pathlib.Path("/workspace")


def node_dir(argv):
    if len(argv) > 2:
        return pathlib.Path(argv[2]).resolve()
    reg = yaml.safe_load((W / "data/lab/REGISTRY.yaml").read_text())
    return (W / reg["nodes"][0]["workspace_path"]).resolve()


def checks(root):
    c = {
        "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md",
        "CHANGELOG.md", ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        "README.md", "LICENSE", ".gitignore",
    }
    results = []
    for f in sorted(c):
        p = root / f
        results.append((f"present+nonempty: {f}", p.is_file() and p.stat().st_size > 0))
    src = (root / "src/index.ts").read_text(encoding="utf-8")
    results.append(("parse guard/message consistent",
                    "str.length > 100" in src and "length between 1 and 100" in src))
    results.append(("regression test present",
                    (root / "src/parse-length.test.ts").is_file()))
    wf = root / ".github/workflows/ndl-community.yml"
    results.append(("ci gate workflow present", wf.is_file() and wf.stat().st_size > 0))
    try:
        yaml.safe_load(wf.read_text()) if wf.is_file() else None
        results.append(("ci gate YAML parseable", wf.is_file()))
    except Exception:
        results.append(("ci gate YAML parseable", False))
    for f in (".github/ISSUE_TEMPLATE/bug_report.yml",
              ".github/ISSUE_TEMPLATE/feature_request.yml"):
        p = root / f
        try:
            yaml.safe_load(p.read_text())
            ok = p.is_file()
        except Exception:
            ok = False
        results.append((f"YAML parseable: {f}", ok))
    return results


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    root = node_dir(sys.argv)
    failed = []
    if mode in ("community", "parse-msg", "ci-gate", "all"):
        for name, ok in checks(root):
            keep = (mode == "all"
                    or (mode == "community" and (name.startswith("present") or "YAML parseable" in name))
                    or (mode == "parse-msg" and "consistent" in name)
                    or (mode == "parse-runtime" and "regression test" in name)
                    or (mode == "ci-gate" and "ci gate" in name))
            if keep:
                print(("PASS " if ok else "FAIL ") + name)
                if not ok:
                    failed.append(name)
    if mode in ("parse-runtime", "all"):
        r = subprocess.run(["pnpm", "run", "test:nodejs"], cwd=root,
                           capture_output=True, text=True, timeout=300)
        import re
        # Jest 摘要写入 stderr，覆盖率表写入 stdout，必须合并后判定
        combined = r.stdout + "\n" + r.stderr
        tail = combined.strip().splitlines()[-6:]
        m = re.search(r"Tests:\s+(\d+) passed, (\d+) total", combined)
        ok = (r.returncode == 0 and m is not None
              and m.group(1) == m.group(2) and int(m.group(1)) >= 167)
        label = f"pnpm run test:nodejs ({m.group(1)} passed)" if m else "pnpm run test:nodejs (no summary)"
        print(("PASS " if ok else "FAIL ") + label)
        print("\n".join("      " + x for x in tail))
        if not ok:
            failed.append("pnpm run test:nodejs")
    print(f"\nRESULT mode={mode} failed={len(failed)}")
    if failed:
        print("FAILED_ASSERTIONS: " + ", ".join(failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
