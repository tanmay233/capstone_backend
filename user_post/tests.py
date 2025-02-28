from django.test import TestCase

# Create your tests here.
def solve(input1,input2, input3):
    input1.sort()
    res = 0
    x = 0
    for i in input1:
        x+=i
        if x > input2:
            break
        res +=1
    return res