import numpy as np
import pandas as pd

class palindrome:

    def __init__(self, sat_number: int):     
        # initialize the class object with sat_number (it is going to be used by all functions).
        self.sat_number = sat_number
        
        # alphabet map required for rodarmor_names
        alphabet = [x for x in "abcdefghijklmnopqrstuvwxyz"]
        alphabet = {str(x): y for x, y in zip(list(range(0,26)),alphabet)}
        alphabet.update({"-1": "z"})
        
        self.alphabet = alphabet
        self.LAST_SAT = 2099999997690000
    
    @staticmethod
    def __divide_by__(dividend: int, divisor: int):
        """returns the division result and the carry from a division between sat_number and denominator

        Parameters:
        dividend (int): dividend
        divisor (int): divisor

        Returns:
        (int, int): result and carry

        """ 
        return dividend//divisor, dividend % divisor
    
    @staticmethod
    def __is_valid__(sat_number: any):
        """Verifies if a sat number if a palindrome or not

        Parameters:
        sat_number (int): sat number in str or int or float form

        Returns:
        bool: True if sat_number is palindrome, False otherwise

        """     
        # verify if sat_number if integer or a string
        if isinstance(sat_number, int):
            sat = str(sat_number)
        else:
            sat = sat_number
            
        # get sat number of digits
        length = len(sat)
        
        # if its even number of digits spliter is half.
        if length%2 == 0:
            spliter = int(length/2)
            
        # In the case of an odd number, spliter adds 1
        # This enables breaking the sat number in half
        # example:
        #         123321 -> even number of digits, we divide into two halves of interest 123 and 321
        #         12321  -> odd number of digits, we divide into two halves of interest 12 and 21, the mid digit is obfuscated.
        else:
            spliter = int(length/2+1)
            
        # second half     
        a = [x for x in sat[spliter:]]
        
        # first half
        b = [x for x in sat[:-spliter]]
        
        # reverse first half
        b.reverse()
        
        # assess if first half = second half reversed (txaram, we have a palindrome if true, otherwise, false)
        return a == b

    def is_2d(self):
        """Verifies if a palindrome is 2d or not

        Parameters:
        self: gets sat_number from class object self.sat_number

        Returns:
        bool: True if palindrome is 2d, False otherwise

        """         
        # split sat number into array of digits
        sat = [x for x in str(self.sat_number)]
        
        # count the number of unique digits and equal to 2.
        return 2 == len(np.unique(sat))

    def is_3d(self):
        """Verifies if a palindrome is 3d or not

        Parameters:
        self: gets sat_number from class object self.sat_number

        Returns:
        bool: True if palindrome is 3d, False otherwise

        """         
        # split sat number into array of digits
        sat = [x for x in str(self.sat_number)]
        
        # count the number of unique digits and equal to 3.
        return 3 == len(np.unique(sat))

    def is_palinception(self):
        """Verifies if a palindrome is palinception or not.
           A palinception is a palindrome composed of multiple sub_palindromes all of the same size

           Example:
                   121666121 has 3 sub_palindromes of 3 digits each "121", "666" and "121"

        Parameters:
        self: gets sat_number from class object self.sat_number

        Returns:
        bool: True if palindrome is palinception, False otherwise

        """  
        # convert sat to string
        sat = str(self.sat_number)
        
        # get number of digits in sat
        l = len(sat)  
        
        # create a list consisting in how many parts we can divide the sat number
        # example:
        #         123456789012 has 12 digits, which means it is divisible by 2, 3, 4 and 6. 
        #         the result of slices = [2,3,4,6]
        slices = [i for i in range(2, l//2+1) if l % i == 0]  

        # iterate over divisible.
        for i in slices:  
            
            # determine slice size. If i = 4 (parts) and digits = 12, we have 4 sub_palindromes with 3 digits each.
            slice_size = int(l/i)
            
            # reverse each sub_set of digits and compare it with original sub_set of digits to validate if its palindrome
            # example:
            #         121131121 into 3 slices "121", "131", "121", it returns ["True", "True", "True"]
            #         122131221 into 3 slices "122", "131", "221", it returns ["False", "True", "False"]
            valid = [sat[j*slice_size:(j+1)*slice_size] == sat[j*slice_size:(j+1)*slice_size][::-1] for j in range(i)]  
            
            # if all values in "valid" are True, then it has subpalindromes -> returns True and the number of subpalindromes.
            if all(valid):  
                return True, i  

        # otherwise it does not have sub_palindromes and returns false and 0.
        return False, 0
    
    
    def is_perfect_palinception(self): 
        """Verifies if a palindrome is palinception or not.
           A palinception is a palindrome composed of multiple sub_palindromes, 
           all of the same size
           all sub_palindromes must be equal

           Example:
                   121121121 has 3 sub_palindromes of 3 digits each "121", "121" and "121" and they are all the same sub_palindrome

        Parameters:
        self: gets sat_number from class object self.sat_number

        Returns:
        bool: True if palindrome is perfect palinception, False otherwise

        """          
        # get number of sub_palindromes
        _, number_of_sub_palindromes = self.is_palinception()
        
        # if zero, does not have and returns False
        if number_of_sub_palindromes == 0:  
            return False  
        
        # convert sat_number to str
        sat = str(self.sat_number) 
        
        # determine sub_palindrome size
        # example:
        #         122113311221 has 12 digits and has 3 sub_palindromes, each sub_size = 4 -> [1221, 1331, 1221]
        sub_size = len(sat) // number_of_sub_palindromes 
        
        # create the subset as writen in the above example
        temp = [sat[i*sub_size:(i+1)*sub_size] for i in range(number_of_sub_palindromes)]  
        
        # if all sub_palindromes are the same (function set removes duplicates), the returns True, otherwise, False
        return len(set(temp)) == 1 

    
    def is_perfect_overlap_palinception(self):  
        """Verifies if a palindrome is palinception or not.
           A palinception is an odd sized palindrome, composed of exactly 2 sub_palindromes
           and they must share the mid digit, which must be equal to the first and last digits.

           Example:
                   122212221 has 2 sub_palindromes of 5 digits each "12221" and "12221", where the mid digit is common.

        Parameters:
        self: gets sat_number from class object self.sat_number

        Returns:
        bool: True if palindrome is perfect overlap palinception, False otherwise

        """         
        # convert sat_number to str
        sat = str(self.sat_number)  
        
        # determine if sat has even or odd number of sats
        is_even = len(sat) % 2 == 0  
        offset = 0 if is_even else 1  

        # split sat in two halves, if sat has odd number of digits, discards middle digit.
        init = sat[:int(len(sat)/2)+offset]  
        end = sat[int(len(sat)/2):]  
        end = end[::-1]  

        # conditions to return true, must all be satisfied.
        # 1: odd number of digits (this is an OVERLAP perfect palindrome
        # 2: mid digit must be equal to first and last digit
        # 3: both halves must be a palindrome themselves
        return self.__is_valid__(int(init)) and self.__is_valid__(int(end)) and not is_even and sat[0] == sat[int(len(sat)/2)] 

    def name(self, divisor: int = 26):
        """Returns the sat name according to rodarmor factorization (26).

        Parameters:
        self: gets sat_number from class object self.sat_number
        divisor: the factorization value (26 by default). If you change the divisor to 3, you will get names with only the letters (a,b,c).

        Returns:
        str: sat name according to rodarmor factorization

        """  
        result = []
        temp = self.LAST_SAT - self.sat_number

        while(True):
            res, carry = self.__divide_by__(temp, divisor)

            result.append(str(carry-1))
            temp = res
            
            if res <= 1:
                if res == 1:
                    result.append(str(res-1))
                break
        result.reverse()
        result = [self.alphabet[x] for x in result]
        return ("").join(result)