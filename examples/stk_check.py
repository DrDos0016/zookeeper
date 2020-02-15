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

def stk_check(zzts):

	element_colors = []
	
	for x in range(0,54):
		element_colors.append([])
	
	std_hacks = [3,5,6,7,9,10,11,12,13,14,15,20,31,47,63,79,95,111,127, 143,191, 223, 239]
	pascolors = [15,31,47,63,79,95,111,127]

	#15,"Star",
	#33,"Horizontal Blink Ray",
	#43,"Vertical Blink Ray",

	element_colors[5] = [3] #ammo
	element_colors[6] = [6] #torch
	element_colors[7] = std_hacks #gem
	element_colors[8] = std_hacks #Key
	element_colors[9] = std_hacks #door
	element_colors[11] = pascolors #Passage"
	element_colors[12] = std_hacks #duplicator
	element_colors[13] = std_hacks #Bomb"
	element_colors[14] = [5] #Energizer
	element_colors[16] = std_hacks #Clockwise Conveyor"
	element_colors[17] = std_hacks #Counter Clockwise Conveyor"
	element_colors[19] = std_hacks #water
	element_colors[19].append(159)
	element_colors[20] = [20] #Forest"
	element_colors[21] = std_hacks #Solid Wall"
	element_colors[22] = std_hacks #Normal Wall"
	element_colors[23] = std_hacks #Breakable Wall"
	element_colors[24] = std_hacks #Boulder"
	element_colors[25] = std_hacks #Slider (NS)"
	element_colors[26] = std_hacks #Slider (EW)"
	element_colors[27] = std_hacks #Fake Wall"
	element_colors[28] = std_hacks #Invisible Wall"
	element_colors[29] = std_hacks #Blinkwall
	element_colors[30] = std_hacks #Transporter"
	element_colors[31] = std_hacks #Line Wall"
	element_colors[32] = [10] #Ricochet"
	element_colors[34] = [6] #Bear
	element_colors[35] = [13] #Ruffian
	element_colors[36] = std_hacks #Object"
	element_colors[37] = std_hacks #Slime
	element_colors[38] = std_hacks #shark
	element_colors[39] = std_hacks #spinning gun
	element_colors[40] = std_hacks #Pusher
	element_colors[41] = [12] #Lion
	element_colors[42] = [11] #Tiger
	element_colors[44] = std_hacks #head
	element_colors[45] = std_hacks #linewalls

	lines = []
	#filler_line = "+----------+-------+-------+-------+-------+-------+-------+-------+"
	#lines.append('\n'+filler_line)
	#lines.append("| FILENAME | LIONS | TIGRS | BEARS | AMMO  | TRCHS | BRDS  | DkRms |")
	#lines.append(filler_line)

	for zzt in zzts:
		stk_found = 0
		z = Zookeeper(zzt)

		working_line = "| " + pad_to(textwrap.shorten(zzt,len(zzt)-4,placeholder=''),9)
		for board in z.boards:
			
			for element in board.elements:
				if len(element_colors[element.id]) > 0:
					if element.color_id not in element_colors[element.id]:
						stk_found+=1
	
		if stk_found == 0:
			lines.append("Totally non-STK")
		else:
			lines.append(zzt + ": found " + str(stk_found) + " STK element(s)")
	
	#lines.append(filler_line)
	
	for line in lines:
		print(line)

	return

def main():

	args = sys.argv

	if len(args) > 1:
		zzts = []
		for i in range (1,(len(args))):
			zzts.append(args[i])
		stk_check(zzts)
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