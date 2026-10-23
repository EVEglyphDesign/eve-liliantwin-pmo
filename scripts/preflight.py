#!/usr/bin/env python3
"""Repo entry and release checks; not a platform-wide enforcement mechanism."""
import argparse, hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "Emerson_Rush_DI_PMO_reference.pptx": "84158ce39296d99381214552e94969f8a930f7c80bc25a79b771393b4767310d",
    "DI_PMO_Decision_Roles_Map_approved.pptx": "cfb8d2542d47399a718cf517795084b46850e468ac5b65931ae1d6efbf84d664"}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(boot, project, release=False):
    errors, hashes = [], {}
    paths = [boot/x for x in ("README.md","registry/NARROWING.md","registry/ACTIVE.md","registry/OBSERVATIONS.md")]
    paths += [ROOT/"AGENTS.md"] + [project/x for x in ("START-HERE.md","AGENTS.md","di-pmo-pitch/CASE-RECORD.md","di-pmo-pitch/RELEASE-STATUS.json")]
    for path in paths:
        if not path.is_file() or not path.stat().st_size: errors.append(f"Required source unavailable: {path}")
        else: hashes[str(path)] = sha(path)
    for name, expected in TEMPLATES.items():
        path = ROOT/"templates"/name
        if not path.is_file() or sha(path) != expected: errors.append(f"Missing or altered template: {name}")
    status = project/"di-pmo-pitch/RELEASE-STATUS.json"
    if release and status.is_file():
        try:
            state=json.loads(status.read_text())
            if state.get("status") != "approved": errors.append("Release BLOCKED: not operator-approved.")
            artifact=project/state.get("artifact","")
            if not artifact.is_file(): errors.append("Release BLOCKED: artifact missing.")
            elif sha(artifact) != state.get("sha256"): errors.append("Release BLOCKED: bytes differ from reviewed artifact.")
            if not state.get("operator_approval_reference"): errors.append("Release BLOCKED: no operator approval reference.")
            review=state.get("review",{})
            checks=("all_slides_rendered","diagram_checked_at_slide_scale","source_coverage_checked","audience_and_custody_checked")
            if review.get("artifact_sha256") != state.get("sha256") or not all(review.get(k) for k in checks):
                errors.append("Release BLOCKED: exact-artifact review incomplete.")
        except (ValueError,TypeError) as exc: errors.append(f"Invalid release state: {exc}")
    return {"ok":not errors,"errors":errors,"input_sha256":hashes,
            "limitation":"Checks inputs and recorded state; does not prove comprehension, visual quality or platform enforcement."}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--boot-repo",type=Path,required=True)
    ap.add_argument("--project-files",type=Path,required=True)
    ap.add_argument("--release",action="store_true")
    a=ap.parse_args();r=validate(a.boot_repo,a.project_files,a.release)
    print(json.dumps(r,indent=2));sys.exit(0 if r["ok"] else 1)
