#!/usr/bin/env bash
# Shared runtime helpers for OpenBB wrapper scripts.

resolve_openbb_python() {
    if [[ -n "${OPENBB_PYTHON:-}" ]]; then
        if [[ -x "${OPENBB_PYTHON}" ]]; then
            printf "%s\n" "${OPENBB_PYTHON}"
            return 0
        fi
        echo "OPENBB_PYTHON is set but not executable: ${OPENBB_PYTHON}" >&2
        return 1
    fi

    local venv_python="${HOME}/.local/venvs/openbb/bin/python3"
    if [[ -x "${venv_python}" ]]; then
        printf "%s\n" "${venv_python}"
        return 0
    fi

    if command -v python3 >/dev/null 2>&1; then
        command -v python3
        return 0
    fi

    echo "No usable python3 found for OpenBB wrappers." >&2
    return 1
}

setup_openbb_ld_library_path() {
    local parts=()

    if command -v nix-build >/dev/null 2>&1; then
        local libstdcpp=""
        local libz=""
        libstdcpp="$(nix-build -E "with import <nixpkgs> {}; stdenv.cc.cc.lib" --no-out-link 2>/dev/null || true)"
        libz="$(nix-build -E "with import <nixpkgs> {}; zlib" --no-out-link 2>/dev/null || true)"

        if [[ -n "${libstdcpp}" && -d "${libstdcpp}/lib" ]]; then
            parts+=("${libstdcpp}/lib")
        fi
        if [[ -n "${libz}" && -d "${libz}/lib" ]]; then
            parts+=("${libz}/lib")
        fi
    fi

    if (( ${#parts[@]} > 0 )); then
        local joined=""
        joined="$(IFS=:; echo "${parts[*]}")"
        export LD_LIBRARY_PATH="${joined}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
    fi
}

is_openbb_lock_contention() {
    local text="$1"
    [[ "${text}" == *".build.lock"* ]] \
        || [[ "${text}" == *"Another build process is running"* ]] \
        || [[ "${text}" == *"BlockingIOError"* ]] \
        || [[ "${text}" == *"Resource temporarily unavailable"* ]]
}

run_openbb_python_with_retry() {
    local script=""
    script="$(cat)"

    local py=""
    py="$(resolve_openbb_python)" || return 1
    setup_openbb_ld_library_path

    local max_attempts="${OPENBB_RETRY_MAX_ATTEMPTS:-6}"
    local base_delay_sec="${OPENBB_RETRY_BASE_DELAY_SEC:-2}"

    local attempt=1
    while true; do
        local output=""
        local status=0

        if output="$("${py}" 2>&1 <<<"${script}")"; then
            status=0
        else
            status=$?
        fi

        if [[ ${status} -eq 0 ]]; then
            printf "%s\n" "${output}"
            return 0
        fi

        if is_openbb_lock_contention "${output}"; then
            if [[ ${attempt} -ge ${max_attempts} ]]; then
                {
                    echo "OpenBB wrapper failed after ${max_attempts} lock-contention retries."
                    echo "${output}"
                } >&2
                return "${status}"
            fi

            local delay=$((base_delay_sec * (2 ** (attempt - 1))))
            echo "OpenBB build lock detected, retry ${attempt}/${max_attempts} in ${delay}s..." >&2
            sleep "${delay}"
            attempt=$((attempt + 1))
            continue
        fi

        printf "%s\n" "${output}" >&2
        return "${status}"
    done
}
