#!/usr/bin/env bash
# Rollback automation for PopDeuxRem / Lysergic GitHub Surface Engine.
#
# Modes:
#   --list
#   --from-backup <backup_dir> [--yes]
#   --revert-commit <commit_sha> [--yes]
#
# Examples:
#   bash scripts/rollback_surface.sh --list
#   bash scripts/rollback_surface.sh --from-backup .backups/pre-release-20260511T000000Z --yes
#   bash scripts/rollback_surface.sh --revert-commit abc1234 --yes

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
LOG_FILE="$LOG_DIR/rollback_surface.log"

mkdir -p "$LOG_DIR"

MODE=""
TARGET=""
ASSUME_YES="no"

usage() {
  cat <<USAGE
Usage:
  bash scripts/rollback_surface.sh --list
  bash scripts/rollback_surface.sh --from-backup <backup_dir> [--yes]
  bash scripts/rollback_surface.sh --revert-commit <commit_sha> [--yes]

Modes:
  --list
      List available .backups directories.

  --from-backup <backup_dir>
      Restore tracked surface files from a backup directory.

  --revert-commit <commit_sha>
      Run git revert against a specific commit.

Safety:
  --yes
      Skip interactive confirmation.

Notes:
  - This script does not push.
  - This script runs make validate after rollback.
  - This script refuses to run outside a Git repository.
USAGE
}

log() {
  local level="$1"
  shift
  local msg="$*"
  local ts
  ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  printf '[%s] [%s] %s\n' "$ts" "$level" "$msg" | tee -a "$LOG_FILE"
}

fail() {
  log "FAIL" "$*"
  exit 1
}

confirm() {
  local prompt="$1"

  if [[ "$ASSUME_YES" == "yes" ]]; then
    log "INFO" "Confirmation bypassed by --yes: $prompt"
    return 0
  fi

  printf '%s [type YES to continue]: ' "$prompt"
  read -r answer

  if [[ "$answer" != "YES" ]]; then
    fail "Confirmation failed. Aborting."
  fi
}

require_git_repo() {
  git -C "$ROOT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "Not inside a Git repository: $ROOT_DIR"
}

require_clean_or_confirm() {
  if [[ -n "$(git -C "$ROOT_DIR" status --porcelain)" ]]; then
    log "WARN" "Working tree has changes:"
    git -C "$ROOT_DIR" status --short | tee -a "$LOG_FILE"
    confirm "Working tree is not clean. Continue anyway?"
  fi
}

list_backups() {
  log "INFO" "Listing backups under .backups"

  if [[ ! -d "$ROOT_DIR/.backups" ]]; then
    log "WARN" "No .backups directory found."
    return 0
  fi

  find "$ROOT_DIR/.backups" -mindepth 1 -maxdepth 1 -type d | sort | sed "s#^$ROOT_DIR/##"
}

validate_after_rollback() {
  log "INFO" "Running validation after rollback"

  if make -C "$ROOT_DIR" validate; then
    log "PASS" "Validation passed after rollback"
  else
    fail "Validation failed after rollback"
  fi
}

restore_path_if_exists() {
  local backup_dir="$1"
  local path="$2"

  if [[ -e "$backup_dir/$path" ]]; then
    rm -rf "$ROOT_DIR/$path"
    mkdir -p "$(dirname "$ROOT_DIR/$path")"
    cp -a "$backup_dir/$path" "$ROOT_DIR/$path"
    log "INFO" "Restored: $path"
  else
    log "WARN" "Backup missing path: $path"
  fi
}

restore_from_backup() {
  local backup_dir="$1"

  [[ -n "$backup_dir" ]] || fail "Missing backup directory"
  [[ -d "$backup_dir" ]] || [[ -d "$ROOT_DIR/$backup_dir" ]] || fail "Backup directory not found: $backup_dir"

  if [[ -d "$ROOT_DIR/$backup_dir" ]]; then
    backup_dir="$ROOT_DIR/$backup_dir"
  fi

  log "INFO" "Preparing backup restore from: $backup_dir"

  require_clean_or_confirm
  confirm "Restore surface files from backup directory '$backup_dir'?"

  local paths=(
    "README.md"
    "README.base.md"
    "Makefile"
    "scripts"
    "systems"
    ".github/workflows"
    "assets"
    "data"
    "health"
    "metrics"
    "identity"
    "portfolio.json"
    "skills.json"
    "timeline.json"
    "CHANGELOG.md"
    "RELEASE_CHECKLIST.md"
  )

  for path in "${paths[@]}"; do
    restore_path_if_exists "$backup_dir" "$path"
  done

  validate_after_rollback

  log "PASS" "Backup restore completed"
  log "INFO" "Review changes with: git status --short && git diff --stat"
}

revert_commit() {
  local commit_sha="$1"

  [[ -n "$commit_sha" ]] || fail "Missing commit SHA"

  git -C "$ROOT_DIR" cat-file -e "${commit_sha}^{commit}" 2>/dev/null || fail "Commit not found: $commit_sha"

  require_clean_or_confirm

  log "INFO" "Preparing git revert for commit: $commit_sha"
  git -C "$ROOT_DIR" show --stat --oneline --decorate "$commit_sha" | tee -a "$LOG_FILE"

  confirm "Revert commit '$commit_sha'?"

  if git -C "$ROOT_DIR" revert --no-edit "$commit_sha"; then
    log "PASS" "Git revert completed: $commit_sha"
  else
    fail "Git revert failed. Resolve conflicts manually, then run make validate."
  fi

  validate_after_rollback

  log "PASS" "Commit revert completed"
  log "INFO" "This script does not push. Push manually after review."
}

parse_args() {
  if [[ "$#" -eq 0 ]]; then
    usage
    exit 1
  fi

  while [[ "$#" -gt 0 ]]; do
    case "$1" in
      --list)
        MODE="list"
        shift
        ;;
      --from-backup)
        MODE="from-backup"
        TARGET="${2:-}"
        shift 2
        ;;
      --revert-commit)
        MODE="revert-commit"
        TARGET="${2:-}"
        shift 2
        ;;
      --yes)
        ASSUME_YES="yes"
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        fail "Unknown argument: $1"
        ;;
    esac
  done
}

main() {
  parse_args "$@"

  cd "$ROOT_DIR"
  require_git_repo

  log "INFO" "Rollback tool started"
  log "INFO" "Mode: ${MODE:-unset}"
  log "INFO" "Root: $ROOT_DIR"

  case "$MODE" in
    list)
      list_backups
      ;;
    from-backup)
      restore_from_backup "$TARGET"
      ;;
    revert-commit)
      revert_commit "$TARGET"
      ;;
    *)
      usage
      fail "No valid mode selected"
      ;;
  esac

  log "INFO" "Rollback tool finished"
}

main "$@"
