import pickle

code6 = {}
code8 = {}

with open ('X_code_6.pkl', 'rb') as f:
    X_code_6 = pickle.load(f)
with open ('O_code_6.pkl', 'rb') as f:
    O_code_6 = pickle.load(f)
with open ('X_code_8.pkl', 'rb') as f:
    X_code_8 = pickle.load(f)
with open ('O_code_8.pkl', 'rb') as f:
    O_code_8 = pickle.load(f)

for state in X_code_6:
    code6[state] = X_code_6[state]
for state in O_code_6:
    code6[state] = O_code_6[state]
for state in X_code_8:
    code8[state] = X_code_8[state]
for state in O_code_8:
    code8[state] = O_code_8[state]

print(code6)
print()
print(code8)

pickle.dump(code6,open('code6.pkl', 'wb'))
pickle.dump(code8,open('code8.pkl', 'wb'))
