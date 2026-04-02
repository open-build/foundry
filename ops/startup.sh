#!/usr/bin/env bash
# ============================================================
# First City Foundry — Unified Startup Script
# ============================================================
# Manages all project services: site preview, ForgeWeb admin,
# OpenClaw gateway, and the Python automation venv.
#
# Usage:
#   ops/startup.sh              # start everything
#   ops/startup.sh start        # same
#   ops/startup.sh stop         # stop all services
#   ops/startup.sh restart      # stop then start
#   ops/startup.sh status       # show what's running
# ============================================================

set -euo pipefail

# ── Colors ───────────────────────────────────────────────────
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

# ── Paths ────────────────────────────────────────────────────
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDFILE_DIR="$PROJECT_ROOT/ops/.pids"
FORGEWEB_DIR="$PROJECT_ROOT/ForgeWeb"
VENV_DIR="$PROJECT_ROOT/.venv"

# ── Preferred ports ──────────────────────────────────────────
SITE_PREFERRED_PORT=3000
FORGEWEB_PREFERRED_PORT=8000
DASHBOARD_PREFERRED_PORT=4000
OPENCLAW_PORT=18789  # managed by openclaw itself

# ── Helpers ──────────────────────────────────────────────────

log_info()    { echo -e "${BLUE}ℹ${NC}  $*"; }
log_ok()      { echo -e "${GREEN}✓${NC}  $*"; }
log_warn()    { echo -e "${YELLOW}⚠${NC}  $*"; }
log_err()     { echo -e "${RED}✗${NC}  $*"; }
log_section() { echo -e "\n${BOLD}── $* ──${NC}"; }

# Find an open port starting from $1
find_open_port() {
    local port=$1
    while lsof -Pi :"$port" -sTCP:LISTEN -t >/dev/null 2>&1; do
        port=$((port + 1))
    done
    echo "$port"
}

# Read a saved PID; empty string if none
read_pid() {
    local name=$1
    local f="$PIDFILE_DIR/${name}.pid"
    [[ -f "$f" ]] && cat "$f" || echo ""
}

# Save a PID
save_pid() {
    mkdir -p "$PIDFILE_DIR"
    echo "$2" > "$PIDFILE_DIR/${1}.pid"
}

# Remove a PID file
clear_pid() {
    rm -f "$PIDFILE_DIR/${1}.pid"
}

# Save the port a service is running on
save_port() {
    mkdir -p "$PIDFILE_DIR"
    echo "$2" > "$PIDFILE_DIR/${1}.port"
}

read_port() {
    local f="$PIDFILE_DIR/${1}.port"
    [[ -f "$f" ]] && cat "$f" || echo ""
}

clear_port() {
    rm -f "$PIDFILE_DIR/${1}.port"
}

# Kill a named service by its PID file
kill_service() {
    local name=$1
    local pid
    pid=$(read_pid "$name")
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        kill "$pid" 2>/dev/null || true
        sleep 1
        if kill -0 "$pid" 2>/dev/null; then
            kill -9 "$pid" 2>/dev/null || true
            sleep 1
        fi
        log_ok "Stopped $name (PID $pid)"
    else
        # Try to find by port
        local port
        port=$(read_port "$name")
        if [[ -n "$port" ]]; then
            local found
            found=$(lsof -Pi :"$port" -sTCP:LISTEN -t 2>/dev/null || echo "")
            if [[ -n "$found" ]]; then
                kill "$found" 2>/dev/null || true
                sleep 1
                log_ok "Stopped $name (port $port)"
            fi
        fi
    fi
    clear_pid "$name"
    clear_port "$name"
}

# ── Venv & Dependencies ─────────────────────────────────────

