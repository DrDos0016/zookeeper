import zookeeper
import sys

# Usage: python3 join.py WORLD1.ZZT WORLD2.ZZT (...) JOINED.ZZT
def main():
    worldMain = zookeeper.Zookeeper(sys.argv[1])

    for i in range(2, len(sys.argv) - 1):
        worldSub = zookeeper.Zookeeper(sys.argv[i])
        boardOffsetMain = worldMain.world.total_boards
        for idx in range(0, worldSub.world.total_boards):
            boardSub: zookeeper.Board = worldSub.boards[idx]
            # transpose board IDs
            if boardSub.board_north > 0:
                boardSub.board_north += boardOffsetMain
            if boardSub.board_south > 0:
                boardSub.board_south += boardOffsetMain
            if boardSub.board_west > 0:
                boardSub.board_west += boardOffsetMain
            if boardSub.board_east > 0:
                boardSub.board_east += boardOffsetMain
            for statIdx in range(0, boardSub.stat_count):
                stat: zookeeper.Stat = boardSub.stats[statIdx]
                element: zookeeper.Element = boardSub.elements[(stat.x - 1 + ((stat.y - 1) * 60))]
                # Passage
                if element.id == 11:
                    stat.param3 = stat.param3 + boardOffsetMain
            # append
            worldMain.boards.append(boardSub)
        worldMain.world._total_boards += worldSub.world._total_boards

    worldMain.save(sys.argv[-1])

if __name__ == "__main__":
    main()




