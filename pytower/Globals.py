# -*- coding: utf-8 -*-

# It feels wrong, but I'm not a python guru...
s_window = None
dr_window = []

f_loading = None
s_loading = None
r_loading = None

s_full = None

s_mini = None

h_offset = 0
v_offset = 0

q_tx = None
q_rx = None

objects = [ [], [], [], [], [], [], [] ] # 0 stars, 1 star, 2, 3, 4, 5, TOWER

cash = 0
game_clock = [ 1, 1, 1, 0, 0 ] # Y, M, D, H, M
population = 0
