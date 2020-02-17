from zookeeper import Zookeeper, World, Board, Flag
import sys
import argparse
import textwrap

# built from analysis.py initally, with cues taken from code_search.py spits out world's board sizes,
# size of code on each board, and % of each board that is ZZT-OOP. I don't know 100% if the RLE element
# column is faithful because I think it might not include RLEs that are "underneath" other things.
#
# syntax: python codesize.py WORLD.ZZT
# 
# cheers and enjoy - kkairos / dan

def codesize(path,summary_only):

	z = Zookeeper(path)
	lines = []
	
	filler_line = "+----------+---------------------------------------------------+-------+-------+-------+------+"
	lines.append('\n'+filler_line)
	lines.append("| FILENAME | BOARD                                             | BYTES | RLE   | OOP   | OOP% |")
	lines.append(filler_line)
	size_total = 0
	oop_total = 0	
	disp_path = "| " + pad_to(textwrap.shorten(path,len(path)-4,placeholder=''),9)
		
	for board in z.boards:
	
		size_total += board.size
		board_line = disp_path + board.title
		board_oop = 0
		
		for stat in board.stats:
		
			if stat.oop_length:
				board_oop += stat.oop_length

		oop_total += board_oop
		
		board_rle = 3*len(board.rle_elements)
		board_line = pad_to(board_line,63) + str(board.size)
		board_line = pad_to(board_line,71) + str(board_rle)
		board_line = pad_to(board_line,79) + str(board_oop)
		board_line = pad_to(board_line,87) + sdec((board_oop/board.size)*100)
		board_line = pad_to(board_line,94)
		
		lines.append(board_line)
		
	board_line = "\n" + path + " size is " + str(size_total) +"b and total ZZT-OOP size is " + str(oop_total) + "b for a total of " + sdec((oop_total/size_total)*100) + " percent ZZT-OOP."
	
	lines.append(filler_line + "\n" + board_line)
	
	if summary_only == False:
		for line in lines:
			print(line)
	else:
		print(board_line)
	
	return

def main():

	args = sys.argv

	if len(args) == 2:
		codesize(args[1],False)
	elif len(args) > 2:
		zzts = []
		for i in range (1,(len(args))):
			zzts.append(args[i])
		for zzt in zzts:
			codesize(zzt,True)
	else:
		path = ""
		while (len(path) < 1):
			path = input("\nThis tool shows code size versus ZZT board and file size.\nZZT File Name (Include .ZZT !):")
		codesize(path,False)

def sdec(x):
	return "{0:.1f}".format(x)

def pad_to(str_x,x):
	while len(str_x) < x:
		str_x += " "
	return str_x + "| "

if __name__ == "__main__":
	main()