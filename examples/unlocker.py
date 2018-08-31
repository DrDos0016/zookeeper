# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from zookeeper import Zookeeper, World, Board, Flag


def main():
    # Check that at least one file was passed to the script
    if len(sys.argv) < 2:
        print("Run: python unlocker.py <file1> <file2> <etc>")
        print("Ex: python unlocker.py LOCK-LCK.ZZT LOCK-UNL.ZZT " +
              "LOCK-SPR.ZZT LOCK-SAV.ZZT")
        print("\nThis script will remove all locks (normal, super, save) " +
              "from the provided ZZT files.")
        sys.exit()

    # Iterate over the files provided
    for file_name in sys.argv[1:]:
        # Create a Zookeeper object
        zoo = Zookeeper()

        # Load the file
        zoo.load_file(file_name)

        # Parse the file's world information
        zoo.parse_world()

        # Parse the file's board information
        zoo.parse_boards()

        print("Loaded world:", zoo.meta.file_name)

        ########################################
        # Regular Lock
        ########################################
        # Check for a regular lock -- This lock is performed by having a flag
        # named SECRET set in the world header.
        print("Checking for regular lock... ", end="")
        locked = False
        new_flags = []

        for flag in zoo.world.flags:
            if flag.name.upper() == "SECRET":
                locked = True
                new_flags.append("")
            else:
                new_flags.append(flag.name)

        if locked:
            print("Found!")
            print("Removing lock... ", end="")
            # Erase the current flag list
            zoo.world.flags = []

            # Set flags matching the list generated earlier (identical to the
            # old list, but with SECRET removed)
            for x in range(0, 10):
                flag = Flag(new_flags[x])
                zoo.world.flags.append(flag)

            print("Complete!")

        else:
            print("No lock found.")

        ########################################
        # Super Lock
        ########################################
        # Check for a super lock -- This lock is performed by renaming boards
        # to hyperlinks.
        # The board's number is put in the name to make editing easier than
        # searching through a dozen !c;LOCKED FILE boards.
        print("Checking for super lock... ", end="")
        super_locked = False

        board_idx = 0
        for board in zoo.boards:
            if board.title[0] == "!" or board.title[0] == ":":
                if not super_locked:
                    super_locked = True
                    print("Found!")
                    print("Removing super lock...", end="")
                board.title = str(board_idx).zfill(3) +
                board.title.encode("utf-8").decode("utf-8") + "  " +
                board.title.split(";", 1)[-1]
            board_idx += 1

        if super_locked:
            print("Complete!")
        else:
            print("No super lock found.")

        ########################################
        # Save Lock
        ########################################
        # Check for a save lock -- This lock is performed by saving a game,
        # then renaming the file extension of the save to .ZZT.
        # If the save byte is set, simply set it back to 0 to mark the world
        # as a ZZT world and not a ZZT save.
        print("Checking for save lock... ", end="")
        save_locked = False

        if zoo.world.saved_game:
            save_locked = True
            print("Found!")
            print("Removing save lock... ", end="")
            zoo.world.saved_game = False

        if save_locked:
            print("Complete!")
        else:
            print("No save lock found.")

        # If any locks were found, the file needs to be saved
        if locked or super_locked or save_locked:
            print("World has been modified. Saving unlocked world... ", end="")
            zoo.save()
            print("Saved!")
        else:
            print("World is already unlocked. No changes made.")

        print("-"*40)

    print("\nAll worlds processed.")

if __name__ == "__main__":
    main()
