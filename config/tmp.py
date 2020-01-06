import json,time

def xx():
    s=1

    while(1):
        s = s+1
        if s == 5:
            return 123
        print(s)
        time.sleep(1)

print(xx())