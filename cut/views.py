from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .forms import UserUrlInput
from .models import UrlModels
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def aftercut(request):
    error = ""
    link = ""
    first_char = ""
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
                        return render(
                                request ,
                                'after.html' , 
                                {
                                    'link' : link ,
                                    'error': error ,
                                    'base' : address ,
                                    'view' : sample_address.visited
                                }
                                    )

                url2 = url.replace('https://' , 'http://')
                for sample_address in all_addresses:
                    if  sample_address.url_before_cut == url2  :
                        link = sample_address.url_after_cut
                        return render(
                            request , 
                            'after.html' , 
                            {
                                'link' : link , 
                                'error': error , 
                                'base' : address , 
                                'view' : sample_address.visited
                            }
                                )


            elif url.startswith('http://'):
                for sample_address in all_addresses:
                    if  sample_address.url_before_cut == url  :
                        link = sample_address.url_after_cut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : sample_address.visited})
                url2 = url.replace('http://' , 'https://')
                for sample_address in all_addresses:
                    if  sample_address.url_before_cut == url2  :
                        link = sample_address.url_after_cut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : sample_address.visited})
            else:
                for sample_address in all_addresses:
                    if sample_address.url_before_cut == 'http://' + url or sample_address.url_before_cut == 'https://' + url :
                        link = sample_address.url_after_cut
                        return render(request , 'after.html' , {'link' : link , 'error': error , 'base' : address , 'view' : sample_address.visited})
            
            if( url.startswith('http://') or  url.startswith('https://')): 
                link = url 
                first_char = url[9]   
            else:
                link = "http://" + url
                first_char = url[0]
            set = UrlModels.objects.create(url_before_cut = link , visited = 0 , url_after_cut = first_char+str(count+1))
            set.save()
        link =  first_char+str(count+1)
    arg = {'link' : link , 'error': error , 'base' : address , 'view' : 'refresh to see'}
    return render(request , 'after.html' , arg)

def beforcut(request):
    form = UserUrlInput()
    arg = {'form' : form}
    return render(request , 'before.html' , arg)

def rd(request , number):
    
    this_url = get_object_or_404(UrlModels, url_after_cut = number)
    
    this_url.visited = this_url.visited + 1
    this_url.save()
    return redirect(this_url.url_before_cut)


@login_required
def all(request):
    all = UrlModels.objects.all()
    arg = {'all' : all}
    return render(request , 'all.html' , arg)

