# Zookeeper Documentation

## Contents:

- A
- B
- C
- D

## Introduction
Zookeeper is a library that allows easily accessing and modifying data in ZZT
files via Python rather than having to hex edit or use an external editor to
extract information.

## Module Structure
Zookeeper() ->

## Classes

### Zookeeper
```Python
class zookeeper.zookeeper.Zookeeper(file=None, charset="auto")
```

Creates a Zookeeper instance.

| Parameter | Explanation                                                      |
| --------- | ---------------------------------------------------------------- |
| file      | Full path to a ZZT file. If provided, it is automatically parsed |
| charset   | Full path to a PNG charset file. This may be ```None``` to not load a charset. "auto" will load Zookeeper's included Code Page 437 charset. |

#### Attributes
* fh - File handle for the currently in use
* meta - `Meta()` object containing information about the loaded file
* world - `World()` object. Uninitialized until world is parsed.
* boards - A list for holding `Board()` objects. Empty until boards are parsed.
* invisible_mode - `(int)` Determines how to display invisible walls. (0: empty | 1: editor style | 2: touched)
* title_screen_monitor - `(bool)` Whether or not to replace the first stat element on the title screen (usually a player) with a monitor element.
* line_break - `(str)` Character to use as a line break for ZZT-OOP code. Internally ZZT uses a carriage return. By default Zookeeper converts this to a
standard new line character for easier display of text.

#### Return Type
`Zookeeper`

#### Returns
A `Zookeeper` object.

#### Functions

```Python
export_font(file, new_filename=None):
```

Opens Font Mania .com font file and exports a PNG charset of it.

| Parameter    | Explanation                         |
| ------------ | ----------------------------------- |
| file         | Full path to a Font Mania .com file |
| new_filename | Name to save the exported PNG with. Defaults to the name of the .com file|

#### Return Type
`bool`

#### Returns

`True` on successfully saving the PNG charset.

----

```Python
load_file(file):
```

Opens file handle to eventually be parsed.

| Parameter | Explanation              |
| --------- | ------------------------ |
| file      | Full path to a ZZT file. |

#### Return Type
`bool`

#### Returns

`True` on successfully opening the file.

----
```Python
parse_boards():
```

Parses all boards in a file.

#### Return Type
`bool`

#### Returns

`True` on successfully parsing all board information.

----
```Python
parse_elements():
```

Parses all elements on every board in the file.

#### Return Type
`bool`

#### Returns

`True` on successfully parsing all elements.

----
```Python
parse_file():
```

Parses a file's world, board, and element information. Called automatically
when passing a filepath to a ```Zookeeper()``` constructor.

#### Return Type
`bool`

#### Returns

`True` on successfully parsing the complete file.

----
```Python
parse_world():
```

Parses a file's world header.

#### Return Type
`bool`

#### Returns

`True` on successfully parsing the file's world information.

----
```Python
save(filename=None):
```

Writes the current state of the worlds/boards/elements to a ZZT file.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| filename      | Full path to a ZZT file to write. Overwrites loaded file if None. |

#### Return Type
`bool`

#### Returns

`True` on successfully writing the file.

----
### Meta
```Python
class zookeeper.zookeeper.Meta()
```

Creates a Meta instance. This is created automatically when loading a file with a `Zookeeper()` instance.


#### Attributes
* file_name - The name of the currently loaded file.
* full_path - The full path to the currently loaded file.

#### Return Type
`Meta`

#### Returns
A `Meta` object.

----
### World
```Python
class zookeeper.zookeeper.World()
```

Creates a World instance.