ensure_venv() {
    log_section "Python Environment"

    if [[ ! -d "$VENV_DIR" ]]; then
        log_info "Creating virtual environment at .venv ..."
        python3 -m venv "$VENV_DIR"
        log_ok "Virtual environment created"
    else
        log_ok "Virtual environment exists"
    fi

    # Activate
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"

    # Install/update requirements
    local updated=0
    for req in "$PROJECT_ROOT/requirements_outreach.txt" \
               "$PROJECT_ROOT/requirements.txt"; do
        if [[ -s "$req" ]]; then
            log_info "Installing $(basename "$req") ..."
            pip install -q -r "$req" 2>&1 | tail -1
            updated=1
        fi
    done

    if [[ $updated -eq 1 ]]; then
        log_ok "Python dependencies up to date"
    fi
}

# ── Service: Static Site Preview ─────────────────────────────

start_site_preview() {
    log_section "Site Preview (serve)"

    local port
    port=$(find_open_port "$SITE_PREFERRED_PORT")

    if [[ "$port" -ne "$SITE_PREFERRED_PORT" ]]; then
        log_warn "Port $SITE_PREFERRED_PORT busy — using $port"
    fi

    # Ensure 'serve' is available
    if ! command -v npx >/dev/null 2>&1; then
        log_err "npx not found — install Node.js to enable site preview"
        return 1
    fi

    npx --yes serve "$PROJECT_ROOT/docs" -p "$port" -L >/dev/null 2>&1 &
    local pid=$!
    sleep 2

    if kill -0 "$pid" 2>/dev/null; then
        save_pid "site-preview" "$pid"
        save_port "site-preview" "$port"
        log_ok "Site preview running → ${BOLD}http://localhost:${port}${NC}"
    else
        log_err "Site preview failed to start"
        return 1
    fi
}

# ── Service: ForgeWeb Admin ──────────────────────────────────

start_forgeweb() {
    log_section "ForgeWeb Admin"

    if [[ ! -f "$FORGEWEB_DIR/admin/file-api.py" ]]; then
        log_err "ForgeWeb not found (missing admin/file-api.py)"
        return 1
    fi

    # Setup ForgeWeb venv if needed
    if [[ ! -d "$FORGEWEB_DIR/venv" ]]; then
        log_info "Creating ForgeWeb venv ..."
        python3 -m venv "$FORGEWEB_DIR/venv"
    fi
    # shellcheck disable=SC1091
    source "$FORGEWEB_DIR/venv/bin/activate"
    pip install -q -r "$FORGEWEB_DIR/requirements.txt" 2>&1 | tail -1

    # Initialize DB if needed
    if [[ -f "$FORGEWEB_DIR/admin/database.py" ]]; then
        (cd "$FORGEWEB_DIR" && python3 admin/database.py 2>/dev/null) || true
    fi

    local port
    port=$(find_open_port "$FORGEWEB_PREFERRED_PORT")

    if [[ "$port" -ne "$FORGEWEB_PREFERRED_PORT" ]]; then
        log_warn "Port $FORGEWEB_PREFERRED_PORT busy — using $port"
    fi

    (cd "$FORGEWEB_DIR/admin" && python3 file-api.py --port "$port" >/dev/null 2>&1 &)
    local pid=$!
    sleep 2

    # Grab PID by port since bg subshell PID may differ
    local real_pid
    real_pid=$(lsof -Pi :"$port" -sTCP:LISTEN -t 2>/dev/null || echo "")
    if [[ -n "$real_pid" ]]; then
        save_pid "forgeweb" "$real_pid"
        save_port "forgeweb" "$port"
        log_ok "ForgeWeb admin running → ${BOLD}http://localhost:${port}/admin/${NC}"
    else
        log_err "ForgeWeb failed to start on port $port"
        return 1
    fi

    # Switch back to project venv
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate" 2>/dev/null || true
}

# ── Service: OpenClaw Gateway ────────────────────────────────

