"""Package entry: ``python -m magicsquare`` launches the GUI."""

from __future__ import annotations

from magicsquare.boundary.gui.app import main

if __name__ == "__main__":
    raise SystemExit(main())