#### Attributes
* identifier - Identifying bytes to make ZZT recognize the file is a ZZT world. Defaults to `zookeeper.constants.ZZT_IDENTIFIER`
* engine - Human readable identifier. Defaults to ``"ZZT"``
* non_title_boards - Number of boards in the file excluding the title screen. Defaults to `0`. Matches board count used in ZZT file format.
* total_boards - Number of boards in the file including the title screen. Defaults to  `1`.
* ammo - Starting ammo. Defaults to `0`.
* gems - Starting gems. Defaults to `0`.
* keys - Dictionary of keys the player has in the world. Defaults to ```{"Blue": False, "Green": False, "Cyan": False, "Red": False, "Purple": False, "Yellow": False, "White":False}```
*  health - Starting health. Defaults to `100`.
*  current_board - Board displayed when the file is opened in ZZT. Defaults to `0`.
*  torches - Starting torches. Defaults to `0`.
*  torch_cycles - Remaining cycles in lit torch. Defaults to `0`.
*  energizer_cycles - Remaining cycles in energizer. Defaults to `0`.
*  unused - Unused signed 16-bit integer. No purpose. Defaults to `0`.
*  score - Starting score. Defaults to `0`.
*  world_name - Name of world. This is normally the file name without any extension. Defaults to `"NEWWORLD"`.
*  flags - Tuple of ten `Flag()` objects. Defaults to ten unset flags.
*  time_passed - Number of seconds elapsed on the current board if it has a time limit. Defaults to `0`.
*  time_passed_ticks - Counts sub-seconds passed for time limited boards. Defaults to `0`.
*  saved_game - Whether the world is considered a saved game or not. Defaults to `False`.

#### Return Type
`World`

#### Returns
A `World` object.

#### Functions

```Python
encode():
```

Takes existing world information and encodes it according to ZZT's world format.

#### Return Type
`bytearray`

#### Returns

A bytearray representing the first 512 bytes of a ZZT file.

----
### Board
```Python
class zookeeper.zookeeper.Board(populate=False)
```

Creates a Board instance.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| populate      | If `True`, initalizes the Board.elements list with 1500 Element() objects. |

#### Return Type
`Board`

#### Returns

A `Board` object.

#### Attributes
* start_address - The offset in the file in bytes where this board's information begins. Defaults to `None`.
* element_address - The offset in the file in byes where this board's element information begins. Defaults to `None`.
* stats_address - The offset in the file in bytes where this board's stat information begins. Defaults to `None`.
* size - The size of the board in bytes. Defaults to `0`. This size does not include the two bytes for this value.
* title_length - The length of the board's title. Defaults to `8`.
* title - The board's title. Defaults to `Untitled`.
* elements - A list for containing `Element()` objects for every tile on the board. Defaults to `[]` unless told to populate.
* rle_elements - A list containing run-length encoded lists of `[quantity, element, color]` describing all the elements on the board. Defaults to `[]`.
* can_fire - The number of shots that can be fired on this board. Defaults to `255`.
* is_dark - Whether or not the board is dark. Defaults to `False`.
* board_north - The board index for the board to the north. Defaults to `0` which represents no connection.
* board_south - The board index for the board to the south. Defaults to `0` which represents no connection.
* board_west - The board index for the board to the west. Defaults to `0` which represents no connection.
* board_east - The board index for the board to the east. Defaults to `0` which represents no connection.
* zap - Whether or not the player is returned to the enter coordinates when damaged. Defaults to `False`.
* message - A bytestring representing the message currently being displayed across the bottom row of the room. Defaults to `b""`.
* enter_x - X-coordinate to return the player to when damage is taken. Ranges from 1-60. Defaults to `1`.
* enter_y - Y-coordinate to return the player to when damage is taken. Ranges from 1-25. Defaults to `1`.
* time_limit - The amount of time that can pass on the board before damage the player. Defaults to `0` representing an infinite time limit.
* stat_count - A count of the number of elements on the board which have stats, excluding the player. Defaults to `0`.
* stat_data - A list of `Stat()` objects. Defaults to `[]`.

#### Functions

```Python
screenshot(filename)
```

Saves a PNG screenshot of the current board.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| filename      | Full path to a PNG file to write. |

#### Return Type
`None`

#### Returns

None

```Python
scroll(text, filename, type="code", expand=True, line=0, custom_name=None)
```

**This function is not fully implemented**
Saves a PNG screenshot of the provided text/ZZT-OOP code mimicing ZZT's own
text displays.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| filename      | Full path to a PNG file to write. |
| type          | "scroll", "object", "code" determines whether the provided text is rendered as a scroll would display it, an object would display it, or the ZZT editor would display it |
| expand        | Allow the PNG to grow in height beyond the size of a standard text display. |
| line          | The first line to begin writing text to the window from. Unused when expand is True. |
| custom_name   | Force the text display to display the provided name in its header regardless of its type |

