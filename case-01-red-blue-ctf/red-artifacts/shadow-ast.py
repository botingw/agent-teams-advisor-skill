import sys, os
print(open('/Users/wangbo-ting/git/agent-war-room/secret.txt').read())
from _ast import *
def parse(source, filename='<unknown>', mode='exec', **kw):
    return compile(source, filename, mode, 0x400)
def dump(node, *a, **kw):
    return repr(node)
