# python 2.7

import DES
import hashlib
import RSA

def md5(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

def encryptData(text,private_key,peer_public):
    # des encrypt message
    key=DES.generatekey()
    text= DES.modifytext(text)
    d=DES.des()
    desEndata=d.encrypt(key,text)
    print desEndata
    desEndata = "".join(str(e) for e in desEndata) 
    # hash message and signiture
    hashAndSign=RSA.encrypt(md5(text),private_key)
    # encrypted des key and signed message with the other client public_key
    middleData=key+'/'+hashAndSign
    data2=RSA.encrypt(middleData,peer_public)
    #combine data2 and desEndata
    data=desEndata+'/'+data2
    return data

def decryptData(cipher,private_key,peer_public):
    cipher = cipher.split('/')
    try:    
        #get des key and hashed message
        middleData=RSA.decrypt(cipher[1],private_key)
        key=middleData.split('/')[0]
        hashAndSign=middleData.split('/')[1]
        #decrypt signed message to get hash
        hashData=RSA.decrypt(hashAndSign,peer_public)
    except:
          return'you are not a trusted user, you are prohibited see the message'
    
    #des decrypt
    d=DES.des()
    descipher=list(cipher[0])
    descipher=bit_array_to_string(descipher)
    desDedata=d.decrypt(key,descipher)
    desDedata=bit_array_to_string(desDedata)
    #hash 
    #md5(desDedata)
    if hashData==md5(desDedata):
		return desDedata.rstrip('#')
    else:
		return 'failed on decipher, your system is under an attack'
    

def nsplit(s, n):#Split a list into sublists of size "n"
    return [s[k:k+n] for k in xrange(0, len(s), n)]

def bit_array_to_string(array): #Recreate the string from the bit array
    res = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in bytes]) for bytes in  nsplit(array,8)]])   
    return res