start_openclaw() {
    log_section "OpenClaw Gateway"

    if ! command -v openclaw >/dev/null 2>&1; then
        log_warn "openclaw CLI not found — skipping"
        return 0
    fi

    # Check if already running
    if lsof -Pi :"$OPENCLAW_PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
        local pid
        pid=$(lsof -Pi :"$OPENCLAW_PORT" -sTCP:LISTEN -t 2>/dev/null)
        save_pid "openclaw" "$pid"
        save_port "openclaw" "$OPENCLAW_PORT"
        log_ok "OpenClaw gateway already running → ${BOLD}http://127.0.0.1:${OPENCLAW_PORT}/${NC}"
        return 0
    fi

    log_info "Starting OpenClaw gateway ..."
    openclaw daemon start >/dev/null 2>&1 || openclaw gateway start >/dev/null 2>&1 || true
    sleep 3

    if lsof -Pi :"$OPENCLAW_PORT" -sTCP:LISTEN -t >/dev/null 2>&1; then
        local pid
        pid=$(lsof -Pi :"$OPENCLAW_PORT" -sTCP:LISTEN -t 2>/dev/null)
        save_pid "openclaw" "$pid"
        save_port "openclaw" "$OPENCLAW_PORT"
        log_ok "OpenClaw gateway running → ${BOLD}http://127.0.0.1:${OPENCLAW_PORT}/${NC}"
    else
        log_warn "OpenClaw gateway did not start — cron jobs will run next time it's available"
    fi
}

# ── Service: Dashboard Server ─────────────────────────────

start_dashboard() {
    log_section "Automation Dashboard"

    local port
    port=$(find_open_port "$DASHBOARD_PREFERRED_PORT")

    if [[ "$port" -ne "$DASHBOARD_PREFERRED_PORT" ]]; then
        log_warn "Port $DASHBOARD_PREFERRED_PORT busy — using $port"
    fi

    # Ensure project venv active
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate" 2>/dev/null || true

    python3 "$PROJECT_ROOT/ops/dashboard_server.py" --port "$port" >/dev/null 2>&1 &
    sleep 2

    local real_pid
    real_pid=$(lsof -Pi :"$port" -sTCP:LISTEN -t 2>/dev/null || echo "")
    if [[ -n "$real_pid" ]]; then
        save_pid "dashboard" "$real_pid"
        save_port "dashboard" "$port"
        log_ok "Dashboard running → ${BOLD}http://localhost:${port}${NC}"
    else
        log_err "Dashboard failed to start on port $port"
        return 1
    fi
}

# ── Orchestration ────────────────────────────────────────────

do_start() {
    echo -e "\n${BOLD}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║        🚀  First City Foundry — Starting Up  🚀       ║${NC}"
    echo -e "${BOLD}╚═══════════════════════════════════════════════════════╝${NC}"

    ensure_venv
    start_site_preview
    start_forgeweb
    start_dashboard
    start_openclaw

    print_summary
}

do_stop() {
    echo -e "\n${BOLD}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║        🛑  First City Foundry — Stopping  🛑          ║${NC}"
    echo -e "${BOLD}╚═══════════════════════════════════════════════════════╝${NC}\n"

    kill_service "site-preview"
    kill_service "forgeweb"
    kill_service "dashboard"
    # Don't stop OpenClaw — it's a shared system daemon
    log_info "OpenClaw gateway left running (shared daemon)"
    echo ""
    log_ok "All project services stopped"
}

do_restart() {
    do_stop
    sleep 1
    do_start
}

