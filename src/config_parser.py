from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from mazegen.grid import Coord


# ---------------------------------------------------------------------
# Config model
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class Config:
    width: int
    height: int
    entry: Coord
    exit: Coord
    perfect: bool
    seed: Optional[int]
    output: str


# ---------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------

def _parse_bool(value: str) -> bool:
    v = value.strip().lower()
    if v in {"true", "1", "yes", "y"}:
        return True
    if v in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean: {value}")


def _parse_int(value: str) -> int:
    return int(value.strip())


def _parse_coord(value: str) -> Coord:
    # Expected format: "x,y"
    parts = [p.strip() for p in value.split(",")]
    if len(parts) != 2:
        raise ValueError(f"Invalid coord (expected x,y): {value}")
    return (int(parts[0]), int(parts[1]))


# ---------------------------------------------------------------------
# File reader
# ---------------------------------------------------------------------

def read_config_file(path: str) -> dict[str, str]:
    data: dict[str, str] = {}

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(
                    f"Invalid config line (expected KEY=VALUE): {raw.rstrip()}"
                )

            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            data[key] = value

    return data


# ---------------------------------------------------------------------
# Public parser
# ---------------------------------------------------------------------

def parse_config(path: str) -> Config:
    raw = read_config_file(path)

    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "PERFECT", "OUTPUT_FILE"]
    missing = [k for k in required if k not in raw]
    if missing:
        raise ValueError(f"Missing config keys: {', '.join(missing)}")

    width = _parse_int(raw["WIDTH"])
    height = _parse_int(raw["HEIGHT"])
    entry = _parse_coord(raw["ENTRY"])
    exit_ = _parse_coord(raw["EXIT"])
    perfect = _parse_bool(raw["PERFECT"])
    output = raw["OUTPUT_FILE"]

    seed: Optional[int] = None
    if "SEED" in raw and raw["SEED"].strip() != "":
        seed = _parse_int(raw["SEED"])

    # Basic validations
    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be > 0")

    ex, ey = entry
    xx, xy = exit_

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError("ENTRY out of bounds")

    if not (0 <= xx < width and 0 <= xy < height):
        raise ValueError("EXIT out of bounds")

    if entry == exit_:
        raise ValueError("ENTRY and EXIT must be different")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        perfect=perfect,
        seed=seed,
        output=output,
    )
