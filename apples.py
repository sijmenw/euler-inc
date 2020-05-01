# created by Sijmen van der Willik
# 24/05/2018 13:33
#
# in this puzzle you have two baskets of apples
# each basket has a number of poisoned apples
#
# you have to eat n1 apples if you choose b1, and n2 if you choose b2
# you have to eat at least m apples to die

from itertools import permutations


# 0 = regular, 1 = poisoned
b1 = (0, 0, 0, 1, 1)
b2 = (0, 0, 1, 1, 1)

n1 = 3
n2 = 2

m = 2

# counts of death
count_d1 = 0
count_d2 = 0

for i in permutations(b1):
    if sum(i[:n1]) >= m:
        count_d1 += 1

for i in permutations(b2):
    if sum(i[:n2]) >= m:
        count_d2 += 1

print(count_d1)
print(count_d2)
