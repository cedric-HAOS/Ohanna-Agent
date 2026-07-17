#!/usr/bin/env bash

set -Eeuo pipefail

readonly SERVICE_NAME="ohanna-agent"
readonly SERVICE_USER="ohanna-agent"
readonly SERVICE_GROUP="ohanna-agent"

readonly INSTALL_ROOT="/opt/ohanna-agent"
readonly VENV_PATH="${INSTALL_ROOT}/venv"
readonly CONFIG_ROOT="/etc/ohanna-agent"
readonly PLUGIN_CONFIG_ROOT="${CONFIG_ROOT}/plugins"
readonly SYSTEMD_UNIT="/etc/systemd/system/${SERVICE_NAME}.service"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

PYTHON_BIN="${PYTHON_BIN:-python3.13}"
PACKAGE_SOURCE="${1:-${PROJECT_ROOT}}"

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

install_config_if_missing() {
    local source_path="$1"
    local destination_path="$2"

    if [[ -e "${destination_path}" ]]; then
        log "Keeping existing configuration: ${destination_path}"
        return
    fi

    [[ -f "${source_path}" ]] \
        || fail "Example configuration not found: ${source_path}"

    install \
        -o root \
        -g "${SERVICE_GROUP}" \
        -m 0640 \
        "${source_path}" \
        "${destination_path}"

    log "Created configuration: ${destination_path}"
}

create_service_account() {
    if ! getent group "${SERVICE_GROUP}" >/dev/null; then
        groupadd --system "${SERVICE_GROUP}"
        log "Created system group: ${SERVICE_GROUP}"
    fi

    if ! id "${SERVICE_USER}" >/dev/null 2>&1; then
        useradd \
            --system \
            --gid "${SERVICE_GROUP}" \
            --home-dir /nonexistent \
            --no-create-home \
            --shell /usr/sbin/nologin \
            "${SERVICE_USER}"

        log "Created system user: ${SERVICE_USER}"
    fi
}

install_application() {
    install -d -o root -g root -m 0755 "${INSTALL_ROOT}"

    if [[ -e "${VENV_PATH}" ]]; then
        fail "${VENV_PATH} already exists. Use deployment/update.sh."
    fi

    "${PYTHON_BIN}" -m venv "${VENV_PATH}"
    "${VENV_PATH}/bin/python" -m pip install --upgrade pip
    "${VENV_PATH}/bin/python" -m pip install "${PACKAGE_SOURCE}"

    "${VENV_PATH}/bin/ohanna-agent" --version
}

install_configuration() {
    install -d \
        -o root \
        -g "${SERVICE_GROUP}" \
        -m 0750 \
        "${CONFIG_ROOT}" \
        "${PLUGIN_CONFIG_ROOT}"

    install_config_if_missing \
        "${PROJECT_ROOT}/config/shikamaru.example.yaml" \
        "${CONFIG_ROOT}/shikamaru.yaml"

    install_config_if_missing \
        "${PROJECT_ROOT}/config/infrastructure.example.yaml" \
        "${CONFIG_ROOT}/infrastructure.yaml"

    install_config_if_missing \
        "${PROJECT_ROOT}/config/plugins/dns.example.yaml" \
        "${PLUGIN_CONFIG_ROOT}/dns.yaml"
}

install_systemd_service() {
    local source_unit="${PROJECT_ROOT}/deployment/systemd/${SERVICE_NAME}.service"

    [[ -f "${source_unit}" ]] \
        || fail "Systemd unit not found: ${source_unit}"

    install \
        -o root \
        -g root \
        -m 0644 \
        "${source_unit}" \
        "${SYSTEMD_UNIT}"

    systemctl daemon-reload
    systemctl enable "${SERVICE_NAME}.service"

    log "Installed systemd unit: ${SYSTEMD_UNIT}"
}

main() {
    require_root

    require_command "${PYTHON_BIN}"
    require_command getent
    require_command groupadd
    require_command id
    require_command useradd
    require_command install
    require_command systemctl

    [[ -e "${PACKAGE_SOURCE}" ]] \
        || fail "Package source not found: ${PACKAGE_SOURCE}"

    create_service_account
    install_application
    install_configuration
    install_systemd_service

    log "Installation completed."
    log "Review the files in ${CONFIG_ROOT} before starting the service."
    log "Start with: systemctl start ${SERVICE_NAME}"
}

main "$@"