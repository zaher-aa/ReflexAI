"""Security helpers focused on SQL query hardening and safe file operations."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence, Tuple, Union

logger = logging.getLogger(__name__)

SQL_COMMENT_PATTERN = re.compile(r"(--|#|/\*)")
IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PLACEHOLDER_PATTERN = re.compile(r":([A-Za-z_][A-Za-z0-9_]*)")
PYFORMAT_PATTERN = re.compile(r"%\(([^)]+)\)s")
TAUTOLOGY_PATTERN = re.compile(r"(=\s*\d+\s+OR\s+\1=\1)", re.IGNORECASE)


class SQLInjectionError(ValueError):
    """Raised when a potentially unsafe SQL construct is detected."""


def guard_against_sql_injection(query: str) -> None:
    """Validate a query string for obvious SQL injection indicators.

    The function enforces a single statement, forbids inline SQL comments
    and attempts to highlight suspicious tautologies that are commonly used
    during injection attempts.
    """

    if not query or not query.strip():
        raise SQLInjectionError("Empty SQL queries are not permitted.")

    stripped = query.strip()
    statements = [segment for segment in stripped.split(";") if segment.strip()]
    if len(statements) > 1:
        raise SQLInjectionError("Multiple SQL statements in a single query are not allowed.")

    if SQL_COMMENT_PATTERN.search(stripped):
        raise SQLInjectionError("Inline SQL comments are not allowed in dynamic queries.")

    if TAUTOLOGY_PATTERN.search(stripped):
        raise SQLInjectionError("Potential SQL tautology detected in query.")


def ensure_parameterized_query(query: str, parameters: Mapping[str, Any]) -> None:
    """Ensure a SQL query relies on parameter binding rather than string formatting."""

    guard_against_sql_injection(query)

    placeholders = set(PLACEHOLDER_PATTERN.findall(query))
    placeholders.update(PYFORMAT_PATTERN.findall(query))

    if not placeholders and parameters:
        raise SQLInjectionError("Parameters were supplied but no placeholders were found in the query.")

    missing_params = placeholders.difference(parameters.keys())
    if missing_params:
        raise SQLInjectionError(f"Missing parameters for placeholders: {', '.join(sorted(missing_params))}")

    for key, value in parameters.items():
        if isinstance(value, str) and SQL_COMMENT_PATTERN.search(value):
            raise SQLInjectionError(f"Parameter '{key}' contains SQL comment markers and was rejected.")


def sanitize_like_parameter(value: str) -> str:
    """Escape SQL LIKE wildcards in user supplied strings."""

    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def validate_sql_identifiers(identifiers: Sequence[str]) -> None:
    """Validate that user supplied identifiers follow safe naming rules."""

    for identifier in identifiers:
        if not IDENTIFIER_PATTERN.match(identifier):
            raise SQLInjectionError(f"Unsafe SQL identifier received: {identifier}")


def scrub_order_by_clause(order_by: Iterable[Tuple[str, str]]) -> Tuple[Tuple[str, str], ...]:
    """Whitelist order by clauses by validating identifiers and directions."""

    sanitized: list[Tuple[str, str]] = []
    for column, direction in order_by:
        validate_sql_identifiers([column])
        upper_direction = direction.upper()
        if upper_direction not in {"ASC", "DESC"}:
            raise SQLInjectionError(f"Invalid sorting direction for column {column}: {direction}")
        sanitized.append((column, upper_direction))
    return tuple(sanitized)


def ensure_within_directory(path: Union[str, Path], base_dir: Union[str, Path]) -> Path:
    """Ensure that a path stays within a trusted base directory."""

    candidate_path = Path(path).resolve()
    base_path = Path(base_dir).resolve()

    try:
        candidate_path.relative_to(base_path)
    except ValueError as exc:
        logger.debug("Rejected path outside of base directory: %s", candidate_path)
        raise ValueError("Path escapes the allowed directory") from exc

    return candidate_path