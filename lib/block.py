import os, sys
sys.path.append(os.path.join("."))
sys.path.append(os.path.join(".."))
from local.config import BLOCK_PER_HALVING, FIRST_REWARD, SATS_PER_BTC
import pandas as pd

# 0 - 209999 = 50
# 210000 - 419999 = 25
# 420000 - 629999 = 12.5

class block:
    
    def __init__(self, event_name: str, save: bool = False):
        
        self.BLOCK_PER_HALVING = BLOCK_PER_HALVING
        self.FIRST_REWARD = FIRST_REWARD
        self.SATS_PER_BTC = SATS_PER_BTC
        self.name = event_name
        self.save = save
           
    def reward(self, block_number: int):
        """ Computes the reward in btc for a given block number

        Parameters:
        block_number (int): the block number

        Returns:
        float: the btc reward

        """  
        return self.FIRST_REWARD/pow(2,(block_number//self.BLOCK_PER_HALVING))

    def create_sat_range(self, block_number: int):  
        """ Creates the sat range (first and last sat) of a given block

        Parameters:
        block_number (int): the block number

        Returns:
        pd.DataFrame: a dataframe with 2 columns "init" and "end" corresponding to the first and last sat of the block.

        """
        init_sat = 0  
        halvings = block_number // self.BLOCK_PER_HALVING  

        for i in range(1, halvings + 2):  
            block_difference = block_number - (i - 1) * self.BLOCK_PER_HALVING  
            if block_difference > self.BLOCK_PER_HALVING:  
                init_sat += self.BLOCK_PER_HALVING * self.reward(i * self.BLOCK_PER_HALVING - 1)  
            else:  
                init_sat += block_difference * self.reward(i * self.BLOCK_PER_HALVING - 1)  

        end_sat = (init_sat + self.reward(block_number)) * self.SATS_PER_BTC - 1  
        init_sat *= self.SATS_PER_BTC  

        df = pd.DataFrame({"init": [int(init_sat)], "end": [int(end_sat)]})  
        
        if self.save:  
            df.to_csv(f"./data/event_sat_range/{self.name}.csv", sep=";", index=False)  
        
        return df