# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from zookeeper import Zookeeper, World, Board


def main():
    # Check that at least one file was passed to the script
    if len(sys.argv) < 2:
        print("Run: python undark.py <file1> <file2> <etc>")
        print("Ex: python undark.py UNDARK.ZZT")
        print("\nThis script will set all boards from the provided ZZT " +
              "files to not be dark.")
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

        # Remove darkness from any boards where the room is dark.
        modified = False
        for board in zoo.boards:
            if board.is_dark:
                if not modified:
                    print("Dark board found. Let there be light!")
                modified = True
                board.is_dark = False

        # If any dark rooms were found, the file needs to be saved
        if modified:
            print("World has been modified. Saving world... ", end="")
            zoo.save()
            print("Saved!")
        else:
            print("World is already lit. No changes made.")

        print("-"*40)

    print("\nAll worlds processed.")

if __name__ == "__main__":
    main()
