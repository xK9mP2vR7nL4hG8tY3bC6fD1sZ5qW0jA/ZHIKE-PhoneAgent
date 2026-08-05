"""Export ZHIKE trace span JSONL to OTLP-compatible JSONL."""

from __future__ import annotations

import argparse
from pathlib import Path

from zhike_phoneagent.trace_export import export_otlp_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export ZHIKE trace span JSONL to OTLP-compatible JSONL."
    )
    parser.add_argument("trace_file", type=Path, help="Input ZHIKE trace JSONL file")
    parser.add_argument("output_file", type=Path, help="Output OTLP JSONL file")
    parser.add_argument("--trace-id", default=None, help="Only export one trace id")
    args = parser.parse_args()

    count = export_otlp_jsonl(
        args.trace_file,
        args.output_file,
        trace_id=args.trace_id,
    )
    print(f"Exported {count} span record(s) to {args.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
