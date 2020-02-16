from zookeeper import Zookeeper, World, Board, Flag
import sys
import argparse
import textwrap
import os

# notes:
#
#	* 0ROBERT.ZZT should register no STK elements but will demonstrate cleanly how some such things might have been generated
#	* 0ROBTEST.ZZT should register no STK elements (torch/forest/energizer/ammo/water colors and resulting #put things treated as non-stk)
#	* to do:
#		* create a "tier" of STK looking for torch/forest/energizer/ammo colored things (being treated as non-STK right now)
#		* & give an option to look at that separately from less "hackable" STK
#		* export to CSV
#		* look at combining with codesize.py or creating a linking .py file for an "impressiveness"/"pretentiousness" meter
#
# tells you the amount of elements which are STK colors in a board. the commands below
# are NOT case-sensitive.
#
# thanks to asiekierka for suggesting this project and for some advice (and catching something re: element_colors[n] setup)
# thanks to rabbitboots and dr_dos for advice
#
# syntax:	python stk.py world WORLD.ZZT	does just WORLD.ZZT
#
#			python stk.py detail WORLD.ZZT	analyze WORLD.ZZT in excruciating detail
#											(prints every STK element)
#
# 			python stk.py all				analyze all .ZZT files in directory
#
#			python stk.py dir SUBDIR		analyze all .ZZT files in dubdirectory SUBDIR
#
# will also tell you if there's reason to suspect a corrupt board.
#
# to-do: introduce a tier of classification for torch, forest, ammo and energizer colors as opposed to full-on STK

