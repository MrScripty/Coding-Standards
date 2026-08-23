# Standards Engine

`tools/standards_engine/` is the typed composition facade for standards
navigation and read-only analysis. Callers use canonical IDs and immutable
snapshot handles; repository paths, metadata layouts, graph declarations, and
source locators remain internal unless explicitly inspected.

Current operations provide snapshot-bound `read`, `related`, and `inspect`.
Router-owned `route` and change-impact analysis remain later A1 slices.

Run tests:

```bash
python3 -m unittest discover -s tools/standards_engine/tests
```
