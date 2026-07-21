"""Bless the current row ids into the permanent published roster (reference/row-ids.txt).

MANUAL ONLY. No build or gate script may ever invoke this. Blessing a row id makes it a permanent
public identifier that inbound deep links (#/row/<id>) will point at from then on, so it has to be a
deliberate human act. build/assemble.py carries an inventory guard that FAILS the build on any id it
has not seen before, precisely so a new id cannot slip into permanence without someone running this.

Run:
  python build/update_row_ids.py            # dry run: report what would change, write nothing
  python build/update_row_ids.py --write    # rewrite reference/row-ids.txt to the current ids

Retiring a row: delete the row from its module AND remove its line here, in the same commit. The
#/row/<id> route then serves the not-found state for that id (which never gets reused for a new row).
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble import collect_row_ids, read_inventory, INVENTORY_PATH

HEADER = (
    "# Published row-id roster (PR-004). Every id here is a permanent public identifier that\n"
    "# deep links (#/row/<id>) resolve against; ids are never renamed once published.\n"
    "# Regenerated ONLY by a manual `python build/update_row_ids.py --write`, never by the build.\n"
)


def main():
    current = sorted(set(collect_row_ids()))
    published = read_inventory() if os.path.exists(INVENTORY_PATH) else []
    added = sorted(set(current) - set(published))
    removed = sorted(set(published) - set(current))

    print(f"{len(current)} row ids in the modules; {len(published)} in reference/row-ids.txt.")
    if added:
        print(f"  + {len(added)} to bless: " + ", ".join(added))
    if removed:
        print(f"  - {len(removed)} no longer present (retirement): " + ", ".join(removed))
    if not added and not removed:
        print("  roster already matches the modules; nothing to do.")

    if "--write" in sys.argv:
        with open(INVENTORY_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write(HEADER + "\n".join(current) + "\n")
        print(f"Wrote {INVENTORY_PATH} ({len(current)} ids).")
    elif added or removed:
        print("Dry run. Re-run with --write to update the roster.")


if __name__ == "__main__":
    main()
