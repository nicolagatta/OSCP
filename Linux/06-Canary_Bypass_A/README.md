# The main requirement that makes it possible to exploit it is 
# The buffer 
# receive user data  (gets())
# prints it (print())
# receive additional user data (gets())

# The exploitation leverage this to
# use the first user input for a format string 
# use the print to leak the value of the canary
# prepare a second paylad for the second gets()