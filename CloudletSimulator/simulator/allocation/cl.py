dl =[]
while True:
    data = input("input num: ")
    data = int(data)
    dl.append(data)
    if data == 0:
        break
print(dl)
dlleng = len(dl)
print(dlleng)
j = 0
w = 0
s = 0
for i in dl:
    w += i
    s += i * j
    j += 1

print(s/w)