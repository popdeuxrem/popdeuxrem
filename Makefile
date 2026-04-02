SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

setup:
	@echo "[+] Setup complete"

run:
	@bash systems/automation/bootstrap.sh

verify:
	@bash systems/automation/healthcheck.sh