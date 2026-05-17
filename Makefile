
SHELL := /bin/bash

.SHELLFLAGS := -eu -o pipefail -c

VALIDATION_TIMEOUT ?= 60

.PHONY: setup run verify validate build dry-run health status metrics cards workflow manifest clean

setup:

	@echo "[+] Setup complete"

run:

	@bash systems/automation/bootstrap.sh

verify:

	@$(MAKE) validate

validate:

	@echo "[validate] python syntax"
	@python3 -m py_compile scripts/build_readme.py
	@if [ -f scripts/collect_repo_metrics.py ]; then python3 -m py_compile scripts/collect_repo_metrics.py; fi
	@if [ -f scripts/generate_project_cards.py ]; then python3 -m py_compile scripts/generate_project_cards.py; fi
	@if [ -f scripts/generate_workflow_status.py ]; then python3 -m py_compile scripts/generate_workflow_status.py; fi
	@if [ -f scripts/rollback_surface.sh ]; then bash -n scripts/rollback_surface.sh; fi
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
		metrics/popdeuxrem_popdeuxrem.json \
		assets/projects/index.json \
		dist/build-manifest.json; do \
			if [ -f "$$file" ]; then python3 -m json.tool "$$file" >/dev/null; fi; \
		done
	@echo "[validate] README template markers"
	@grep -q '<!-- AUTO-GENERATED:START -->' README.base.md
	@grep -q '<!-- AUTO-GENERATED:END -->' README.base.md
	@echo "[validate] generator dry-run"
	@python3 scripts/build_readme.py --dry-run --check >/dev/null
	@echo "[validate] system health"
	@python3 -m json.tool health/system_health.json >/dev/null
	@echo "[validate] render status"
	@bash systems/intelligence/render_status.sh >/dev/null
	@echo "[validate] quantum build dry validation"
	@COMMAND_TIMEOUT="$(VALIDATION_TIMEOUT)" bash scripts/quantum_build.sh --check >/dev/null
	@echo "[validate] ok"

build:

	@bash scripts/quantum_build.sh

dry-run:

	@python3 scripts/build_readme.py --dry-run --check

health:

	@bash systems/scripts/system_health.sh

status:

	@bash systems/intelligence/render_status.sh

metrics:

	@python3 scripts/collect_repo_metrics.py

cards:

	@python3 scripts/generate_project_cards.py --limit 8

workflow:

	@python3 scripts/generate_workflow_status.py

manifest:

	@python3 scripts/build_readme.py
	@python3 -m json.tool dist/build-manifest.json >/dev/null

clean:

	@rm -f dist/build.log


.PHONY: workflow-telemetry workflow-panel workflow-sync

workflow-telemetry:
	@python3 scripts/collect_workflow_runs.py

workflow-panel:
	@python3 scripts/generate_workflow_status.py

workflow-sync:
	@python3 scripts/collect_workflow_runs.py
	@python3 scripts/generate_workflow_status.py
	@python3 scripts/build_readme.py
