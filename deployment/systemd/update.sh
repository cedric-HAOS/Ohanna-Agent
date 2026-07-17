#!/usr/bin/env bash

set -Eeuo pipefail

readonly SERVICE_NAME="ohanna-agent"
readonly INSTALL_ROOT="/opt/ohanna-agent"
readonly VENV_PATH="${INSTALL_ROOT}/venv"
readonly NEXT_VENV_PATH="${INSTALL_ROOT}/venv.next"
readonly PREVIOUS_VENV_PATH="${INSTALL_ROOT}/venv.previous"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

PYTHON_BIN="${PYTHON_BIN:-python3.13}"
PACKAGE_SOURCE="${1:-${PROJECT_ROOT}}"

SERVICE_WAS_ACTIVE=false
UPDATE_COMMITTED=false

log() {
    printf '[ohanna-agent] %s\n' "$*"
}

fail() {
    printf '[ohanna-agent] ERROR: %s\n' "$*" >&2
    exit 1
}

require_root() {
    [[ "${EUID}" -eq 0 ]] || fail "This script must be run as root."
}

require_command() {
    command -v "$1" >/dev/null 2>&1 \
        || fail "Required command not found: $1"
}

restore_previous_version() {
    if [[ "${UPDATE_COMMITTED}" == true ]]; then
        return
    fi

    if [[ -d "${PREVIOUS_VENV_PATH}" && ! -e "${VENV_PATH}" ]]; then
        log "Restoring the previous environment."
        mv "${PREVIOUS_VENV_PATH}" "${VENV_PATH}"
    fi

    rm -rf "${NEXT_VENV_PATH}"

    if [[ "${SERVICE_WAS_ACTIVE}" == true && -d "${VENV_PATH}" ]]; then
        systemctl start "${SERVICE_NAME}.service" || true
    fi
}

prepare_environment() {
    rm -rf "${NEXT_VENV_PATH}"

    "${PYTHON_BIN}" -m venv "${NEXT_VENV_PATH}"
    "${NEXT_VENV_PATH}/bin/python" -m pip install --upgrade pip
    "${NEXT_VENV_PATH}/bin/python" -m pip install "${PACKAGE_SOURCE}"

    "${NEXT_VENV_PATH}/bin/ohanna-agent" --version
}

replace_environment() {
    if systemctl is-active --quiet "${SERVICE_NAME}.service"; then
        SERVICE_WAS_ACTIVE=true
        systemctl stop "${SERVICE_NAME}.service"
    fi

    rm -rf "${PREVIOUS_VENV_PATH}"
    mv "${VENV_PATH}" "${PREVIOUS_VENV_PATH}"
    mv "${NEXT_VENV_PATH}" "${VENV_PATH}"

    systemctl daemon-reload

    if [[ "${SERVICE_WAS_ACTIVE}" == true ]]; then
        if ! systemctl start "${SERVICE_NAME}.service"; then
            log "The updated service failed to start. Rolling back."

            rm -rf "${VENV_PATH}"
            mv "${PREVIOUS_VENV_PATH}" "${VENV_PATH}"
            systemctl start "${SERVICE_NAME}.service"

            fail "Update rolled back."
        fi
    fi

    UPDATE_COMMITTED=true
    rm -rf "${PREVIOUS_VENV_PATH}"
}

main() {
    require_root

    require_command "${PYTHON_BIN}"
    require_command mv
    require_command rm
    require_command systemctl

    [[ -d "${VENV_PATH}" ]] \
        || fail "Ohanna-Agent is not installed in ${VENV_PATH}."

    [[ -e "${PACKAGE_SOURCE}" ]] \
        || fail "Package source not found: ${PACKAGE_SOURCE}"

    trap restore_previous_version ERR INT TERM

    prepare_environment
    replace_environment

    trap - ERR INT TERM

    log "Update completed."
    "${VENV_PATH}/bin/ohanna-agent" --version
}

main "$@"