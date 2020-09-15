from string import ascii_uppercase

ALPHA = list(ascii_uppercase)

r = [l for l in 'BDFHJLCPRTXVZNYEIWGAKMUSQO']
position = 1
rotersetting = 1

temp = position - rotersetting

print(ALPHA[(ALPHA.index(r[(ALPHA.index('A') + temp) % 26]) - temp) % 26])
