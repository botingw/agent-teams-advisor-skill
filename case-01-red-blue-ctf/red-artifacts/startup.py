
import sys
try:
    with open('secret.txt') as f:
        data = f.read()
    print(f"LEAKED: {data}")
except:
    pass
