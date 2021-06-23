from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import userurl
from .models import urlsdatabase
from django.shortcuts import get_object_or_404


def aftercut(request):
    error = ""
    link = ""
    firstchar = ""
    address = request.build_absolute_uri('/')
    obj = urlsdatabase.objects.all()
    count = obj.count()
    if request.method == "POST":
        form = userurl(request.POST)
        if form.is_valid():
            url = form.cleaned_data['address']
            # check if link is given before or not :
            
            if 'https://' in url:
                for ad in obj:
                    if  ad.urlbeforecut == url  :
                        link = ad.urlaftercut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
                url2 = url.replace('https://' , 'http://')
                for ad in obj:
                    if  ad.urlbeforecut == url2  :
                        link = ad.urlaftercut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
            elif 'http://' in url:
                
                for ad in obj:
                    if  ad.urlbeforecut == url  :
                        link = ad.urlaftercut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
                url2 = url.replace('http://' , 'https://')
                for ad in obj:
                    if  ad.urlbeforecut == url2  :
                        link = ad.urlaftercut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
            else:
                for ad in obj:
                    if ad.urlbeforecut == 'http://' + url or ad.urlbeforecut == 'https://' + url :
                        link = ad.urlaftercut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
            if("https://" in url or "http://" in url):
                if(len(url) >=4):
                    if url[0:4] == "http" :
                        link = url 
                        firstchar = url[9]   
            else:
                link = "http://" + url
                firstchar = url[0]
            set = urlsdatabase.objects.create(urlbeforecut = link , visited = 0 , urlaftercut = firstchar+str(count+1))
            set.save()
        link =  firstchar+str(count+1)
    arg = {'link' : link , 'error': error , 'base' : address , 'view' : 'refresh to see'}
    return render(request , 'after.html' , arg)

def beforcut(request):
    form = userurl()
    arg = {'form' : form}
    return render(request , 'before.html' , arg)

def rd(request , number):
    
        #hadaf = urlsdatabase.objects.get(urlaftercut = number)
    hadaf = get_object_or_404(urlsdatabase, urlaftercut = number)
    
    hadaf.visited = hadaf.visited + 1
    hadaf.save()
    return redirect(hadaf.urlbeforecut)
def all(request):
    all = urlsdatabase.objects.all()
    arg = {'all' : all}
    return render(request , 'all.html' , arg)