do_status() {
    echo -e "\n${BOLD}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║        📊  First City Foundry — Service Status        ║${NC}"
    echo -e "${BOLD}╚═══════════════════════════════════════════════════════╝${NC}\n"

    print_service_status "site-preview"  "Site Preview"
    print_service_status "forgeweb"      "ForgeWeb Admin"
    print_service_status "dashboard"     "Dashboard"
    print_service_status "openclaw"      "OpenClaw Gateway"

    echo ""
    # Venv status
    if [[ -d "$VENV_DIR" ]]; then
        log_ok "Python venv: $VENV_DIR"
    else
        log_warn "Python venv: not created"
    fi

    # Cron status
    local cron_count
    cron_count=$(crontab -l 2>/dev/null | grep -c "Projects/foundry" || echo 0)
    if [[ "$cron_count" -gt 0 ]]; then
        log_ok "System cron: $cron_count foundry jobs"
    else
        log_warn "System cron: no foundry jobs"
    fi

    # OpenClaw jobs
    if command -v openclaw >/dev/null 2>&1; then
        local oc_count
        oc_count=$(openclaw cron list --json 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
        log_ok "OpenClaw cron: $oc_count scheduled jobs"
    fi
}

print_service_status() {
    local name=$1
    local label=$2
    local pid port

    pid=$(read_pid "$name")
    port=$(read_port "$name")

    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
        log_ok "$label: ${GREEN}running${NC} (PID $pid, port $port)"
    elif [[ -n "$port" ]] && lsof -Pi :"$port" -sTCP:LISTEN -t >/dev/null 2>&1; then
        local found_pid
        found_pid=$(lsof -Pi :"$port" -sTCP:LISTEN -t 2>/dev/null)
        log_ok "$label: ${GREEN}running${NC} (PID $found_pid, port $port)"
    else
        log_warn "$label: ${RED}stopped${NC}"
    fi
}

print_summary() {
    local site_port forgeweb_port dash_port oc_port
    site_port=$(read_port "site-preview")
    forgeweb_port=$(read_port "forgeweb")
    dash_port=$(read_port "dashboard")
    oc_port=$(read_port "openclaw")

    echo ""
    echo -e "${BOLD}╔═══════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}║               ✨  All Services Ready  ✨              ║${NC}"
    echo -e "${BOLD}╠═══════════════════════════════════════════════════════╣${NC}"
    [[ -n "$site_port" ]]    && echo -e "${BOLD}║${NC}  🌐 Site Preview      ${BOLD}http://localhost:${site_port}${NC}"
    [[ -n "$forgeweb_port" ]] && echo -e "${BOLD}║${NC}  🔧 ForgeWeb Admin    ${BOLD}http://localhost:${forgeweb_port}/admin/${NC}"
    [[ -n "$dash_port" ]]    && echo -e "${BOLD}║${NC}  📊 Dashboard         ${BOLD}http://localhost:${dash_port}${NC}"
    [[ -n "$oc_port" ]]      && echo -e "${BOLD}║${NC}  🦞 OpenClaw          ${BOLD}http://127.0.0.1:${oc_port}/${NC}"
    echo -e "${BOLD}║${NC}  🚀 Live Site         ${BOLD}https://www.firstcityfoundry.com${NC}"
    echo -e "${BOLD}╠═══════════════════════════════════════════════════════╣${NC}"
    echo -e "${BOLD}║${NC}  Python venv: $VENV_DIR"
    echo -e "${BOLD}║${NC}"
    echo -e "${BOLD}║${NC}  Stop:    ${YELLOW}ops/startup.sh stop${NC}"
    echo -e "${BOLD}║${NC}  Restart: ${YELLOW}ops/startup.sh restart${NC}"
    echo -e "${BOLD}║${NC}  Status:  ${YELLOW}ops/startup.sh status${NC}"
    echo -e "${BOLD}╚═══════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ── Main ─────────────────────────────────────────────────────

cd "$PROJECT_ROOT"

case "${1:-start}" in
    start)   do_start   ;;
    stop)    do_stop    ;;
    restart) do_restart ;;
    status)  do_status  ;;
    help|-h|--help)
        echo "Usage: ops/startup.sh [start|stop|restart|status|help]"
        echo ""
        echo "  start    Start all services (default)"
        echo "  stop     Stop all project services"
        echo "  restart  Stop then start"
        echo "  status   Show running services"
        ;;
    *)
        log_err "Unknown command: $1"
        echo "Usage: ops/startup.sh [start|stop|restart|status|help]"
        exit 1
        ;;
esac
