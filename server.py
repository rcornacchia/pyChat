# Read list of username-password combinations
f = open ("user_pass.txt", "r")
combos = f.read()
f.close()

# split by lines
slices = combos.split('\n')

# Create dictionary for usernames/password combos
users = {}
for i in slices:
        if i != '':
                key, val = i.split(' ')
                users[key] = val
print users
