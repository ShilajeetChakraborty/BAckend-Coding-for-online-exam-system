import random
import string


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def textForNotPallindrome():
    notPallindromeList = []
    for each in range(0, 5):
        randomLength = random.randint(0, 20)
        notPlalindromeStr = randomString(randomLength)
        notPallindromeList.append(notPlalindromeStr)
    return notPallindromeList


def textPallindrome():
    return ["redivider", "deified", "radar", "level", "a"]


def testCasesForPallindrome():
    nPallindrome = textForNotPallindrome()
    pallindrome = textPallindrome()
    finalList = nPallindrome + pallindrome
    return finalList
