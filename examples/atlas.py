# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from zookeeper import Zookeeper, World, Board
from PIL import Image
from PIL import ImageColor

visited_board_index_list = []
all_boards = []

def explore_world(board_index, board_coordinate_map, x, y):
    #This function follows the links from board to board and works out their coordinates
    #relative to other boards. Each time it finds a linked board, it calls this same
    #function recursively with the coordinates. It uses a list of visited board indices
    #to make sure that it isn't going to go around in an infinite loop.
    board_coordinate_map[board_index] = {'x': x, 'y': y}
    visited_board_index_list.append(board_index)
    board_to_examine = all_boards[board_index]
    print("Examining exits of: " + board_to_examine.title)

    adjacent_board_index = board_to_examine.board_north
    if (adjacent_board_index > 0 and adjacent_board_index not in visited_board_index_list):
        explore_world(adjacent_board_index, board_coordinate_map, x, y-1)

    adjacent_board_index = board_to_examine.board_south
    if (adjacent_board_index > 0 and adjacent_board_index not in visited_board_index_list):
        explore_world(adjacent_board_index, board_coordinate_map, x, y+1)

    adjacent_board_index = board_to_examine.board_west
    if (adjacent_board_index > 0 and adjacent_board_index not in visited_board_index_list):
        explore_world(adjacent_board_index, board_coordinate_map, x-1, y)

    adjacent_board_index = board_to_examine.board_east
    if (adjacent_board_index > 0 and adjacent_board_index not in visited_board_index_list):
        explore_world(adjacent_board_index, board_coordinate_map, x+1, y)

    return board_coordinate_map

def main():
    global all_boards
    global visited_board_index_list
    # Check that at least three arguments were passed to the script
    if len(sys.argv) < 4:
        print("Run: python atlas.py <zztworld> <outputfilename> <startingboardindex>")
        print("Ex: python atlas.py WORLD.ZZT ATLAS.PNG 8")
        print("\nThis script will save a PNG of the world map starting from the specified board.")
        sys.exit()

    #Define screen height and width here so we don't have to repeat them
    screen_height = 350
    screen_width = 480
    
    # Iterate over the files provided
    file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    starting_board = sys.argv[3]

    # Create a Zookeeper object
    zoo = Zookeeper(file_name)
    all_boards = zoo.boards

    #Now explore the world starting from the given board number.
    #We pass in the starting board index and say that it's at coordinate 0, 0
    print("Loaded world:", zoo.meta.file_name)
    print("-"*40)
    print("Exploring...")
    board_coordinate_map = explore_world(int(starting_board), {}, 0, 0)
    
    #Print the board coordinate map that we generated
    print("-"*40)
    print("Generated board coordinate map")
    print(board_coordinate_map)

    #To find the dimensions of our image, get the maximum and minimum X/Y coordinates
    #in the map. The total width or height is the difference between the two, plus one.
    min_x = None
    min_y = None
    max_x = None
    max_y = None

    for board_index in board_coordinate_map:
        x = board_coordinate_map[board_index]['x']
        y = board_coordinate_map[board_index]['y']
        if (min_x == None or x < min_x):
            min_x = x
        if (min_y == None or y < min_y):
            min_y = y
        if (max_x == None or x > max_x):
            max_x = x
        if (max_y == None or y > max_y):
            max_y = y
    
    atlas_width = (max_x - min_x) + 1
    atlas_height = (max_y - min_y) + 1    
    print("Board coordinate map is " + str(atlas_width) + " by " + str(atlas_height) + " screens")
    print("-"*40)
    
    #Now we want to create a black image of the size we worked out so we can start pasting screenshots in
    atlas_image = Image.new("RGB", (screen_width*atlas_width, screen_height*atlas_height), "black")

    print("Rendering included boards...")
    #Render only the images that we need from the list of all boards
    images = {}
    for idx, board in enumerate(all_boards):
        if(idx in list(board_coordinate_map.keys())):
            images[idx] = board.render()
            print("Rendered board " + str(idx))
    print("-"*40)

    print("Assembling...")
    #Now paste the images into our canvas according to their coordinates in the map.
    #Offset them with our minimum X/Y coordinates so that the minimum comes out as 0, 0
    for board_index in board_coordinate_map:
        x = board_coordinate_map[board_index]['x']
        y = board_coordinate_map[board_index]['y']
        x -= min_x
        y -= min_y
        print("Pasting board " + str(board_index) + " \"" + all_boards[board_index].title + "\" at " + str(x) + ", " + str(y))
        atlas_image.paste(images[board_index], (screen_width*x, screen_height*y))

    #Finally, save the large image and declare that we're finished!        
    atlas_image.save(output_file_name)

    print("-"*40)
    print("\nSaved " + output_file_name + ".")

if __name__ == "__main__":
    main()
