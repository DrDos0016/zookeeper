from zookeeper import Zookeeper, World, Board, Flag
import argparse

# built from analysis.py initally, with cues taken from code_search.py spits out world's board sizes,
# size of code on each board, and % of each board that is ZZT-OOP.
#
# syntax: python sizeinfo.py [WORLD.ZZT]
# cheers and enjoy - kkairos / dan

def main():

	parser = argparse.ArgumentParser(description="ZZT File Size Breakdown")
	parser.add_argument("file")
	args = parser.parse_args()

	if args.file:
		path = args.file
	else:
		path = input("ZZT file path:")
	
	z = Zookeeper(path)
	
	print()
	print("FILE          | BOARD NAME                                 | SIZE  | OOP SIZE | OOP %")
	print("--------------+--------------------------------------------|-------|----------|------")
	running_size = 0
	running_oop = 0
	
	for board in z.boards:
		running_size+=board.size
		data_line = path
		while len(data_line) < 14:
			data_line += " "
		data_line += ("| " + board.title)
		oop_total = 0
		for stat in board.stats:
			if stat.oop_length:
				oop_total+=stat.oop_length
				running_oop+=stat.oop_length
		while len(data_line) < 59:
			data_line += " "
		data_line = data_line + "| " + str(board.size)
		while len(data_line) < 67:
			data_line += " "
		data_line = data_line + "| " + str(oop_total)
		while len(data_line) < 78:
			data_line += " "
		data_line += "| " + "{0:.2f}".format((oop_total/board.size)*100)
		print(data_line)
	print("--------------+--------------------------------------------|-------|----------|------")
	data_line = path
	while len(data_line) < 14:
		data_line += " "
	data_line += "| GRAND TOTALS"
	while len(data_line) < 59:
		data_line += " "
	data_line = data_line + "| " + str(running_size)
	while len(data_line) < 67:
		data_line += " "
	data_line = data_line + "| " + str(running_oop)
	while len(data_line) < 78:
		data_line += " "
	data_line += "| " + "{0:.2f}".format((running_oop/running_size)*100)
	print(data_line)

if __name__ == "__main__":
	main()
