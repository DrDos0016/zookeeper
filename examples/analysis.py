from zookeeper import Zookeeper, World, Board, Flag


def main():
    #path = input("ZZT file path:")
    path = "/mnt/ez/486/ZZT/201X/ZOMBINAT.ZZT"

    z = Zookeeper(path)

    for board in z.boards:
        print(board.title)
        for stat in board.stats:
            if stat.oop:
                code = stat.oop.split("\n")
                for line in code:
                    if line.startswith("#give score"):
                        print("\t",code[0])
                        print("\t\t", line)

if __name__ == "__main__":
    main()