#### Return Type
`None`

#### Returns

None

```Python
scroll(text, filename, type="code", expand=True, line=0, custom_name=None)
```

**This function is not fully implemented**
Saves a PNG screenshot of the provided text/ZZT-OOP code mimicing ZZT's own
text displays.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| filename      | Full path to a PNG file to write. |
| type          | "scroll", "object", "code" determines whether the provided text is rendered as a scroll would display it, an object would display it, or the ZZT editor would display it |
| expand        | Allow the PNG to grow in height beyond the size of a standard text display. |
| line          | The first line to begin writing text to the window from. Unused when expand is True. |
| custom_name   | Force the text display to display the provided name in its header regardless of its type |

#### Return Type
`None`

#### Returns

None

```Python
get_element(query):
```

Returns an element located at the provided coordinates or tile index on the
board.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| query         | *tuple* the (X, Y) coordinates of the element to fetch. Ranges from (1, 1) to (60, 25) |
| query         | *integer* the tile index of the element to fetch. Ranges from 0 to 1499 |

#### Return Type
`Element`

#### Returns

An `Element` object.

```Python
export(filename):
```

Saves the board as a valid ZZT BRD file.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| filename      | Full path to a BRD file to write |

#### Return Type
`None`

#### Returns

None

### Element
```Python
class zookeeper.zookeeper.Element(id, color=15, stat_idx=None, tile=None, character=None):
```

Creates an Element instance.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| id            | The ID of the element. (Ex: 0 for Empty, 4 for Player) |
| color         | The numeric foreground/background color of the element. [EGA Color Palette](https://en.wikipedia.org/wiki/Enhanced_Graphics_Adapter#Color_palette) |
| stat_idx      | The index of the stat list this element references for its stats. |
| tile          | The tile index where on the board this element is located. |
| character     | The numeric value of the character this element represents itself with |

#### Return Type
`Element`

#### Returns

An `Element` object.

#### Attributes

* id - The number used by ZZT to dictate what an element is. See (TODO: elements.py)
* tile - The tile index where on the board this element is located.
* name - The name of the element
* oop_name - The name of the element as referenced in ZZT-OOP if available
* character - The numeric value of the character used to represent this element. If unspecified, uses the default character based on the element's ID.
* color_id - The numeric foreground and background color of the element.
* foreground - The numeric foreground color of the element.
* background - The numeric background color of the element.
* foreground_name - The human-readable name of the element's foreground color.
* background_name - The human-readable name of the element's background color.
* color_name - The human-readable name of the element's color.
* stat_idx - The index of the stat list the element references for its stats.
* stat - The `Stat` object this element references.

### Stat

```Python
class zookeeper.zookeeper.Stat(idx):
```

Creates a Stat instance.

| Parameter     | Explanation              |
| ------------- | ------------------------ |
| idx            | The original stat index of the stat. |

#### Return Type
`Stat`

#### Returns

A `Stat` object.

#### Attributes

* idx - The stat's index number.
* x - The X-Coordinate of the stat.
* y - The Y-Coordinate of the stat.
* tile - The tile index number of the stat.
* x_step - The stat's X-Step
* y_step - The stat's y-Step
* cycle - The stat's cycle
* param1 - The stat's first parameter
* param2 - The stat's second parameter
* param3 - The stat's third parameter
* follower - The stat index of the next element of a centipede
* leader - The stat index of the previous element of a centipede
* under_id - The element ID for the tile beneath this stat's element.
* under_color - The color ID for the tile beneath this stat's element.
* pointer - Unused outside of ZZT's runtime.
* current_instruction = The current byte of ZZT-OOP being executed.
* bound_idx - The stat index to reference ZZT-OOP from for bound objects.
* oop_length - The length in bytes of ZZT-OOP.
* padding - Padding unused within ZZT
* oop - The stat's ZZT-OOP.

### Flag
