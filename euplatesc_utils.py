import hmac
import uuid
import codecs
from time import strftime
from urllib.parse import urlencode


def hmacmd5(key, data):
    blocksize=64
    #pad key as per requirement of hmac algorithm with blocksize using bytes b'\0'
    key=key.ljust(blocksize, b"\0")
    #encode data to unicode 8 bit
    return hmac.new(key,data.encode('utf-8')).hexdigest().upper()

def euplatesc_mac(key,params):
    data=""
    for p in params:
        if len(p)==0:
            data+="-"
        else:
            data+=str(len(p))+p
    #call hmacmd5 by converting to hex bytes object
    return hmacmd5(codecs.decode(key,"hex"),data)


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
    params['order_desc'],
    params['merch_id'],
    params['timestamp'],
    params['nonce']
]

params['fp_hash']=euplatesc_mac(key,oparam)

print(params['fp_hash'])
#now show the customer the form
#<form method="POST" action="https://secure.euplatesc.ro/tdsprocess/tranzactd.php">
#print the inputs with the values from the var params
#</form>
print("https://secure.euplatesc.ro/tdsprocess/tranzactd.php?"+urlencode(params))
