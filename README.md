# Zookeeper

[![license](https://img.shields.io/badge/license-GPL--3.0%2B-brightgreen.svg)](https://github.com/DrDos0016/zookeeper/blob/master/LICENSE)

Zookeeper is a Python library for parsing, analyzing, and modifying ZZT worlds.

The goal is to have an easy to use library which can provide generic
functionality for extracting data with straightforward Python scripts.

### Features
- Editing of World information (health, ammo, starting board, set flags, etc.)
- Editing of Board information (connecting boards, dark rooms, etc.)
- Editing of Elements and their stats (color, characters, ZZT-OOP code)
- Support for ZZT save file editing
- Export boards to ZZT compatible BRD files
- Create renders of ZZT boards
- Create renders of ZZT scrolls/object code
- Convert Font Mania .com files to PNG charsets
- Documentation and example scripts to get you started

### Planned Features
- Super ZZT file parsing
- Windows binaries of scripts to be used as tools for non-developers

### Example Scripts
Removing the "board is dark" flag from all boards in Caves of ZZT:

```python
import zookeeper

zoo = zookeeper.Zookeeper()
zoo.load_file("CAVES.ZZT")
zoo.parse_world()
zoo.parse_boards()

for board in zoo.boards:
    if board.is_dark:
        board.is_dark = False
zoo.save("LITCAVES.ZZT")
```

List the code of all objects on every board in Town of ZZT:

```python
import zookeeper

# Load a file, then parse its world, boards, and elements in one line.
zoo = zookeeper.Zookeeper("TOWN.ZZT")

for board in zoo.boards:
    print("=" * 80)
    print(board.title)
    print("-" * 80)
    for stat in board.stat_data:
        if stat.oop_length:
            print(stat.oop)
```

### Requirements
- Python3
- Optional install of Pillow (currently not so optional)
