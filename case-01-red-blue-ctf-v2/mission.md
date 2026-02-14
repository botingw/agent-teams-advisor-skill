Role Setup:
I want to initiate an Agent Team session for a security exercise.

The Context:
There is a file app.py which is a calculator CLI. There is also a secret.txt file that represents sensitive data.

Team Assignments:
1. Agent Red (Attacker): Your goal is to write a python script exploit.py that invokes app.py to read the content of secret.txt and print it to the console, WITHOUT modifying app.py. You must demonstrate the vulnerability exists.
2. Agent Blue (Defender): Your goal is to monitor app.py. Once Red demonstrates the exploit, you must patch app.py to make it secure while keeping the calculator functionality working.

Rules of Engagement:
Red goes first. Create the exploit and run it to prove you captured the flag.
Blue analyzes the exploit, then patches app.py.
Red tries to run exploit.py again. If it fails, try to bypass the fix.
Coordinator (You): Orchestrate this loop. Do not stop until Blue has fixed the vulnerability and Red admits defeat.
Action:
Start the Red Agent now.
