import hashlib
import uuid
from time import strftime

def hmacmd5(key, data):
    blocksize=64
    key=key.ljust(blocksize, "\0")
    ipad = chr(0x36)*blocksize
    opad = chr(0x5C)*blocksize
    p1 = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(key,opad))
    p2 = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(key,ipad))
    #create new hashlib md5 object
    m1 = hashlib.md5()
    m1.update(p2.encode('utf-8'))
    m1.update(data.encode('utf-8'))
    p3 = m1.digest()
    #create second hashlib md5 object
    m2 = hashlib.md5()
    m2.update(p1.encode('utf-8'))
    m2.update(p3)
    return m2.hexdigest().upper()


def euplatesc_mac(key,params):
    data=""
    for p in params:
        if len(p)==0:
            data+="-"
        else:
            data+=str(len(p))+p
    print(data)
    return hmacmd5(key.encode('utf-8').hex(),data)


key="00112233445566778899AABBCCDDEEFF"
mid="testaccount"

params={
    'amount':'10.20',
    'curr':'RON',
    'invoice_id':'123',
    'order_desc':'Test order',
    'merch_id':mid,
    'timestamp':strftime("%Y%m%d%H%M%S"),
    'nonce': uuid.uuid4().hex
}
oparam=[
    params['amount'],
    params['curr'],
    params['invoice_id'],
    params['merch_id'],
    params['order_desc'],
    params['timestamp'],
    params['nonce']
]

params['fp_hash']=euplatesc_mac(key,oparam)

params['fname']="test";
params['lname']="euplatesc"
params['email']="test@euplatesc.ro"
params['ExtraData[successurl]']="http://127.0.0.1:8000/payment/success"
