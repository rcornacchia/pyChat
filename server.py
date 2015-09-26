# Read list of username-password combinations
with open ("user_pass.txt", "r") as authFile:
    combos = authFile.read()

print combos

print 'xxxxxxxxxxxxx'

slices = combos.split('\n')

print combos

print 'xxxxxxxxxxxxxxxx'

# clean slices
print slices

print 'xxxxxxxxxxxxx'

# Create dictionary for usernames/password combos
userDict = {}
myList = []
for i in slices:
        if i != '':
                print i
                myList = i.split(' ')
                userDict = dict(myList)
                print myList

print 'xxxxxxxxxxxxx'

print myList

print 'xxxxxxxxxxxxx'

userDict = dict(myList)
print userDict
