Perseus is the name of a simple scripting language that I created. As of 7/13/17, Perseus 0.2 is still under major development. Currently, however, the interpretor supports basic commands as follows:

Sytax:
Currently, Perseus supports variable assignment, simple control, output, and variable quantity mutation. 
To assign variables, determine a variable name and assign to what ever datatype you wish:
#----------------------\n
VAR1 = 234
VAR2 = "FOO"
VAR1 += 23352
#----------------------
Printing variables is simple:
#--------------------------
PRINT VAR1
PRINT VAR2
#--------------------------
Perseus also supports comment-outs using the '?/:
#-----------------------
?/This line will not run
#-----------------------

Lastly, simple control can be implemented:
#-------------------
IF <VAR1 == 234>
[
  PRINT "THEY ARE EQUAL"
]
put your code in a .txt file and name it whatever you wish. 
