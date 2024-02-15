import pandas as pd

def compute_fix_digits_palindrome(max_digits: int, save: bool = False):
""" computes all palindromes for a fix digit size and saves them into a file of pre computed palindromes.

Parameters:
max_digits (int): fixe digit size of palindrome
save (bool): True if file must be saved, False otherwise 
    
Returns:
pd.DataFrame: dataframe with the all palindromes of max_digits size.

"""  
    # create an empty palidrome list
    pali_list = []
    
    # define the max range of the palindrome list. If I have 5 digits, the max palidrome is 99999
    _range = int("9"*max_digits) 
    
    # iterate over range to check if number is palindrome
    for i in range(0, _range + 1):
        
        # fill with zeros on the left side. 
        # This is because we are creating sub-palindromes that are in the middle of the sat number
        temp = str(i).zfill(max_digits)
        
        # if number if palindrome then append it to the list.
        if palindrome(0).is_pali(temp):
            pali_list.append(temp)
            
    # create a dataframe with the sub_palindromes 
    df = pd.DataFrame({"mid": pali_list})
    
    # if save, save this pre-computed list in the folder "operational_data" and the name prefixed with the number of digits
    # for 5_pali_list.csv, we have all sub_palindromes with 5 digits from 00000 to 99999.
    if save:
        df.to_csv(f"../data/pre_computed/{max_digits}_pali_list.csv", sep=";", index=False)
    
    return df