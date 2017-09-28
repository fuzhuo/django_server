from django.http import HttpResponse
def hello(request):
    if request.method=="POST":
        i = request.POST.get('pubkey')
        return HttpResponse("Hello world ! "+i)
    else:
        return HttpResponse("Hello world ! ")
