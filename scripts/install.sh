#!/usr/bin/env bash
set -euo pipefail

APP_NAME="callumployed"
REPO_URL="${CALLUMPLOYED_REPO_URL:-https://github.com/callummackenzie/callumployed.git}"
INSTALL_ROOT="${CALLUMPLOYED_INSTALL_ROOT:-$HOME/.local/share/$APP_NAME}"
SOURCE_DIR="$INSTALL_ROOT/source"
BIN_DIR="${CALLUMPLOYED_BIN_DIR:-$HOME/.local/bin}"
SHIM_PATH="$BIN_DIR/$APP_NAME"
UV_BIN=""

info() {
  printf '\033[1;34m==>\033[0m %s\n' "$1"
}

warn() {
  printf '\033[1;33mwarning:\033[0m %s\n' "$1" >&2
}

fail() {
  printf '\033[1;31merror:\033[0m %s\n' "$1" >&2
  exit 1
}

have() {
  command -v "$1" >/dev/null 2>&1
}

prompt_secret() {
  local prompt="$1"
  local value=""

  [ -r /dev/tty ] || fail "interactive terminal is required for API key prompts"

  while [ -z "$value" ]; do
    printf "%s: " "$prompt" >/dev/tty
    IFS= read -rs value </dev/tty
    printf '\n' >/dev/tty
  done

  printf '%s' "$value"
}

prompt_optional_secret() {
  local prompt="$1"
  local value=""

  [ -r /dev/tty ] || fail "interactive terminal is required for API key prompts"

  printf "%s (optional, press enter to skip): " "$prompt" >/dev/tty
  IFS= read -rs value </dev/tty
  printf '\n' >/dev/tty

  printf '%s' "$value"
}

ensure_uv() {
  if have uv; then
    return
  fi

  info "Installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh

  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  have uv || fail "uv install completed, but uv was not found on PATH"
}

set_uv_bin() {
  UV_BIN="$(command -v uv)"
}

ensure_python() {
  if "$UV_BIN" python find 3.12 >/dev/null 2>&1; then
    return
  fi

  info "Installing Python 3.12 with uv"
  "$UV_BIN" python install 3.12
}

ensure_git() {
  have git || fail "git is required. Install git, then run this installer again."
}

ensure_latex() {
  if have tectonic || have latexmk || have pdflatex; then
    return
  fi

  warn "$APP_NAME requires an external LaTeX compiler for resume PDF rendering."

  if have brew; then
    [ -r /dev/tty ] || fail "interactive terminal is required for install prompts"
    printf "Install the recommended compiler with Homebrew now? [Y/n]: " >/dev/tty
    local answer=""
    IFS= read -r answer </dev/tty
    case "${answer:-Y}" in
      y|Y|yes|YES)
        info "Installing tectonic with Homebrew"
        brew install tectonic
        ;;
      *)
        fail "Install tectonic, latexmk, or pdflatex, then run this installer again."
        ;;
    esac
  else
    fail "Install tectonic, latexmk, or pdflatex, then run this installer again."
  fi
}

checkout_source() {
  mkdir -p "$INSTALL_ROOT"

  if [ -d "$SOURCE_DIR/.git" ]; then
    info "Updating existing source checkout"
    git -C "$SOURCE_DIR" pull --ff-only
  elif [ -e "$SOURCE_DIR" ]; then
    fail "$SOURCE_DIR already exists but is not a git checkout"
  else
    info "Cloning $APP_NAME"
    git clone "$REPO_URL" "$SOURCE_DIR"
  fi
}

write_env_file() {
  local openai_api_key="$1"
  local browserbase_api_key="$2"
  local env_path="$SOURCE_DIR/.env"

  info "Writing local environment config"
  {
    printf 'CALLUMPLOYED_LLM_PROVIDER=openai\n'
    printf 'CALLUMPLOYED_LLM_MODEL=gpt-4.1-mini\n'
    printf 'OPENAI_API_KEY=%s\n' "$openai_api_key"
    if [ -n "$browserbase_api_key" ]; then
      printf 'CALLUMPLOYED_BROWSER_BACKEND=browserbase\n'
      printf 'BROWSERBASE_API_KEY=%s\n' "$browserbase_api_key"
    else
      printf 'CALLUMPLOYED_BROWSER_BACKEND=local\n'
    fi
  } > "$env_path"
  chmod 600 "$env_path"
}

install_dependencies() {
  info "Installing Python dependencies"
  (
    cd "$SOURCE_DIR"
    "$UV_BIN" venv --python 3.12
    "$UV_BIN" pip install --upgrade pip
    "$UV_BIN" pip install -e ".[agents,mcp]"
    "$UV_BIN" run playwright install chromium
  )
}

write_shim() {
  mkdir -p "$BIN_DIR"

  info "Creating $SHIM_PATH"
  cat > "$SHIM_PATH" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$SOURCE_DIR"
exec "$UV_BIN" run callumployed "\$@"
EOF
  chmod +x "$SHIM_PATH"
}

print_next_steps() {
  info "Installed $APP_NAME"
  printf '\n'
  printf 'Run the CLI with:\n'
  printf '  %s --help\n' "$SHIM_PATH"
  printf '\n'
  printf 'Start the local web tracker with:\n'
  printf '  %s serve\n' "$SHIM_PATH"
  printf '\n'
  printf 'Central company ID sync uses the deployed store by default.\n'
  printf 'Add the private role-feed passkey from web settings or with:\n'
  printf '  %s central configure --prompt-passkey\n' "$SHIM_PATH"
  printf '\n'

  case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *)
      warn "$BIN_DIR is not on PATH. Add this to your shell profile:"
      printf '  export PATH="%s:$PATH"\n' "$BIN_DIR"
      ;;
  esac
}

main() {
  info "Installing $APP_NAME"
  ensure_git
  ensure_latex
  ensure_uv
  set_uv_bin
  ensure_python
  checkout_source

  local openai_api_key=""
  local browserbase_api_key=""
  openai_api_key="$(prompt_secret "OpenAI API key")"
  browserbase_api_key="$(prompt_optional_secret "Browserbase API key")"

  write_env_file "$openai_api_key" "$browserbase_api_key"
  install_dependencies
  write_shim
  print_next_steps
}

main "$@"
