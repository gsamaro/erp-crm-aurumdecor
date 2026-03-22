from __future__ import annotations

import os
from pathlib import Path

from streamlit.runtime.scriptrunner import get_script_run_ctx


def resolve_page_path(page_filename: str, current_file: str) -> str:
    ctx = get_script_run_ctx()
    target = Path(current_file).resolve().parent / page_filename
    if ctx and getattr(ctx, "main_script_path", None):
        main_dir = Path(ctx.main_script_path).resolve().parent
        return os.path.relpath(target, start=main_dir)
    return page_filename
