import sys, os
import pandas as pd
import numpy as np

sys.path.append(os.path.join("."))
from lib.generator import generate
from lib.block import block

# create the sat range for block 666 
# this will save a file in ./data/event_sat_range/ folder
#
df_a = block(event_name="block666", save=True).create_sat_range(666)
print(df_a.head())

# generate palindromes for event block666 -> sat_range file must exist in ./data/event_sat_range/ folder 
#
df_b = generate(event_name="block666", save=True).palindromes()
print(df_b.head())

# generate satributes for event block666 -> palindrome file must exist in ./data/palindromes/ folder
#
df_c = generate(event_name="block666", save=True).satributes()
print(df_c.head())

# show stats for block666
#
df_d = df_c.groupby(["event",
                     "palinception",
                     "sub_palindromes",
                     "perfect_palinception",
                     "perfect_overlap_palinception",
                     "2d",
                     "3d"])["valid"].count().rename("count").reset_index()
print(df_d)