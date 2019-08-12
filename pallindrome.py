# Given a string, write a python function to check if it is palindrome or not.
# A string is said to be palindrome if reverse of the string is same as string.For example, "radar" is palindrome, but "radix" is not palindrome.

# string_name[beginning: end : step]
# start - starting integer where the slicing of the object starts
# stop - integer until which the slicing takes place. The slicing stops at index stop - 1.
# step - integer value which determines the increment between each index for slicing

# 1 : pallindrome
# 0 : nope
import test_pallindrome


def isPalindrome(mainStr):
    reversedStr = mainStr[::-1]

    if mainStr == reversedStr:
        return 1
    else:
        return 0

