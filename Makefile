SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: setup run verify validate build dry-run health status clean

setup:
	@echo "[+] Setup complete"

run:
	@bash systems/automation/bootstrap.sh

verify:
	@$(MAKE) validate

validate:
	@echo "[validate] python syntax"
	@python3 -m py_compile scripts/build_readme.py
	@echo "[validate] bash syntax"
	@for script in \
		scripts/quantum_build.sh \
		scripts/update_readme.sh \
		systems/automation/bootstrap.sh \
		systems/automation/healthcheck.sh \
		systems/intelligence/render_status.sh \
		systems/orchestrator/dispatch.sh \
		systems/orchestrator/sync.sh \
		systems/scripts/generate_metrics.sh \
		systems/scripts/generate_readme.sh \
		systems/scripts/system_health.sh; do \
			if [ -f "$$script" ]; then bash -n "$$script"; fi; \
		done
	@echo "[validate] json syntax"
	@for file in \
		portfolio.json \
		skills.json \
		timeline.json \
		data/quotes.json \
		identity/repos.json \
		health/status.json \
		health/system_health.json \
		health/orchestrator.json \
		metrics/aggregate.json \
		metrics/metrics.json \
		metrics/popdeuxrem_popdeuxrem.json; do \
			if [ -f "$$file" ]; then python3 -m json.tool "$$file" >/dev/null; fi; \
		done
	@echo "[validate] README template markers"
	@grep -q '<!-- AUTO-GENERATED:START -->' README.base.md
	@grep -q '<!-- AUTO-GENERATED:END -->' README.base.md
	@echo "[validate] generator dry-run"
	@python3 scripts/build_readme.py --dry-run --check >/dev/null
	@echo "[validate] system health"
	@bash systems/scripts/system_health.sh >/dev/null
	@echo "[validate] render status"
	@bash systems/intelligence/render_status.sh >/dev/null
	@echo "[validate] quantum build dry validation"
	@bash scripts/quantum_build.sh --check >/dev/null
	@echo "[validate] ok"

build:
	@bash scripts/quantum_build.sh

dry-run:
	@python3 scripts/build_readme.py --dry-run --check

health:
	@bash systems/scripts/system_health.sh

status:
	@bash systems/intelligence/render_status.sh

clean:
	@rm -f dist/build.log
