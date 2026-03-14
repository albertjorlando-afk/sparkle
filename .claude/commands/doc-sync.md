Perform a deep documentation and diagram sync for the sparkle project.

## Steps

1. **Read all source files** to understand current state:
   - `src/sparkle/models.py` — data model fields, types, validation
   - `src/sparkle/graph.py` — GraphStore public methods and traversal logic
   - `src/sparkle/cli.py` — all CLI subcommands and arguments
   - `src/sparkle/templates.py` — branch template definitions
   - `src/sparkle/bootstrap.py` — bootstrap seed structure
   - `tests/test_cli.py` — what's tested

2. **Audit the README.md diagrams** against the code:
   - **Class diagram**: verify every public field and method on Node, Edge, GraphStore, and BranchTemplate matches the code. Add missing members, remove stale ones.
   - **Sequence diagram**: verify the add-branch flow matches the actual call sequence in `cli.py`.
   - **State diagram**: verify the status transitions match `NodeStatus` in `models.py`.

3. **Audit README.md prose sections**:
   - "What It Does" — matches implemented features
   - "CLI" — all subcommands documented with correct examples
   - "Source layout" — all files listed
   - "Testing" — coverage list matches actual test methods
   - "Current Limits" — nothing listed that's actually implemented
   - "Next" — nothing listed that's already done

4. **Audit docs/prd.md**:
   - "MVP status" — matches what's actually built
   - "Next usability focus" — only lists unbuilt work

5. **Audit docs/roadmap.md**:
   - "Completed" — includes all shipped work
   - Phase sections — only list unbuilt items

6. **Make all fixes** to align docs with code. Do not change code — only change documentation files.

7. **Run tests** to confirm nothing is broken.

8. **Commit** with message: "Sync docs and diagrams with current project state"