def stk_check(zzts,details=False):

	# define element_colors: array of arrays

	# policy: decided NOT to count cyan, brown or purple "on" dark other colors for the time being.
	# will consider evidence of a multi-iteration loop of running, editing, savelock+debug etc.

	element_colors = []

	std_hacks = [3,5,6,7,9,10,11,12,13,14,15,20,31,47,63,79,95,111,127,143,191, 223, 239, 159, 149, 32,112,249]
	std_waterhacks = [121,122,123,124,125,126]
	std_doors = [3,5,6,7,9,10,11,12,13,14,15,20,31,47,63,79,95,111,127,143,175,191,207, 223,239]
	pascolors = [15,31,47,63,79,95,111,127]
	text_chars = []
	
	for x in range(32,127):
		text_chars.append(x)

	for x in range(0,54):
		element_colors.append([])
	
	element_colors[7] = std_hacks.copy() #gem
	element_colors[7].append(112)
	element_colors[8] = std_hacks.copy() #Key
	element_colors[9] = std_doors.copy() #door
	element_colors[11] = pascolors #Passage"
	element_colors[12] = [15,31,127] #duplicator
	element_colors[13] = std_hacks.copy() + std_waterhacks.copy() #Bomb"
	element_colors[16] = std_hacks.copy() #Clockwise Conveyor"
	element_colors[17] = std_hacks.copy() #Counter Clockwise Conveyor"
	element_colors[19] = std_hacks.copy() #water
	element_colors[21] = std_hacks.copy() #Solid Wall"
	element_colors[22] = std_hacks.copy() #Normal Wall"
	element_colors[23] = std_hacks.copy() #Breakable Wall"
	element_colors[24] = std_hacks.copy() #Boulder"
	element_colors[25] = std_hacks.copy() #Slider (NS)"
	element_colors[26] = std_hacks.copy() #Slider (EW)"
	element_colors[27] = std_hacks.copy() #Fake Wall"
	element_colors[28] = std_hacks.copy() #Invisible Wall"
	element_colors[29] = std_hacks.copy() + std_waterhacks.copy() #Blinkwall
	element_colors[30] = std_hacks.copy() + std_waterhacks.copy() #Transporter"
	element_colors[31] = std_hacks.copy() #Line Wall"
	element_colors[33] = std_hacks.copy() #H-Blinkray"
	element_colors[36] = std_hacks.copy() + std_waterhacks.copy() #Object"
	element_colors[37] = std_hacks.copy() + std_waterhacks.copy() #Slime
	element_colors[39] = std_hacks.copy() + std_waterhacks.copy() #spinning gun
	element_colors[40] = std_hacks.copy() + std_waterhacks.copy() #Pusher
	element_colors[43] = std_hacks.copy() #V-Blinkray"
	element_colors[44] = std_hacks.copy() + std_waterhacks.copy() + [0] #head
	element_colors[45] = std_hacks.copy() + std_waterhacks.copy() + [0] #segment

	element_colors[5] = [3] #ammo
	element_colors[6] = [6] #torch
	element_colors[14] = [5] #Energizer
	element_colors[19] = std_hacks.copy() #water
	element_colors[19].append(159)
	element_colors[19].append(249)
	element_colors[20] = [32] #Forest"
	element_colors[32] = [] #Ricochet"
	element_colors[32].append(10) #Ricochet"
	element_colors[34] = [6,118] #Bear
	element_colors[35] = [13,125] #Ruffian
	element_colors[38] = [7,23,39,55,71,87,103,119] #shark
	element_colors[41] = [12,124] #Lion
	element_colors[42] = [11,123] #Tiger

	text_elements = [47,48,49,50,51,52,53]

	lines = [("")]

	print("")
	for zzt in zzts:
		stk_found = 0
		non_stk_found = 0
		
		name = zzt[0]
		path = zzt[1]
		
		z = Zookeeper(zzt[1])

		print("Checking " + zzt[0] + "...")
		
		for board in z.boards:

			for element in board.elements:
				try:
					if len(element_colors[element.id]) > 0:
						if element.color_id not in element_colors[element.id]:
							stk_found+=1
							element_x,element_y = (element.tile % 60),(element.tile // 60)
							if details:
								print( zzt[0] + " STK element on " + board.title + " " + str(element_x) + "," + str(element_y) + ": " + str(element.color_id) )
						else:
							non_stk_found+=1
					elif element.id in text_elements:
						if element.character not in text_chars:
							stk_found+=1
							element_x,element_y = (element.tile % 60),(element.tile // 60)
							if details:
								print( zzt[0] + " STK element on " + board.title + " " + str(element_x) + "," + str(element_y) + ": " + str(element.color_id) )
						else:
							non_stk_found+=1
				except IndexError:
					print("Warning: " + zzt[0] + " board " +  board.title + " may be corrupted.")
					break

		lines.append(zzt[0] + " | non-STK: " + str(non_stk_found) + " | STK: " + str(stk_found) + " | % STK: " + sdec(stk_found/(non_stk_found+stk_found)*100))

	return lines

def main_help(error_name="Unspecified syntax error."):
	
	error_line = "\nError: "
	
	if error_name == "no_args":
		error_line += "No arguments given."
	elif error_name == "no_world":
		error_line += "World argument requires valid .zzt file as argument."
	elif error_name == "no_worlds":
		error_line += "Called 'all' or 'dir' but no .ZZT files were found in requested directory."
	elif error_name == "no_dir":
		error_line += "Dir argument requires directory as argument."
	else:
		error_line += "Unspecified."
	
	lines = [error_line]
	
	lines.append("\nSyntax help:\n")
	lines.append("\tpython stk.py world WORLD.ZZT - analyze WORLD.ZZT")
	lines.append("\tpython stk.py detail WORLD.ZZT - analyze WORLD.ZZT in excruciating detail")
	lines.append("\tpython stk.py all - analyze all .ZZT files in directory")
	lines.append("\tpython stk.py dir /SUBDIR - analyze all .ZZT files in dubdirectory SUBDIR")
	lines.append("\nHappy hunting!")
	return lines

def get_zzts(scanpath,working_dir=""):
	zzts = []
	files = os.scandir(scanpath)
	for file in files:
		if (file.is_file() and (file.name.endswith(".zzt") or file.name.endswith(".ZZT"))):
			zzts.append((file.name, file.path))
	return zzts

def main():

	args = sys.argv

	if len(args) < 2:
		lines = main_help("no_args")
	elif args[1] == "world":
		if len(args) < 3:
			lines = main_help("no_world")
		else:
			zzts = [(args[2],args[2])]
			lines = stk_check(zzts,False)
	elif args[1] == "detail":
		if len(args) < 3:
			lines = main_help("no_world")
		else:
			zzts = [(args[2],args[2])]
			lines = stk_check(zzts,True)
	elif args[1] == "all":
		scanpath = os.getcwd()
		zzts = get_zzts(scanpath)
		if len(zzts) == 0:
			lines = main_help("no_worlds")
		else:
			lines = stk_check(zzts,False)
	elif args[1] == "dir":
		if len(args) < 3:
			lines = main_help("no_dir")
		else:
			working_dir = "\\" + args[2]
			scanpath = os.getcwd() + working_dir
			zzts = get_zzts(scanpath,working_dir)
		if len(zzts) == 0:
			lines = main_help("no_worlds")
		else:
			lines = stk_check(zzts,False)

	else:
		lines = main_help()

	for line in lines:
		print(line)
		
def sdec(x):
	return "{0:.1f}".format(x)

def pad_to(str_x,x):
	while len(str_x) < x:
		str_x += " "
	return str_x + "| "

if __name__ == "__main__":
	main()