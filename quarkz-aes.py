import random
import sys
import json
import decimal
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import number
from Crypto.PublicKey import RSA 
from decimal import Decimal

def gcd(a, b): 
   while a != 0:
      a, b = b % a, a
   return b

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modInverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

decimal.getcontext().prec=10000

p = number.getPrime(4096)
q = number.getPrime(4096)
n = Decimal(p*q)
phi = Decimal((p-1)*(q-1))
while True:
    e = Decimal(number.getPrime(12))
    r = gcd(int(e), int(phi))
    if r == 1:
        break

d = Decimal(modInverse(int(e), int(phi)))

m = Decimal(24)

s = m**e

t = random.randint(1, 8000)


k = n

ksize = sys.getsizeof(k)

kb = int(k).to_bytes(ksize, "big")

key = get_random_bytes(32)
cipher = AES.new(key, AES.MODE_CTR)
ct_bytes = cipher.encrypt(kb)
o = int.from_bytes(ct_bytes, "big")
nonce = b64encode(cipher.nonce).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
#    result = json.dumps({'nonce':nonce, 'ciphertext':ct})

#o = k^t

diff = abs(k-Decimal(o)) % n

#print (diff)

if diff > 0:
    pub = n/diff
else:
    u = random.randint(0, 1000)
    o -= u
    diff = abs(k-o) % n
    pub = n/diff

#    print ("pub: ", pub)
#    print ("diff: ", diff)

count = Decimal(int(s)//int(o))

#    print("count: ", count)

priv = round((Decimal(count)%Decimal(pub))*diff)

#    print ("middle: ", count%pub)
#    print ("priv: ", priv)
c = pow(m, e, o)

#    print ("c: ", c)

plain = pow((int(c)+int(priv)), int(d), int(n))
print (c)
print (s)
print (o)
print (plain)
plain2 = pow((int(c)-int(priv)), int(d), int(n))

#    if plain == m:
#
#        print("index: ", i)
#        print("something cool: ", (count%pub)*diff)
#        #print ("plain: ", plain)
#        #print ("cipher: ", c)
#        #print ("s: ", s)
#        #print ("k: ", k)
#        #print ("o: ", o)
#        #print ("diff: ", diff)
#        #print ("pub: ", pub)
#        #print ("count: ", count)
#        #print ("priv: ", priv)
#
#    
#    elif plain2 == m:
#
#        print ("==========================================")
#        print("index: ", i)
#        print("something cool: ", (count%pub)*diff)
#        print ("plain: ", plain2)
#        print ("cipher: ", c)
#        print ("s: ", s)
#        print ("k: ", k)
#        print ("o: ", o)
#        print ("diff: ", diff)
#        print ("pub: ", pub)
#        print ("count: ", count)
#        print ("priv: ", priv)
#        print ("*******************************************8")

if plain != m:
    print ("ERROR!!")