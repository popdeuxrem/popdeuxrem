import os
import shutil
import sys
import pathlib
# Ensure 'scripts' package is importable when running tests from repo root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))
from update_readme import build_readme


def test_build_readme_writes_last_updated(tmp_path, monkeypatch):
    # Back up current README
    repo_root = os.getcwd()
    readme_path = os.path.join(repo_root, 'README.md')
    backup = None
    if os.path.exists(readme_path):
        backup = readme_path + '.testbak'
        shutil.copyfile(readme_path, backup)

    try:
        # Run the builder
        build_readme()

        # Assert README exists and contains LAST_UPDATED comment
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert '<!-- LAST_UPDATED:' in content
    finally:
        # Restore backup
        if backup and os.path.exists(backup):
            shutil.move(backup, readme_path)
        else:
            # Remove README if it didn't exist before
            if os.path.exists(readme_path):
                os.remove(readme_path)
