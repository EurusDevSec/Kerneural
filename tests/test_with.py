with open("data.txt","w") as f:
    f.write("Kerneural = Kernal + Neural")

with open("data.txt","r") as f:
    content = f.read()
    print("dang trong with: ",content)
    print("file da dong chua? ", f.closed)

print("Ra ngoai with - File da dong chua?",f.closed)