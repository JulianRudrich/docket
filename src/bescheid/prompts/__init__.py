"""Versioned prompts. Never edit a released prompt; add a new version instead,
so every evaluation result can be traced back to the exact prompt it used."""

from importlib.resources import files


def load_prompt(version: str) -> str:
    return files(__package__).joinpath(f"{version}.md").read_text(encoding="utf-8")
