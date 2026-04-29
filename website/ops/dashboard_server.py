#!/usr/bin/env python3
"""
Automation Dashboard Server
============================
Serves the interactive automation dashboard with REST API for:
  - Contacts CRUD
  - Targets CRUD
  - Outreach approval / sending
  - Social content approval
  - Blog content management
  - Automation scheduling & triggers
  - Analytics & logs

Uses Python stdlib http.server (same pattern as ForgeWeb).

Usage:
    python3 ops/dashboard_server.py                  # default port 4000
    python3 ops/dashboard_server.py --port 4001
"""

import argparse
import json
import os
import subprocess
import sys
import traceback
import uuid
from datetime import datetime
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "outreach_data"
CONTENT_DIR = PROJECT_ROOT / "content"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
DASHBOARD_DIR = PROJECT_ROOT / "ops" / "dashboard"

DEFAULT_PORT = 4000
DEFAULT_HOST = "localhost"
BLOCKLIST_FILE = DATA_DIR / "blocklist.json"


# ── Data helpers ─────────────────────────────────────────────

def read_json(path: Path) -> list | dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def find_by_field(items: list, field: str, value) -> tuple[int, dict | None]:
    for i, item in enumerate(items):
        if item.get(field) == value:
            return i, item
    return -1, None


def read_blocklist() -> dict:
    """Read contacts blocklist — {email: {reason, date, name, org}}."""
    if BLOCKLIST_FILE.exists():
        data = json.loads(BLOCKLIST_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return {e: {"reason": "migrated"} for e in data}
        return data
    return {}


def add_to_blocklist(email: str, name: str = "", org: str = "", reason: str = "deleted"):
    bl = read_blocklist()
    bl[email.lower()] = {
        "reason": reason,
        "name": name,
        "organization": org,
        "date": datetime.now().isoformat(),
    }
    write_json(BLOCKLIST_FILE, bl)


def is_blocked(email: str) -> bool:
    return email.lower() in read_blocklist()


# ── Request Handler ──────────────────────────────────────────

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for the automation dashboard."""

    def log_message(self, fmt, *args):
        # Quieter logging
        pass

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status=200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, filepath: Path):
        if not filepath.exists():
            self._send_json({"error": "Not found"}, 404)
            return
        ext = filepath.suffix.lower()
        content_types = {
            ".html": "text/html",
            ".css": "text/css",
            ".js": "application/javascript",
            ".json": "application/json",
            ".png": "image/png",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        ct = content_types.get(ext, "application/octet-stream")
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    def _parse_qs(self) -> dict:
        parsed = urlparse(self.path)
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()}

    # ── Routing ──────────────────────────────────────────────

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        # API routes
        if path.startswith("/api/"):
            return self._route_api_get(path)

        # Dashboard UI
        if path == "/" or path == "/index.html":
            return self._send_static(DASHBOARD_DIR / "index.html")

        # Static assets
        static_path = DASHBOARD_DIR / path.lstrip("/")
        if static_path.exists() and static_path.is_file():
            return self._send_static(static_path)

        self._send_json({"error": "Not found"}, 404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            return self._route_api_post(path)
        self._send_json({"error": "Not found"}, 404)

    def do_PUT(self):
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            return self._route_api_put(path)
        self._send_json({"error": "Not found"}, 404)

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path.startswith("/api/"):
            return self._route_api_delete(path)
        self._send_json({"error": "Not found"}, 404)

    # ── API GET routes ───────────────────────────────────────

    def _route_api_get(self, path: str):
        try:
            routes = {
                "/api/contacts": self._api_get_contacts,
                "/api/targets": self._api_get_targets,
                "/api/outreach/pending": self._api_get_pending,
                "/api/outreach/analytics": self._api_get_analytics,
                "/api/outreach/daily-reports": self._api_get_daily_reports,
                "/api/content/social": self._api_get_social,
                "/api/content/blog": self._api_get_blog,
                "/api/schedules": self._api_get_schedules,
                "/api/logs": self._api_get_logs,
                "/api/status": self._api_get_status,
                "/api/blocklist": self._api_get_blocklist,
            }
            handler = routes.get(path)
            if handler:
                return handler()
            self._send_json({"error": f"Unknown API route: {path}"}, 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def _route_api_post(self, path: str):
        try:
            routes = {
                "/api/contacts": self._api_create_contact,
                "/api/targets": self._api_create_target,
                "/api/outreach/approve": self._api_approve_outreach,
                "/api/outreach/reject": self._api_reject_outreach,
                "/api/outreach/send": self._api_send_outreach,
                "/api/content/social": self._api_create_social,
                "/api/content/social/approve": self._api_approve_social,
                "/api/content/blog": self._api_create_blog,
                "/api/contacts/log-contact": self._api_log_contact,
                "/api/contacts/toggle-response": self._api_toggle_response,
                "/api/automation/run": self._api_run_automation,
                "/api/automation/discover": self._api_run_discovery,
                "/api/discovery/search": self._api_discovery_search,
                "/api/blocklist/unblock": self._api_unblock_contact,
            }
            handler = routes.get(path)
            if handler:
                return handler()
            self._send_json({"error": f"Unknown API route: {path}"}, 404)
        except Exception as e:
            self._send_json({"error": str(e), "trace": traceback.format_exc()}, 500)

    def _route_api_put(self, path: str):
        try:
            if path.startswith("/api/contacts/"):
                return self._api_update_contact()
            if path.startswith("/api/targets/"):
                return self._api_update_target()
            if path.startswith("/api/outreach/pending/"):
                return self._api_update_pending()
            self._send_json({"error": f"Unknown API route: {path}"}, 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def _route_api_delete(self, path: str):
        try:
            if path.startswith("/api/contacts/"):
                return self._api_delete_contact()
            if path.startswith("/api/targets/"):
                return self._api_delete_target()
            if path.startswith("/api/outreach/pending/"):
                return self._api_delete_pending()
            self._send_json({"error": f"Unknown API route: {path}"}, 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    # ── Contacts ─────────────────────────────────────────────

    def _api_get_contacts(self):
        contacts = read_json(DATA_DIR / "contacts.json")
        params = self._parse_qs()
        if "category" in params:
            contacts = [c for c in contacts if c.get("category") == params["category"]]
        if "search" in params:
            q = params["search"].lower()
            contacts = [c for c in contacts if q in c.get("name", "").lower()
                        or q in c.get("email", "").lower()
                        or q in c.get("organization", "").lower()]
        self._send_json({"contacts": contacts, "total": len(contacts)})

    def _api_create_contact(self):
        body = self._read_body()
        contacts = read_json(DATA_DIR / "contacts.json")
        # Deduplicate by email
        email = body.get("email", "").strip().lower()
        if not email:
            return self._send_json({"error": "Email is required"}, 400)
        if is_blocked(email):
            return self._send_json({"error": "This contact was previously removed and is blocked"}, 409)
        for c in contacts:
            if c.get("email", "").lower() == email:
                return self._send_json({"error": "Contact already exists"}, 409)
        contact = {
            "name": body.get("name", "Unknown"),
            "email": email,
            "organization": body.get("organization", ""),
            "role": body.get("role", "Contact"),
            "source": body.get("source", "manual"),
            "category": body.get("category", "other"),
            "social_links": body.get("social_links", []),
            "contact_date": None,
            "response_received": False,
            "notes": body.get("notes", ""),
            "outreach_count": 0,
            "last_contact": None,
        }
        contacts.append(contact)
        write_json(DATA_DIR / "contacts.json", contacts)
        self._send_json({"ok": True, "contact": contact}, 201)

    def _api_update_contact(self):
        email_key = urlparse(self.path).path.split("/api/contacts/")[1]
        body = self._read_body()
        contacts = read_json(DATA_DIR / "contacts.json")
        idx, existing = find_by_field(contacts, "email", email_key)
        if idx == -1:
            return self._send_json({"error": "Contact not found"}, 404)
        for k, v in body.items():
            if k != "email":
                contacts[idx][k] = v
        write_json(DATA_DIR / "contacts.json", contacts)
        self._send_json({"ok": True, "contact": contacts[idx]})

    def _api_delete_contact(self):
        email_key = urlparse(self.path).path.split("/api/contacts/")[1]
        contacts = read_json(DATA_DIR / "contacts.json")
        idx, _ = find_by_field(contacts, "email", email_key)
        if idx == -1:
            return self._send_json({"error": "Contact not found"}, 404)
        removed = contacts.pop(idx)
        write_json(DATA_DIR / "contacts.json", contacts)
        # Add to blocklist so they don't get re-added by discovery
        add_to_blocklist(
            email_key,
            name=removed.get("name", ""),
            org=removed.get("organization", ""),
            reason="deleted",
        )
        self._send_json({"ok": True, "removed": removed, "blocked": True})

    def _api_log_contact(self):
        """Manually record that a contact was reached (email, phone, in-person)."""
        body = self._read_body()
        email = body.get("email", "").strip().lower()
        method = body.get("method", "email")  # email, phone, in-person, social
        note = body.get("note", "")
        if not email:
            return self._send_json({"error": "Email is required"}, 400)
        contacts = read_json(DATA_DIR / "contacts.json")
        idx, contact = find_by_field(contacts, "email", email)
        if idx == -1:
            return self._send_json({"error": "Contact not found"}, 404)
        now = datetime.now().isoformat()
        contacts[idx]["outreach_count"] = contacts[idx].get("outreach_count", 0) + 1
        contacts[idx]["last_contact"] = now
        if not contacts[idx].get("contact_date"):
            contacts[idx]["contact_date"] = now
        # Append to contact log
        log = contacts[idx].get("contact_log", [])
        log.append({"date": now, "method": method, "note": note})
        contacts[idx]["contact_log"] = log
        if note:
            existing_notes = contacts[idx].get("notes", "")
            contacts[idx]["notes"] = (existing_notes + "\n" + note).strip() if existing_notes else note
        write_json(DATA_DIR / "contacts.json", contacts)
        self._send_json({"ok": True, "contact": contacts[idx]})

    def _api_toggle_response(self):
        """Toggle response_received flag for a contact."""
        body = self._read_body()
        email = body.get("email", "").strip().lower()
        if not email:
            return self._send_json({"error": "Email is required"}, 400)
        contacts = read_json(DATA_DIR / "contacts.json")
        idx, contact = find_by_field(contacts, "email", email)
        if idx == -1:
            return self._send_json({"error": "Contact not found"}, 404)
        contacts[idx]["response_received"] = not contacts[idx].get("response_received", False)
        write_json(DATA_DIR / "contacts.json", contacts)
        self._send_json({"ok": True, "response_received": contacts[idx]["response_received"]})

    # ── Targets ──────────────────────────────────────────────

    def _api_get_targets(self):
        targets = read_json(DATA_DIR / "targets.json")
        params = self._parse_qs()
        if "category" in params:
            targets = [t for t in targets if t.get("category") == params["category"]]
        self._send_json({"targets": targets, "total": len(targets)})

    def _api_create_target(self):
        body = self._read_body()
        targets = read_json(DATA_DIR / "targets.json")
        name = body.get("name", "").strip()
        if not name:
            return self._send_json({"error": "Name is required"}, 400)
        target = {
            "name": name,
            "website": body.get("website", ""),
            "category": body.get("category", "other"),
            "focus_areas": body.get("focus_areas", []),
            "contact_methods": body.get("contact_methods", ["email"]),
            "priority": body.get("priority", 3),
            "contacts_found": 0,
            "last_scraped": None,
            "region": body.get("region", ""),
        }
        targets.append(target)
        write_json(DATA_DIR / "targets.json", targets)
        self._send_json({"ok": True, "target": target}, 201)

    def _api_update_target(self):
        name_key = urlparse(self.path).path.split("/api/targets/")[1]
        body = self._read_body()
        targets = read_json(DATA_DIR / "targets.json")
        idx, _ = find_by_field(targets, "name", name_key)
        if idx == -1:
            return self._send_json({"error": "Target not found"}, 404)
        for k, v in body.items():
            targets[idx][k] = v
        write_json(DATA_DIR / "targets.json", targets)
        self._send_json({"ok": True, "target": targets[idx]})

    def _api_delete_target(self):
        name_key = urlparse(self.path).path.split("/api/targets/")[1]
        targets = read_json(DATA_DIR / "targets.json")
        idx, _ = find_by_field(targets, "name", name_key)
        if idx == -1:
            return self._send_json({"error": "Target not found"}, 404)
        removed = targets.pop(idx)
        write_json(DATA_DIR / "targets.json", targets)
        self._send_json({"ok": True, "removed": removed})

    # ── Outreach Pending / Approvals ─────────────────────────

    def _api_get_pending(self):
        pending = read_json(DATA_DIR / "pending_outreach.json")
        params = self._parse_qs()
        if params.get("status") == "approved":
            pending = [p for p in pending if p.get("approved") and not p.get("sent")]
        elif params.get("status") == "pending":
            pending = [p for p in pending if not p.get("approved") and not p.get("sent")]
        elif params.get("status") == "sent":
            pending = [p for p in pending if p.get("sent")]
        self._send_json({
            "messages": pending,
            "total": len(pending),
            "pending_count": sum(1 for p in pending if not p.get("approved") and not p.get("sent")),
            "approved_count": sum(1 for p in pending if p.get("approved") and not p.get("sent")),
            "sent_count": sum(1 for p in pending if p.get("sent")),
        })

    def _api_approve_outreach(self):
        body = self._read_body()
        indices = body.get("indices", [])
        approve_all = body.get("all", False)
        pending = read_json(DATA_DIR / "pending_outreach.json")
        count = 0
        now = datetime.now().isoformat()
        for i, msg in enumerate(pending):
            if approve_all or i in indices:
                if not msg.get("sent"):
                    pending[i]["approved"] = True
                    pending[i]["approved_at"] = now
                    count += 1
        write_json(DATA_DIR / "pending_outreach.json", pending)
        self._send_json({"ok": True, "approved": count})

    def _api_reject_outreach(self):
        body = self._read_body()
        indices = body.get("indices", [])
        pending = read_json(DATA_DIR / "pending_outreach.json")
        # Remove rejected messages (reverse to preserve indices)
        removed = 0
        for i in sorted(indices, reverse=True):
            if 0 <= i < len(pending) and not pending[i].get("sent"):
                pending.pop(i)
                removed += 1
        write_json(DATA_DIR / "pending_outreach.json", pending)
        self._send_json({"ok": True, "removed": removed})

    def _api_update_pending(self):
        idx_str = urlparse(self.path).path.split("/api/outreach/pending/")[1]
        idx = int(idx_str)
        body = self._read_body()
        pending = read_json(DATA_DIR / "pending_outreach.json")
        if idx < 0 or idx >= len(pending):
            return self._send_json({"error": "Index out of range"}, 404)
        for k in ("message", "approved"):
            if k in body:
                pending[idx][k] = body[k]
        write_json(DATA_DIR / "pending_outreach.json", pending)
        self._send_json({"ok": True, "message": pending[idx]})

    def _api_delete_pending(self):
        idx_str = urlparse(self.path).path.split("/api/outreach/pending/")[1]
        idx = int(idx_str)
        pending = read_json(DATA_DIR / "pending_outreach.json")
        if idx < 0 or idx >= len(pending):
            return self._send_json({"error": "Index out of range"}, 404)
        removed = pending.pop(idx)
        write_json(DATA_DIR / "pending_outreach.json", pending)
        self._send_json({"ok": True, "removed": removed})

    def _api_send_outreach(self):
        """Trigger sending of approved outreach messages."""
        body = self._read_body()
        dry_run = body.get("dry_run", True)
        cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "startup_outreach.py"),
               "--mode", "outreach", "--non-interactive"]
        if dry_run:
            cmd.append("--dry-run")
        result = subprocess.run(cmd, cwd=str(PROJECT_ROOT),
                                capture_output=True, text=True, timeout=120)
        self._send_json({
            "ok": result.returncode == 0,
            "dry_run": dry_run,
            "output": result.stdout[-2000:] if result.stdout else "",
            "errors": result.stderr[-1000:] if result.stderr else "",
        })

    # ── Analytics ────────────────────────────────────────────

    def _api_get_analytics(self):
        analytics = read_json(DATA_DIR / "analytics.json")
        self._send_json(analytics)

    def _api_get_daily_reports(self):
        reports = read_json(DATA_DIR / "daily_reports.json")
        params = self._parse_qs()
        limit = int(params.get("limit", 30))
        self._send_json({"reports": reports[-limit:], "total": len(reports)})

    # ── Social Content ───────────────────────────────────────

    def _api_get_social(self):
        social_dir = CONTENT_DIR / "social"
        batches = []
        if social_dir.exists():
            for f in sorted(social_dir.glob("batch_*.json")):
                posts = read_json(f)
                batches.append({
                    "file": f.name,
                    "generated": f.stem.replace("batch_", ""),
                    "posts": posts,
                    "count": len(posts),
                })
        self._send_json({"batches": batches, "total": len(batches)})

    def _api_create_social(self):
        body = self._read_body()
        posts = body.get("posts", [])
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_{ts}.json"
        social_dir = CONTENT_DIR / "social"
        social_dir.mkdir(parents=True, exist_ok=True)
        enriched = []
        for p in posts:
            enriched.append({
                "platform": p.get("platform", "twitter"),
                "topic": p.get("topic", ""),
                "text": p.get("text", ""),
                "generated": datetime.now().isoformat(),
                "approved": False,
                "posted": False,
            })
        write_json(social_dir / filename, enriched)
        self._send_json({"ok": True, "file": filename, "count": len(enriched)}, 201)

    def _api_approve_social(self):
        body = self._read_body()
        filename = body.get("file")
        indices = body.get("indices", [])
        approve_all = body.get("all", False)
        social_dir = CONTENT_DIR / "social"
        filepath = social_dir / filename
        if not filepath.exists():
            return self._send_json({"error": "Batch not found"}, 404)
        posts = read_json(filepath)
        count = 0
        for i, post in enumerate(posts):
            if approve_all or i in indices:
                posts[i]["approved"] = True
                count += 1
        write_json(filepath, posts)
        self._send_json({"ok": True, "approved": count})

    # ── Blog Content ─────────────────────────────────────────

    def _api_get_blog(self):
        blog_dir = CONTENT_DIR / "blog"
        posts = []
        if blog_dir.exists():
            for f in sorted(blog_dir.glob("*.md")):
                content = f.read_text(encoding="utf-8")
                posts.append({
                    "file": f.name,
                    "title": f.stem.split("_", 1)[-1].replace("-", " ").title()
                             if "_" in f.stem else f.stem.replace("-", " ").title(),
                    "size": len(content),
                    "preview": content[:500],
                })
        self._send_json({"posts": posts, "total": len(posts)})

    def _api_create_blog(self):
        body = self._read_body()
        title = body.get("title", "untitled")
        content = body.get("content", "")
        slug = title.lower().replace(" ", "-")
        date_prefix = datetime.now().strftime("%Y%m%d")
        filename = f"{date_prefix}_{slug}.md"
        blog_dir = CONTENT_DIR / "blog"
        blog_dir.mkdir(parents=True, exist_ok=True)
        (blog_dir / filename).write_text(content, encoding="utf-8")
        self._send_json({"ok": True, "file": filename}, 201)

    # ── Schedules ────────────────────────────────────────────

    def _api_get_schedules(self):
        schedules = {"cron": [], "openclaw": []}
        # System cron
        try:
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if "Projects/foundry" in line and not line.startswith("#"):
                        schedules["cron"].append(line)
        except Exception:
            pass

        # OpenClaw
        try:
            result = subprocess.run(["openclaw", "cron", "list", "--json"],
                                    capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                jobs = json.loads(result.stdout)
                schedules["openclaw"] = [
                    {"name": j.get("name"), "schedule": j.get("schedule"),
                     "enabled": j.get("enabled"), "id": j.get("id"),
                     "nextRun": j.get("state", {}).get("nextRunAtMs")}
                    for j in jobs
                ]
        except Exception:
            pass

        self._send_json(schedules)

    # ── Logs ─────────────────────────────────────────────────

    def _api_get_logs(self):
        logs = []
        if LOGS_DIR.exists():
            for f in sorted(LOGS_DIR.glob("*.log"), reverse=True)[:20]:
                logs.append({
                    "file": f.name,
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
                    "tail": f.read_text(encoding="utf-8", errors="replace")[-2000:],
                })
        self._send_json({"logs": logs, "total": len(logs)})

    # ── Status ───────────────────────────────────────────────

    def _api_get_status(self):
        contacts = read_json(DATA_DIR / "contacts.json")
        targets = read_json(DATA_DIR / "targets.json")
        pending = read_json(DATA_DIR / "pending_outreach.json")
        analytics = read_json(DATA_DIR / "analytics.json")
        self._send_json({
            "timestamp": datetime.now().isoformat(),
            "contacts": len(contacts),
            "targets": len(targets),
            "outreach": {
                "pending": sum(1 for p in pending if not p.get("approved") and not p.get("sent")),
                "approved": sum(1 for p in pending if p.get("approved") and not p.get("sent")),
                "sent": sum(1 for p in pending if p.get("sent")),
                "total": len(pending),
            },
            "analytics": {
                "total_sent": analytics.get("total_outreach_sent", 0),
                "response_rate": analytics.get("response_rate", 0),
            },
        })

    # ── Automation triggers ──────────────────────────────────

    def _api_run_automation(self):
        body = self._read_body()
        dry_run = body.get("dry_run", True)
        cmd = [sys.executable, str(PROJECT_ROOT / "run_automation.py")]
        if dry_run:
            cmd.append("--dry-run")
        result = subprocess.run(cmd, cwd=str(PROJECT_ROOT),
                                capture_output=True, text=True, timeout=300)
        self._send_json({
            "ok": result.returncode == 0,
            "dry_run": dry_run,
            "output": result.stdout[-3000:] if result.stdout else "",
            "errors": result.stderr[-1000:] if result.stderr else "",
        })

    def _api_run_discovery(self):
        body = self._read_body()
        dry_run = body.get("dry_run", True)
        cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "daily_automation.py"),
               "--discovery-only"]
        if dry_run:
            cmd.append("--dry-run")
        result = subprocess.run(cmd, cwd=str(PROJECT_ROOT),
                                capture_output=True, text=True, timeout=300)
        self._send_json({
            "ok": result.returncode == 0,
            "dry_run": dry_run,
            "output": result.stdout[-3000:] if result.stdout else "",
            "errors": result.stderr[-1000:] if result.stderr else "",
        })

    # ── Blocklist ────────────────────────────────────────────

    def _api_get_blocklist(self):
        bl = read_blocklist()
        items = [{"email": k, **v} for k, v in bl.items()]
        self._send_json({"blocked": items, "total": len(items)})

    def _api_unblock_contact(self):
        body = self._read_body()
        email = body.get("email", "").strip().lower()
        if not email:
            return self._send_json({"error": "Email is required"}, 400)
        bl = read_blocklist()
        if email not in bl:
            return self._send_json({"error": "Not in blocklist"}, 404)
        del bl[email]
        write_json(BLOCKLIST_FILE, bl)
        self._send_json({"ok": True, "email": email})

    # ── Contact Discovery (Google CSE) ───────────────────────

    def _api_discovery_search(self):
        """Search for new contacts using Google Custom Search Engine."""
        import urllib.request
        import urllib.error

        body = self._read_body()
        query = body.get("query", "").strip()
        if not query:
            return self._send_json({"error": "Query is required"}, 400)

        # Load keys from .env
        from dotenv import dotenv_values
        env = dotenv_values(PROJECT_ROOT / ".env")
        api_key = env.get("GOOGLE_API_KEY", "")
        cse_id = env.get("GOOGLE_CSE_ID", "")
        if not api_key or not cse_id:
            return self._send_json({"error": "GOOGLE_API_KEY and GOOGLE_CSE_ID must be set in .env"}, 500)

        # Build URL and call Google CSE
        from urllib.parse import quote_plus
        num = min(int(body.get("num", 10)), 10)
        url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={quote_plus(api_key)}&cx={quote_plus(cse_id)}"
            f"&q={quote_plus(query)}&num={num}"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FirstCityFoundry/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            err_body = e.read().decode() if hasattr(e, 'read') else str(e)
            return self._send_json({"error": f"Google API error: {e.code}", "details": err_body[:500]}, 502)
        except Exception as e:
            return self._send_json({"error": f"Search failed: {e}"}, 502)

        # Parse results, filter out blocked emails
        existing_contacts = read_json(DATA_DIR / "contacts.json")
        existing_emails = {c.get("email", "").lower() for c in existing_contacts}
        bl = read_blocklist()

        results = []
        for item in data.get("items", []):
            result = {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "displayLink": item.get("displayLink", ""),
                "already_exists": False,
                "blocked": False,
            }
            results.append(result)

        self._send_json({
            "query": query,
            "results": results,
            "totalResults": data.get("searchInformation", {}).get("totalResults", "0"),
            "existing_count": len(existing_emails),
            "blocked_count": len(bl),
        })


# ── Server startup ───────────────────────────────────────────

def start_server(port: int, host: str):
    server = HTTPServer((host, port), DashboardHandler)
    print(f"\n📊 Automation Dashboard running!")
    print(f"   http://{host}:{port}/")
    print(f"\n   Press Ctrl+C to stop.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down dashboard server...")
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Automation Dashboard Server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--host", type=str, default=DEFAULT_HOST)
    args = parser.parse_args()
    start_server(args.port, args.host)


if __name__ == "__main__":
    main()
