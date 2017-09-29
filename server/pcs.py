from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from urllib import parse
import json
import rsa
import base64

@csrf_exempt
def pcs_rsa(request):
    if request.method=="POST":
        print("body is " + str(request.body));
        jdata=parse.parse_qs(str(request.body));
        pubkey=jdata["pubkey"][0]
        password=jdata["password"][0]
        print("pubkey %s password %s"%(pubkey, password))
        key=rsa.PublicKey.load_pkcs1_openssl_pem(pubkey)
        password_rsaed=base64.b64encode(rsa.encrypt(password.encode('utf-8'), key))
        output={"success":True, "password_rsaed": password_rsaed}
        return HttpResponse(json.dumps(output))
    else:
        output={"success":False}
        return HttpResponse(json.dumps(output))

def sign2_func(j, r):
    a = []
    p = []
    o = ''
    v = len(j)

    for q in range(256):
        a.append(ord(j[q % v]))
        p.append(q)

    u = 0
    for q in range(256):
        u = (u + p[q] + a[q]) % 256
        t = p[q]
        p[q] = p[u]
        p[u] = t

    i = 0
    u = 0
    for q in range(len(r)):
        i = (i + 1) % 256
        u = (u + p[i]) % 256
        t = p[i]
        p[i] = p[u]
        p[u] = t
        k = p[((p[i] + p[u]) % 256)]
        o += chr(ord(r[q]) ^ k)

    return base64.b64encode(o)

def pcs_sign2(request):
    sign3=request.GET["sign3"]
    sign1=request.GET["sign1"]
    if sign1!=None and sign3!=None:
        sign2_result=sign2_func(sign3, sign1)
        output={"success":True, "sign2": sign2_result}
        return HttpResponse(json.dumps(output))
    else:
        output={"success":False, "message":"sign3 or sign1 not found"}
        return HttpResponse(json.dumps(output))
