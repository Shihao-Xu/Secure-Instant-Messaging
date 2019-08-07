# python 2.7
#coding:utf-8
import sys
import os
import random
import binascii


#check primality by MillerRabin
def MillerRabin(n):
    m=n-1
    k=0
    while(m%2==0):
        m=m//2
        k=k+1
    a=random.randint(2,n)
    #b=a**m%n
    b = cipher_text(a,m,n)
    if(b==1):
        return 1
    for i in range(k):
        if(b==n-1):
            return 1
        else:
            b=b*b%n
    return 0
#cipher= m^e mod n  text = c^d mod n
def cipher_text(b,n,m):
    
        a=1
        #x=b;y=n;z=m
        binstr = bin(n)[2:][::-1]       #cut Heading 0b，get the following. 
        for item in binstr:
                if item == '1':
                        a = (a*b)%m
                        b = (b**2)%m
                elif item == '0':
                        b = (b**2)%m
        return a
# calculate d,d*e mod _n =1
def findModReverse(e,m):# findModReverse

    if gcd(e,m)!=1:
        return None
    u1,u2,u3 = 1,0,e
    v1,v2,v3 = 0,1,m
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1%m

# get a random large prime            
def randomLargePrime():
        Min = 10**11;Max = 10**15;p = 0
        while(1):
                p = random.randrange(Min,Max,1)
                for i in range(20):
                        if MillerRabin(p)==0:
                                break
                        elif i==19:
                                return p
# function can write data into txt files                        
def dataWrite(foldername,filename,message):
        folder = os.getcwd() +'/'+'Key'+'/'+ foldername
         
        if not os.path.exists(folder):
               os.makedirs(folder,0o700)

        writer = open(folder+'/'+filename,'w')
        writer.write(message)
        writer.close()
        return 0
#gcd 
def     gcd(a,b):
        while a!=0:
            a,b = b%a,a
        return b

# build public_private key pair
def Build_key(foldername):
        p = randomLargePrime()
        q = randomLargePrime()
        n = p*q
        _n = (p-1)*(q-1)    #n Euler's function
        e = 0
        while(1):
                e = random.randint(1,_n+1)
                if gcd(e,_n)==1:
                        break
        d = findModReverse(e,_n)
        #save keys 
        dataWrite(foldername,'p.txt',str(hex(p))[2:-1])
        dataWrite(foldername,'q.txt',str(hex(q))[2:-1])
        dataWrite(foldername,'n.txt',str(hex(n))[2:-1])
        dataWrite(foldername,'e.txt',str(hex(e))[2:-1])
        dataWrite(foldername,'d.txt',str(hex(d))[2:-1])
        return str(hex(n))[2:]+'/'+str(hex(e))[2:-1]+'/'+str(hex(d))[2:]
#ascii_to_hex
def ascii2Hex(raw_str):
        hex_str = ''
        for ch in raw_str:
                hex_str += hex(ord(ch))[2:]
        return hex_str

#hex_to_ascii
def hex2Ascii(raw_str):
        asc_str = ''
        for i in range(0,len(raw_str),2):
                asc_str += chr(int(raw_str[i:i+2],16))
        return asc_str
#encrypt，need public or private key
def encrypt(m,key):
        Key=key.split('/')
        n=int(Key[0].rstrip('L'),16)
        e=int(Key[1].rstrip('L'),16)
        cipher = ""
        nlength = len(str(hex(n))[2:])  #calculate length of hex(n),for grouping
        message = m             #read in plaintext
        for i in range(0,len(message),8):
            if i==len(message)//8*8:
                m = int(ascii2Hex(message[i:]),16)  #the last group
            m = int(ascii2Hex(message[i:i+8]),16)
            c = cipher_text(m,e,n)
            cipher1 = str(hex(c))[2:-1]
            if len(cipher1)!=nlength:
                cipher1 = '0'*(nlength-len(cipher1))+cipher1    #fill 0
            cipher += cipher1
        return cipher
#decrypt，need public or private key
def decrypt(c,key):
        #after encrypted,length ofeach group
        # equal to length of n
        Key=key.split('/')
        n=int(Key[0].rstrip('L'),16)
        d=int(Key[1].rstrip('L'),16)
        cipher = c
        message = ""
        nlength = len(str(hex(n))[2:])
        for i in range(0,len(cipher),nlength):
            c = int(cipher[i:i+nlength],16)  
            m = cipher_text(c,d,n)
            info = hex2Ascii(str(hex(m))[2:-1])
            message += info
        return message

    