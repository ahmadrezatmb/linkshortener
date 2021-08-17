from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserUrlInput
from .models import UrlModels
from django.shortcuts import get_object_or_404


def aftercut(request):
    error = ""
    link = ""
    firstchar = ""
    address = request.build_absolute_uri('/')
    all_addresses = UrlModels.objects.all()
    count = all_addresses.count()
    if request.method == "POST":
        form = UserUrlInput(request.POST)
        if form.is_valid():
            url = form.cleaned_data['address']
            # check if link is given before or not :
            
            if  url.startswith('https://'):
                for sample_address in all_addresses:
                    if  sample_address.url_before_cut == url  :
                        link = sample_address.url_after_cut
                        return render(request ,
                                     'after.html' , 
                                     {
                                         'link' : link ,
                                         'error': error ,
                                         'base' : address ,
                                         'view' : sample_address.visited
                                     }
                                     )
                                     
                url2 = url.replace('https://' , 'http://')
                for ad in all_addresses:
                    if  ad.url_before_cut == url2  :
                        link = ad.url_after_cut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
            elif url.startswith('http://'):
                
                for ad in all_addresses:
                    if  ad.url_before_cut == url  :
                        link = ad.url_after_cut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
                url2 = url.replace('http://' , 'https://')
                for ad in all_addresses:
                    if  ad.url_before_cut == url2  :
                        link = ad.url_after_cut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
            else:
                for ad in all_addresses:
                    if ad.url_before_cut == 'http://' + url or ad.url_before_cut == 'https://' + url :
                        link = ad.url_after_cut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : ad.visited})
            if("https://" in url or "http://" in url):
                if(len(url) >=4):
                    if url[0:4] == "http" :
                        link = url 
                        firstchar = url[9]   
            else:
                link = "http://" + url
                firstchar = url[0]
            set = UrlModels.objects.create(url_before_cut = link , visited = 0 , url_after_cut = firstchar+str(count+1))
            set.save()
        link =  firstchar+str(count+1)
    arg = {'link' : link , 'error': error , 'base' : address , 'view' : 'refresh to see'}
    return render(request , 'after.html' , arg)

def beforcut(request):
    form = UserUrlInput()
    arg = {'form' : form}
    return render(request , 'before.html' , arg)

def rd(request , number):
    
        #hadaf = UrlModels.objects.get(url_after_cut = number)
    hadaf = get_object_or_404(UrlModels, url_after_cut = number)
    
    hadaf.visited = hadaf.visited + 1
    hadaf.save()
    return redirect(hadaf.url_before_cut)
def all(request):
    all = UrlModels.objects.all()
    arg = {'all' : all}
    return render(request , 'all.html' , arg)

