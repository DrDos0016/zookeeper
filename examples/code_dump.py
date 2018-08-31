# -*- coding: utf-8 -*-
import os
import sys
import zookeeper


def main():  # TODO: Comment this
    path = sys.argv[-1]
    filename = os.path.basename(path)

    print(path)
    zoo = zookeeper.Zookeeper(path)

    for board in zoo.boards:
        print("=" * 80)
        print(board.title)
        print("-" * 80)
        for stat in board.stats:
            if stat.oop_length:
                print(stat.oop)

    return True

if __name__ == "__main__":
    main()
