#!/usr/bin/env bash

set -Eeuo pipefail

readonly SERVICE_NAME="ohanna-agent"
readonly INSTALL_ROOT="/opt/ohanna-agent"
readonly VENV_PATH="${INSTALL_ROOT}/venv"
readonly SYSTEMD_UNIT="/etc/systemd/system/${SERVICE_NAME}.service"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

PACKAGE_SOURCE="${1:-${PROJECT_ROOT}}"
SERVICE_WAS_ACTIVE=false

log() {
    printf '[ohanna-agent] %s\n' "$*"
}

fail() {
    printf '[ohanna-agent] ERROR: %s\n' "$*" >&2
    exit 1
}

require_root() {
    [[ "${EUID}" -eq 0 ]] \
        || fail "This script must be run as root."
}

require_command() {
    command -v "$1" >/dev/null 2>&1 \
        || fail "Required command not found: $1"
}

validate_environment() {
    [[ -x "${VENV_PATH}/bin/python" ]] \
        || fail "Ohanna-Agent is not installed in ${VENV_PATH}."

    [[ -x "${VENV_PATH}/bin/ohanna-agent" ]] \
        || fail "Ohanna-Agent executable not found."

    [[ -e "${PACKAGE_SOURCE}" ]] \
        || fail "Package source not found: ${PACKAGE_SOURCE}"

    [[ -f \
        "${PROJECT_ROOT}/deployment/systemd/${SERVICE_NAME}.service" ]] \
        || fail "Reference systemd unit not found."
}

restart_service_after_failure() {
    if [[ "${SERVICE_WAS_ACTIVE}" == true ]]; then
        log "Update failed. Attempting to restart the service."
        systemctl start "${SERVICE_NAME}.service" || true
    fi
}

stop_service_if_active() {
    if systemctl is-active --quiet "${SERVICE_NAME}.service"; then
        SERVICE_WAS_ACTIVE=true
        log "Stopping ${SERVICE_NAME}."
        systemctl stop "${SERVICE_NAME}.service"
    fi
}

update_application() {
    log "Updating Ohanna-Agent from ${PACKAGE_SOURCE}."

    "${VENV_PATH}/bin/python" \
        -m pip install \
        --upgrade \
        "${PACKAGE_SOURCE}"

    "${VENV_PATH}/bin/ohanna-agent" --version
}

update_service_unit() {
    local source_unit

    source_unit="${PROJECT_ROOT}/deployment/systemd/${SERVICE_NAME}.service"

    install \
        -o root \
        -g root \
        -m 0644 \
        "${source_unit}" \
        "${SYSTEMD_UNIT}"

    systemctl daemon-reload
}

start_service_if_needed() {
    if [[ "${SERVICE_WAS_ACTIVE}" == true ]]; then
        log "Starting ${SERVICE_NAME}."
        systemctl start "${SERVICE_NAME}.service"
    fi
}

main() {
    require_root

    require_command install
    require_command systemctl

    validate_environment

    trap restart_service_after_failure ERR INT TERM

    stop_service_if_active
    update_application
    update_service_unit
    start_service_if_needed

    trap - ERR INT TERM

    log "Update completed."
}

main "$@"