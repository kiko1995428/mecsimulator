dl =[]
while True:
    data = input("input num: ")
    data = int(data)
    dl.add = data
    if data == 0:
        break
dlleng = len(dl)
j = 0
w = 0
s = 0
for i in range(0, dlleng):
    w += i
    s += i * j
    j += 1

print(s/w)