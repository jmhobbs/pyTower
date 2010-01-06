# -*- coding: utf-8 -*-

if __name__ == "__main__":
	print "Sorry, you can't run this stand-alone."
	exit()

# It feels wrong, but I'm not a python guru and have no other fix...
s_window = None
dr_window = []
s_render = None # This is the surface we render the game onto, then we blit over to the window surface

f_loading = None
s_loading = None
r_loading = None

s_mini = None

h_offset = 0 # How many slices we are from the left
v_offset = 0 # How many floors we are from the top

q_tx = None
q_rx = None

# Resources
res_floor = None
res_dirt = None

objects = [ [], [], [], [], [], [], [] ] # 0 stars, 1 star, 2, 3, 4, 5, TOWER

cash = 0
game_clock = [ 1, 1, 1, 0, 0 ] # Y, M, D, H, M
population = 0

game_map = None

# The cursor...
r_cursor = [ 0 ] * 4
s_cursor = None