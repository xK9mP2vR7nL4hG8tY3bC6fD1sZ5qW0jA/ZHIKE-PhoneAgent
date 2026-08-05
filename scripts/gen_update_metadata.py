#!/usr/bin/env python3
"""
Generate electron-updater update metadata files from built Electron artifacts.

electron-updater's GitHub provider requires ``latest.yml`` (Windows),
``latest-mac.yml`` (macOS) and ``latest-linux.yml`` (Linux) to be present as
release assets.  Because we build with ``publish: null`` / ``--publish never``
(to avoid Windows large-binary upload timeouts on CI) electron-builder does
NOT emit these files, so we generate them here and they are uploaded by the
release workflow via ``gh release upload``.

The script scans ``electron/dist`` for the installable artifacts:

* Windows  -> ``*Setup-*.exe`` (安装版) + 便携 exe -> ``latest.yml``
* macOS    -> ``*.dmg`` (both arches)     -> ``latest-mac.yml``
* Linux    -> ``*.AppImage``              -> ``latest-linux.yml``

Windows 同时纳入便携版 exe（命名形如 ``ZHIKE-PhoneAgent-<version>-<arch>.exe``，
不含 "Setup"），否则便携版自动更新会误拉取 NSIS 安装包而无法原地替换。

For every artifact it computes the SHA-512 (base64) and the byte size, and
attaches ``blockMapSize`` when a matching ``.blockmap`` file exists (enables
differential updates).

Usage:
    uv run python scripts/gen_update_metadata.py [DIST_DIR]
"""

import base64
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha512_b64(path: Path) -> str:
    """Return the base64-encoded SHA-512 of a file (streamed)."""
    h = hashlib.sha512()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return base64.b64encode(h.digest()).decode("ascii")


def file_entry(name: str, dist: Path) -> dict:
    """Build one electron-updater files[] entry for ``name``."""
    artifact = dist / name
    entry = {
        "url": name,
        "sha512": sha512_b64(artifact),
        "size": artifact.stat().st_size,
    }
    blockmap = dist / f"{name}.blockmap"
    if blockmap.exists():
        entry["blockMapSize"] = blockmap.stat().st_size
    return entry


def write_yaml(path: Path, version: str, files: list[dict], release_date: str) -> None:
    """Write an electron-updater metadata file in the exact expected format."""
    lines = [f"version: {version}", "files:"]
    for f in files:
        lines.append(f"  - url: {f['url']}")
        lines.append(f"    sha512: {f['sha512']}")
        lines.append(f"    size: {f['size']}")
        if "blockMapSize" in f:
            lines.append(f"    blockMapSize: {f['blockMapSize']}")
    # Top-level path/sha512 point at the primary update target (first file).
    lines.append(f"path: {files[0]['url']}")
    lines.append(f"sha512: {files[0]['sha512']}")
    # Quoted ISO-8601 with milliseconds; electron-updater expects this shape.
    lines.append(f"releaseDate: '{release_date}'")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def derive_version(dist: Path) -> str:
    """Best-effort version extraction from an artifact file name."""
    for pattern in ("*Setup-*.exe", "*.dmg", "*.AppImage", "*.tar.gz"):
        for p in sorted(dist.glob(pattern)):
            if p.name.endswith(".blockmap"):
                continue
            for token in p.stem.split("-"):
                if token.count(".") == 2:
                    return token
    return "0.0.0"


def main() -> int:
    dist = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("electron/dist")
    if not dist.is_dir():
        print(f"ERROR: dist directory not found: {dist}", file=sys.stderr)
        return 1

    setup = sorted(p.name for p in dist.glob("*Setup-*.exe"))
    # 便携版 exe（命名形如 ZHIKE-PhoneAgent-<version>-<arch>.exe，不含 "Setup"）
    portable = sorted(
        p.name
        for p in dist.glob("*.exe")
        if not p.name.endswith(".blockmap") and "Setup" not in p.name
    )
    windows = setup + portable
    dmg = sorted(p.name for p in dist.glob("*.dmg") if not p.name.endswith(".blockmap"))
    appimage = sorted(p.name for p in dist.glob("*.AppImage"))

    version = derive_version(dist)
    release_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + "000Z"

    wrote = 0
    if windows:
        files = [file_entry(n, dist) for n in windows]
        write_yaml(dist / "latest.yml", version, files, release_date)
        print(f"Wrote latest.yml (windows, {len(files)} file(s), v{version})")
        wrote += 1
    if dmg:
        files = [file_entry(n, dist) for n in dmg]
        write_yaml(dist / "latest-mac.yml", version, files, release_date)
        print(f"Wrote latest-mac.yml (macos, {len(files)} file(s), v{version})")
        wrote += 1
    if appimage:
        files = [file_entry(n, dist) for n in appimage]
        write_yaml(dist / "latest-linux.yml", version, files, release_date)
        print(f"Wrote latest-linux.yml (linux, {len(files)} file(s), v{version})")
        wrote += 1

    if wrote == 0:
        print("WARNING: no installable artifacts found; nothing written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
