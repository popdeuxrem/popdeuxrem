import json
import types

import requests

from scripts import discovery


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        return None

    def json(self):
        return self._data


def test_fetch_github_metrics_aliases(monkeypatch):
    sample_repo = {
        'name': 'example',
        'description': 'Example repo',
        'stargazers_count': 5,
        'forks_count': 2,
        'language': 'Python',
        'html_url': 'https://github.com/example',
        'fork': False,
        'updated_at': '2026-01-01T00:00:00Z',
        'open_issues_count': 1,
    }

    def fake_get(url, headers=None, timeout=10):
        return DummyResponse([sample_repo])

    monkeypatch.setattr(discovery, 'requests', types.SimpleNamespace(get=fake_get))

    vessels = discovery.fetch_github_metrics('whatever')
    assert len(vessels) == 1
    v = vessels[0]
    # Original short keys
    assert 'stars' in v and v['stars'] == 5
    assert 'forks' in v and v['forks'] == 2
    assert 'desc' in v and 'Example' in v['desc']
    # Canonical API keys also present
    assert 'stargazers_count' in v and v['stargazers_count'] == 5
    assert 'forks_count' in v and v['forks_count'] == 2
    assert 'description' in v and 'Example' in v['description']
    assert 'html_url' in v and v['html_url'] == 'https://github.com/example'