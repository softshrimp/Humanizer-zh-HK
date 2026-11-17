#!/usr/bin/env python3
"""Check Humanizer-zh-HK's package files without external dependencies."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_NAME = "humanizer-zh-hk"


def read_package_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(f"Cannot read {path.relative_to(ROOT)}: {error}")


SKILL_PATH = ROOT / "SKILL.md"
SKILL = read_package_file(SKILL_PATH)
README = read_package_file(ROOT / "README.md")
CHANGELOG = read_package_file(ROOT / "CHANGELOG.md")

try:
    PLUGIN = json.loads(read_package_file(ROOT / ".claude-plugin" / "plugin.json"))
except json.JSONDecodeError as error:
    raise SystemExit(f"Fix the JSON in .claude-plugin/plugin.json: {error}")

try:
    CURSOR_PLUGIN = json.loads(
        read_package_file(ROOT / ".cursor-plugin" / "plugin.json")
    )
except json.JSONDecodeError as error:
    raise SystemExit(f"Fix the JSON in .cursor-plugin/plugin.json: {error}")

try:
    PACKAGE_JSON = json.loads(read_package_file(ROOT / "package.json"))
except json.JSONDecodeError as error:
    raise SystemExit(f"Fix the JSON in package.json: {error}")


def require_match(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


yaml_metadata = require_match(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md must begin with YAML metadata",
).group(1)

skill_name = require_match(
    re.search(r"(?m)^name:\s*(\S+)\s*$", yaml_metadata),
    "Add name to SKILL.md YAML metadata",
).group(1)
if skill_name != EXPECTED_NAME:
    raise SystemExit(f"Set SKILL.md name to {EXPECTED_NAME}, got {skill_name!r}")

for unsupported_field in ("version:", "compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(unsupported_field)}", yaml_metadata):
        raise SystemExit(f"Remove unsupported YAML field: {unsupported_field[:-1]}")

skill_version = require_match(
    re.search(
        r'(?m)^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', yaml_metadata
    ),
    "Add metadata.version to SKILL.md as a three-part version",
).group(1)
changelog_version = require_match(
    re.search(r"(?m)^## ([0-9]+\.[0-9]+\.[0-9]+)$", CHANGELOG),
    "Add a version heading to CHANGELOG.md",
).group(1)

package_versions = {
    skill_version,
    changelog_version,
    str(PLUGIN.get("version", "")),
    str(CURSOR_PLUGIN.get("version", "")),
}
if len(package_versions) != 1:
    raise SystemExit(
        f"Use one package version in all files: {sorted(package_versions)}"
    )

skill_files = {path.relative_to(ROOT) for path in ROOT.rglob("SKILL.md")}
if SKILL_PATH.is_symlink() or skill_files != {Path("SKILL.md")}:
    raise SystemExit("Keep one regular SKILL.md at the repo root")
if PLUGIN.get("name") != EXPECTED_NAME:
    raise SystemExit(f"Set the Claude plugin name to {EXPECTED_NAME}")
if PLUGIN.get("skills") != ["./"]:
    raise SystemExit("Point the Claude plugin skill loader at the repo root")
if CURSOR_PLUGIN.get("name") != EXPECTED_NAME:
    raise SystemExit(f"Set the Cursor plugin name to {EXPECTED_NAME}")
if "skills" in CURSOR_PLUGIN:
    raise SystemExit("Omit skills from the Cursor plugin so it loads the root SKILL.md")
if PACKAGE_JSON.get("name") != EXPECTED_NAME:
    raise SystemExit(f"Set package.json name to {EXPECTED_NAME}")
if "version" in PACKAGE_JSON:
    raise SystemExit("Omit version from package.json for pi git installation")
if PACKAGE_JSON.get("pi", {}).get("skills") != ["./"]:
    raise SystemExit("Point package.json pi.skills at ['./']")

skill_description = "".join(
    line.strip()
    for line in require_match(
        re.search(r"(?m)^description: \|\n((?:  .*\n)+)", yaml_metadata + "\n"),
        "Write the SKILL.md description as an indented block",
    )
    .group(1)
    .splitlines()
)
MARKETPLACE = json.loads(
    read_package_file(ROOT / ".claude-plugin" / "marketplace.json")
)
package_descriptions = {
    str(PLUGIN.get("description", "")),
    str(CURSOR_PLUGIN.get("description", "")),
    str(PACKAGE_JSON.get("description", "")),
    *(
        str(plugin.get("description", ""))
        for plugin in MARKETPLACE.get("plugins", [])
    ),
}
if len(package_descriptions) != 1 or not skill_description.startswith(
    next(iter(package_descriptions))
):
    raise SystemExit(
        "Use the first sentence of the SKILL.md description in every plugin manifest: "
        f"{sorted(package_descriptions)}"
    )

skill_patterns = dict(
    (int(number), name)
    for number, name in re.findall(r"(?m)^### ([0-9]+)\. (.+)$", SKILL)
)
pattern_numbers = list(skill_patterns)
pattern_count = len(pattern_numbers)
if pattern_count == 0 or pattern_numbers != list(range(1, pattern_count + 1)):
    raise SystemExit(
        f"Number SKILL.md patterns from 1 upward without gaps: {pattern_numbers}"
    )

readme_patterns = dict(
    (int(number), name)
    for number, name in re.findall(r"(?m)^\| ([0-9]+) \| \*\*(.+?)\*\*", README)
)
if sorted(readme_patterns) != pattern_numbers:
    raise SystemExit(
        f"List patterns 1 through {pattern_count} once each in the README tables: {sorted(readme_patterns)}"
    )
renamed = [
    f"{number}: {readme_patterns[number]!r} should be {name!r}"
    for number, name in skill_patterns.items()
    if readme_patterns[number] != name
]
if renamed:
    raise SystemExit(
        "Match the README pattern names to SKILL.md: " + "; ".join(renamed)
    )
if f"## {pattern_count} 種 AI 寫作痕跡" not in README:
    raise SystemExit(
        f"Title the README pattern section '{pattern_count} 種 AI 寫作痕跡'"
    )

skill_references = sorted({int(number) for number in re.findall(r"§([0-9]+)", SKILL)})
missing_patterns = [
    number for number in skill_references if not 1 <= number <= pattern_count
]
if missing_patterns:
    raise SystemExit(
        f"Point every SKILL.md section reference at a pattern from 1 to "
        f"{pattern_count}: {missing_patterns}"
    )

skill_words = len(SKILL.split())
skill_chars = len(SKILL)
if skill_words > 5500:
    raise SystemExit(f"Keep SKILL.md at 5,500 words or fewer; it has {skill_words}")
if skill_chars > 16000:
    raise SystemExit(
        f"Keep SKILL.md at 16,000 characters or fewer; it has {skill_chars}"
    )

FORBIDDEN_IN_AFTER = re.compile(
    r"[“”‘’—–]|——| -- |軟體|硬體|網路|同比|環比|賦能|抓手|顆粒度|閉環|賽道|默認|服務器|視頻|出租車|計程車"
)
for doc_name, content in (("SKILL.md", SKILL), ("README.md", README)):
    for index, block in enumerate(
        re.findall(r"\*\*改寫後[^*]*\*\*\n((?:>.*\n?)+)", content), start=1
    ):
        bad = FORBIDDEN_IN_AFTER.search(block)
        if bad:
            raise SystemExit(
                f"{doc_name} '改寫後' example #{index} contains forbidden token {bad.group(0)!r}"
            )

print(
    f"Humanizer-zh-HK package v{skill_version} is valid "
    f"({pattern_count} patterns, {skill_chars} chars)"
)
