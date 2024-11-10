import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def generate_key():
    key = random.getrandbits(56)  
    return key