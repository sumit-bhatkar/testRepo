"""
This is a comment
written in
more than just one line
"""
# this is also a comment

print ("Hello World")
print ("Hello Sumit - made changes")

if 5 > 2:
   print("Five is greater than two!") 

x = 4 # x is of type int
x = "MasterBlaster" # x is now of type str
print(x)

# Using functions for different tests

def testArgumants(intval1,intval2,intval3 , listval):
    print("=====================")
    log = "started {} {} {}"
    print(log.format(intval1,intval2,intval3))
    intval1 += 1  # value doesnt change outside
    intval2 += 1
    intval3 += 1
    print(log.format(intval1,intval2,intval3))
    
    
    print(log.format(listval[0],"","")) # value changes outside
    listval[0] += 1
    print(log.format(listval[0],"",""))
    print("=====================")
    return intval2,intval3

print("=========Use of function============")

x = y = z = 5
mylist = [5,"name"]
y,z=testArgumants(x,y,z,mylist) 
print (x,y,z)

print (mylist)

print (list(filter(lambda x: x % 2 == 0, range(16))))
print ([x for x in range(16) if x % 2 == 0])

print("=========Use of Class and class function============")

class Person:
  sal = "11"
  def __init__(self, name, age):
    self.name = name
    self.age = age
    self.sal = "    10"

  def myfunc(self):
    print("Hello my name is " + self.name + self.sal)

p1 = Person("Sumit", 36)
p1.myfunc()

print("=====================")

