import pandas as pd
import numpy as np
import os, sys
sys.path.append(os.path.join("."))
sys.path.append(os.path.join(".."))
from local.config import SATS_DIGITS, SATS_PER_BTC
from lib.palindrome import palindrome
from lib.block import block
from os import listdir
from os.path import isfile, join

class generate:
    
    def __init__(self, event_name: str, save: bool = False):

        # get current event_sat_range names
        events = [f for f in listdir(f"./data/event_sat_range") if isfile(join(f"./data/event_sat_range", f))]
        events = [x.replace(".csv", "") for x in events]

        # confirm that event name belongs to one of the existing ones
        if event_name not in events or "block" not in event_name:
            print(f"[ERROR] Event not recognized ({event_name})")  
            sys.exit(0)
        
        # otherwise assign event name to class object
        else:
            self.name = event_name
        
        # same for save variable, if True, a file is created, if False, just returns a dataframe
        self.save = save
        
        self.SATS_PER_BTC = SATS_PER_BTC
        self.SATS_DIGITS = SATS_DIGITS

    def __compute_palindromes__(self, init_btc: int):  
        """ Computes all palindrome sats for a given bitcoin unit

        Parameters:
        init_btc (int): the bitcoin unit

        Returns:
        list: list of all palindromes for a given bitcoin unit.

        """          
        # retrieve the number of digits of the bitcoin unit. (1 bitcoin unit = 100 000 000 satoshis).
        btc_digits = len(str(init_btc))  
        
        # get the size of the mid digit count
        # example:
        #         btc unit 450 corresponds to 45000000000 satoshis, meaning we want to split it as
        #         450 + 00000 + 000 
        #         this is because a palindrome must have the first 3 digits (btc unit) must be the same as 
        #         the reversed end 3 digits -> 450 + 00000 + 054.
        #         this means that we need to build palindromes for the 5 mid digits. See as reference build_pali_list function.
        mid_digit_count = SATS_DIGITS - btc_digits  
        
        # get a str object of the btc unit
        init = str(init_btc)  
        
        # get a string object of the btc unit reversed (last 3 digits of the example above
        end = str(init_btc)[::-1]  

        # if there are mid digits
        if mid_digit_count > 0:  
            
            # read the pre computed list of mid palindromes (the 5 digits of the previous example.
            df = pd.read_csv(f"./data/pre_computed/{mid_digit_count}_pali_list.csv", sep=";")  
            
            # guarantee that they are cast as str objects and have a zero padding
            # because they will be read as ints from the read_csv function
            # so integer 100 must be filled with zeros up to the mid_digit_count of 5 resulting in "00100"
            df["mid"] = df["mid"].astype(str).str.zfill(mid_digit_count)  
            
            # create a column init for the concatenation operation (450)
            df["init"] = init  
            
            # create a column end for the concatenation operation (054)
            df["end"] = end  
            
            # create the palindrome by concatenating all the strings (450 + 00100 + 054)
            df["palindrome"] = df["init"] + df["mid"] + df["end"]  

        # in case there are no middle digits (impossible but good rules of coding dictate I code this chance)
        # just adds the init and end
        else:  
            df = pd.DataFrame({"palindrome": [init + end]})  

        # return a list with all the palindromes
        return df["palindrome"].values   

    def __get_btc_units_in_sat_range__(self, first_sat: int, last_sat: int):  
        """ Computes the btc units for a given sat range defined by first sat and last sat

        Parameters:
        first_sat (int): the first sat
        last_sat (int): the last sat

        Returns:
        list: the list of btc units inside the sat range.

        """          
        # verifies that last_sat is bigger than first_sat
        if first_sat > last_sat:  
            print("Error")  
            return None  
        
        # gets first btc dividing first sat by sats_per_btc
        first_btc = first_sat // SATS_PER_BTC
        
        # gets last btc dividing last sat by sats_per_btc
        last_btc = last_sat // SATS_PER_BTC 
        
        # returns btc range
        return list(range(first_btc, last_btc + 1))

    def __read_event_sat_range__(self): 
        """ reads the sat range from the folder ./data/event_sat_range/. 
            if the file does not exist, it creates the sat range if and only if the event name is 'block#'.

        Parameters:
        self: reads class objects

        Returns:
        pd.DataFrame: dataframe with the sat range (or sat ranges in case multiple ranges exist).

        """   
        try:
            # read event_data ranges
            df = pd.read_csv(f"./data/event_sat_range/{self.name}.csv", sep=";")  
        except Exception as err:
            
            # self explanatory
            print("[ERROR] event data does not exist.", err)
            
            if "block" in self.name:
                # replace block from the event name
                temp = self.name.replace("block", "")
            
                # create sat range for block
                df = block(event_name = self.name, save = True).create_sat_range(int(temp))
                
            else:
                print("[ERROR] block name not conforming with block#.")
                return None
        
        # create a new "raw" column with a sat tupple to be used in a lambda function 
        df["raw"] = list(zip(df["init"], df["end"]))  
        
        # return this dataframe with 3 columns "raw" "init" and "end"
        return df  
    
    def palindromes(self, override: bool = False):  
        """ computes palindromes for a given event. An event identifies a sat range, which is used to compute the palindromes.
            example: Block9 has 1 range defined by first and last sat
                     Hitman has multiple non sequential ranges

        Parameters:
        override (bool): if True, any existing data is overriden.

        Returns:
        pd.DataFrame: dataframe with the all palindromes for a given sat range

        """  
        try:
            # tries to check if palindrome data already exists
            df = pd.read_csv(f"./data/palindromes/{self.name}.csv", sep=";")
            print(f"[INFO] Data for {self.name} already exists from file")
            
            # if we do not want to override, we just return the existing data
            if not override:
                return df
            
        except Exception as err:
            # otherwise move on
            print(f"[INFO] Creating new palindrome data from {self.name} data ranges.")
            pass
            
        # get event data (not palindrome data)
        df = self.__read_event_sat_range__()  

        # if no event data exists, return none
        if df is None:
            return None

        # define btc units in sat range.
        # example:
        #         if range is 45000000000 to 45200000000 , the btc unit range is a list [450, 451]
        df["btc_unit"] = df["raw"].apply(lambda x: self.__get_btc_units_in_sat_range__(x[0], x[1]))  

        # explode btc units to create 1 line in the dataframe per btc unit (this is to build the palindromes
        # see as reference __get_palis__
        df = df.explode("btc_unit")  

        # apply __get_palis__ function to create a list of all palindromes in the btc unit range
        df["palindrome"] = df["btc_unit"].apply(lambda x: self.__compute_palindromes__(x))  

        # explode to create 1 line in the dataframe per palindrome
        df = df.explode("palindrome")  

        # make "valid" as True if palindrome is inside the sat range, False if its not.
        df["valid"] = [int(a) <= int(x) <= int(b) for a,b,x in zip(df["init"], df["end"], df["palindrome"])]  

        # Filter palindromes marked as True only
        df = df.loc[df["valid"] == True]  

        # drop raw column (not needed anymore
        df = df.drop(columns=["raw"])  

        # get current column names
        cols = df.columns.tolist()  

        # create a column with the event name
        df["event"] = self.name  
        
        # reorder columns
        df = df[["event"] + cols]  

        # is save is True, save the data
        if self.save:  
            df.to_csv(f"./data/palindromes/{self.name}.csv", sep=";", index=False)  

        # return the result dataframe
        return df 
    
    def satributes(self):
        """ gets the palindromes for a given sat range/event and calculates the satributes for each palindrome in the dataframe.

        Parameters:
        self: reads class objects

        Returns:
        pd.DataFrame: dataframe with the satributes added to the original palindrome dataframe.

        """          

        try:
            # get palindrome data if it exists
            df = pd.read_csv(f"./data/palindromes/{self.name}.csv", sep=";")
        except:
            # if not
            print("[WARN] evet does not exist, generating data from event data.")
            
            # record self.save state
            temp = self.save
            
            # set self.save to True to save the file
            self.save = True
            
            # get palindromes list for this event and save it
            df = self.palindromes()
            
            # restore original save state
            self.save = temp
            
        # add column with sat name
        df["name"] = df["palindrome"].apply(lambda x: palindrome(x).name())
            
        # add column with palidrome digit size.
        df["pali_size"] = df["palindrome"].apply(lambda x: len(str(x)))
        
        # create a temp column with a tupple (has sub palindromes, how many palindromes)
        df["temp"] = df["palindrome"].apply(lambda x: palindrome(x).is_palinception())
        
        # create 2 separate columns from the information of the previous step
        df["palinception"] = df["temp"].apply(lambda x: x[0])
        df["sub_palindromes"] = df["temp"].apply(lambda x: x[1])
        
        # and drop the temp column
        df = df.drop(columns=["temp"])
        
        # insert new column with True/False if all sub_palindromes are equal
        df["perfect_palinception"] = [palindrome(x).is_perfect_palinception() for x in df["palindrome"]]
        
        # insert new column with overlap perfect palindrome as True/False
        df["perfect_overlap_palinception"] = df["palindrome"].apply(lambda x: palindrome(x).is_perfect_overlap_palinception())
        
        # insert True/False if its 2 digits palindrome
        df["2d"] = df["palindrome"].apply(lambda x: palindrome(x).is_2d())
        
        # insert True/False if its 3 digits palindrome
        df["3d"] = df["palindrome"].apply(lambda x: palindrome(x).is_3d())
        
        # return enriched palindrome data
        return df