import argparse
import re
import zookeeper


def main():  # TODO: Comment this
    # Parse config
    parser = argparse.ArgumentParser(description="ZZT-OOP Code Search")
    parser.add_argument("-i", "--ignore-case",
                        help="ignore the case of letters in the expression",
                        action="store_true")
    parser.add_argument("-l", "--objects-with-matches",
                        help="print the name of a matching object rather than \
                        any matched lines",
                        action="store_true")
    parser.add_argument("file")
    parser.add_argument("expression")

    args = parser.parse_args()

    if args.ignore_case:
        regex = re.compile(args.expression, re.I)
    else:
        regex = re.compile(args.expression)

    zoo = zookeeper.Zookeeper(args.file)

    row = "+-------+-------------------------+" + ("-" * 44) + "+"
    print(row)
    if args.objects_with_matches:
        print("| COORD | BOARD                   | ELEMENT" + (" " * 36) + "|")
    else:
        print("| COORD | BOARD                   | LINE" + (" " * 39) + "|")
    print(row)
    for board in zoo.boards:
        known_matches = []
        for stat in board.stats:
            if stat.oop_length:
                for line in stat.oop.split("\n"):
                    if re.search(regex, line) is not None:
                        if (args.objects_with_matches and
                                (stat.x, stat.y) in known_matches):
                            continue

                        x = str(stat.x).zfill(2)
                        y = str(stat.y).zfill(2)
                        title = (board.title + (" " * 40))[:23]
                        line = (line + (" " * 42))[:42]

                        if args.objects_with_matches:
                            known_matches.append((stat.x, stat.y))
                            if stat.oop[0][0] == "@":
                                name = stat.oop[:stat.oop.find("\n")]
                            else:
                                name = board.get_element(
                                    (stat.x, stat.y)
                                ).name.title()
                            name = (name + (" " * 42))[:42]
                            print("|", "{},{}".format(x, y),
                                  "|", title, "|", name, "|")
                        else:
                            print("|", "{},{}".format(x, y),
                                  "|", title, "|", line, "|")
    print(row)
    return True

if __name__ == "__main__":
    main()
