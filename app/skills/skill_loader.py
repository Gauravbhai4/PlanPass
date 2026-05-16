"""Load BBMP skill markdown files.

Skills are structured reference files that teach the LLM about Karnataka building law.
"""
from pathlib import Path
from typing import List

SKILLS_DIR = Path(__file__).parent / "files"


def list_available_skills() -> List[str]:
    """Return names of all available skill files (without .md extension)."""
    return sorted(p.stem for p in SKILLS_DIR.glob("*.md"))


def load_skill(name: str) -> str:
    """Load a single skill markdown file by name (without extension)."""
    skill_path = SKILLS_DIR / f"{name}.md"
    if not skill_path.exists():
        return ""
    return skill_path.read_text(encoding="utf-8")


def load_skills(names: List[str]) -> str:
    """Load specific skills by name, concatenated with separators."""
    parts = []
    for name in names:
        content = load_skill(name)
        if content:
            parts.append(
                f"========================================\n"
                f"SKILL: {name}\n"
                f"========================================\n\n"
                f"{content}\n"
            )
    return "\n".join(parts)


def load_all_skills() -> str:
    """Load every skill file in the directory."""
    return load_skills(list_available_skills())
