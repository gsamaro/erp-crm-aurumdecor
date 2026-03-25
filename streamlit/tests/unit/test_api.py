import os
import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[2]))

from components.api import get_api_base_url  # noqa: E402


def test_get_api_base_url_prefers_secrets(monkeypatch):
    monkeypatch.setattr(st, "secrets", {"API_BASE_URL": "https://api.example.com"})
    monkeypatch.setenv("API_BASE_URL", "https://env.example.com")

    assert get_api_base_url() == "https://api.example.com"


def test_get_api_base_url_falls_back_to_env(monkeypatch):
    monkeypatch.setattr(st, "secrets", {})
    monkeypatch.setenv("API_BASE_URL", "https://env.example.com")

    assert get_api_base_url() == "https://env.example.com"


def test_get_api_base_url_defaults(monkeypatch):
    monkeypatch.setattr(st, "secrets", {})
    monkeypatch.delenv("API_BASE_URL", raising=False)

    assert get_api_base_url() == "http://localhost:8000"
