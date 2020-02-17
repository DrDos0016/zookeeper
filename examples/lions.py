from zookeeper import Zookeeper, World, Board, Flag
import sys
import argparse
import textwrap

# built from analysis.py initally, with cues taken from code_search.py spits out world's board sizes,
# size of code on each board, and % of each board that is ZZT-OOP. I don't know 100% if the RLE element
# column is faithful because I think it might not include RLEs that are "underneath" other things.
#
# syntax: lions.py WORLD.ZZT [you may put additional filenames separated by space]
# 
# cheers and enjoy - kkairos / dan

def lions_tigers_and_bears(zzts):

	lines = []
	filler_line = "+----------+-------+-------+-------+-------+-------+-------+-------+"
	lines.append('\n'+filler_line)
	lines.append("| FILENAME | LIONS | TIGRS | BEARS | AMMO  | TRCHS | BRDS  | DkRms |")
	lines.append(filler_line)

	for zzt in zzts:
		z = Zookeeper(zzt)
	
		dark_boards,lion_count,tiger_count,bear_count,torch_count,ammo_count = 0,0,0,0,0,0

		working_line = "| " + pad_to(textwrap.shorten(zzt,len(zzt)-4,placeholder=''),9)
		for board in z.boards:
			
			if board.is_dark:
				dark_boards+=1
			for element in board.elements:
				if element.id == 41:
					lion_count+=1
				elif element.id == 42:
					tiger_count+=1
				elif element.id == 34:
					bear_count+=1
				elif element.id == 5:
					ammo_count+=1
				elif element.id == 6:
					torch_count+=1

		working_line += str(lion_count)
		working_line = pad_to(working_line,19)
		working_line += str(tiger_count)
		working_line = pad_to(working_line,27)
		working_line += str(bear_count)
		working_line = pad_to(working_line,35)
		working_line += str(ammo_count)
		working_line = pad_to(working_line,43)
		working_line += str(torch_count)
		working_line = pad_to(working_line,51)
		working_line += str(len(z.boards))
		working_line = pad_to(working_line,59)
		working_line += str(dark_boards)
		working_line = pad_to(working_line,67)
		lines.append(working_line)
	
	lines.append(filler_line)
	
	for line in lines:
		print(line)

	return

def main():

	args = sys.argv

	if len(args) > 1:
		zzts = []
		for i in range (1,(len(args))):
			zzts.append(args[i])
		lions_tigers_and_bears(zzts)
	else:
		print("Give at least one ZZT filename to analyze.")

def sdec(x):
	return "{0:.1f}".format(x)

def pad_to(str_x,x):
	while len(str_x) < x:
		str_x += " "
	return str_x + "| "

if __name__ == "__main__":
	main()