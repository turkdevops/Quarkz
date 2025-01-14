from Crypto.Util import number
from decimal import Decimal
import decimal
from quarkz.dtypes import KeyPair
import random
import sys
import binascii


#decimal.getcontext().prec=5000

def gcd(a, b):
   while a != 0:
      a, b = b % a, a
   return b

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

def modpow(x,n,m):
  if n == 0:
    return 1
  elif n == 1:
    return x
  elif n%2 == 0:
    return modpow(x*(x%m),n/2,m)%m
  elif n%2 == 1:
    return (x *  modpow(x*(x%m),(n-1)/2,m)%m )%m

#Used to convert ascii text to integer.
def convert_to_int(data: str) -> int: 
    return int.from_bytes(data.encode(), 'big')

#Used to convert integer back to ascii string.
def convert_to_str(data: int) -> str:
    return data.to_bytes((data.bit_length() + 7) // 8, 'big').decode()

#Create a Quarkz keypair.
def createKey(keysize: int = 256):
    decimal.getcontext().prec=(keysize * 10)
    # 1.2.2   Generating n From Two Primes (Private Key)
    p = number.getPrime(keysize)
    q = number.getPrime(keysize)
    n = Decimal(p*q)
    phi = Decimal((p-1)*(q-1))
    while True:
        # 1.2.3   Generating e Using phi(n) (Public Key)
        e = 65537
        r = gcd(int(e), int(phi))
        if r == 1:
            t = Decimal(random.getrandbits(4))
            # 1.2.4   Generating o From e (Public Key)
            o = 1
            break

    # 1.2.5   Generating d using e and n (Private Key)
    d = Decimal(mod_inverse(int(e), int(phi)))

    print (e)

    x = Decimal(random.getrandbits(256))

    y = Decimal(random.getrandbits(256))

    # 1.2.6   Finding the Difference Between o and n (Private Key)
    diff = (abs(n-Decimal(o))) % n

    # 1.2.7   Salting n and diff (Internal Modifications)
    nSalted = n*(diff*x)

    diffSalted = (abs(nSalted-Decimal(o))) % nSalted

    # 1.2.8   Generating a Ratio Using nSalted and diffSalted (Public Key)
    ratio = ((nSalted*(diffSalted*y))/(diffSalted))

    # if diff > 0:
        #ratio = ((n/diff)%1)+1
        #print ("ratio: ", sys.getsizeof(round(ratio))*8)
    # else:
    #     u = random.randint(0, 1000)
    #     o -= u
    #     diff = abs(n-o) % n
    #     ratio = ((nSalted*(diffSalted*y))//(diffSalted))

    privateKey = {
        "d": d,
        "n": n,
        "diff": diff,
    }

    print ("private: ", sys.getsizeof(privateKey["d"]) + sys.getsizeof(privateKey["n"] + sys.getsizeof(privateKey["diff"])))

    publicKey = {
        "e": e,
        "o": o,
        "ratio": ratio,
    }

    print ("public: ", sys.getsizeof(publicKey["e"]) + sys.getsizeof(publicKey["o"]) + sys.getsizeof(publicKey["ratio"]))

    keyPair = {
        "private_key": privateKey,
        "public_key": publicKey
    }

    return KeyPair(**keyPair)
