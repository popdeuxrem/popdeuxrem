import os
import pathlib
import shutil
import types

from scripts import fetch_external_images


class DummyHead:
    def __init__(self, headers=None):
        self._headers = headers or {}

    def raise_for_status(self):
        return None

    @property
    def headers(self):
        return self._headers


class DummyGet:
    def __init__(self, content=b'12345'):
        self.content = content

    def raise_for_status(self):
        return None


def test_process_readme_respects_max_size(tmp_path, monkeypatch):
    repo_root = tmp_path
    # set up a fake README with external image
    readme = repo_root / 'README.md'
    readme.write_text('![alt](https://example.com/image.png)')

    # change working dir
    old_cwd = os.getcwd()
    os.chdir(repo_root)

    try:
        # monkeypatch requests.head to return large Content-Length
        def fake_head(url, timeout=10):
            return DummyHead(headers={'Content-Length': '99999'})

        def fake_get(url, timeout=10):
            return DummyGet(content=b'x' * 10)

        monkeypatch.setattr(fetch_external_images, 'requests', types.SimpleNamespace(head=fake_head, get=fake_get))

        # max_size_bytes small (e.g., 5 bytes) -> should skip
        replacements = fetch_external_images.process_readme(max_size_bytes=5, dry_run=True)
        assert replacements == {}

        # now allow larger size, dry-run should produce replacement mapping
        replacements = fetch_external_images.process_readme(max_size_bytes=200000, dry_run=True)
        assert 'https://example.com/image.png' in replacements
    finally:
        os.chdir(old_cwd)