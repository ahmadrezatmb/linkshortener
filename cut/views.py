from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect,render
from .forms import UserUrlInput
from .models import UrlModels
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# form handling to cut the link !
def aftercut(request):
    error_message = ''
    link = ''
    first_char = ''
    all_addresses = UrlModels.objects.all()
    count = all_addresses.count()
    if request.method == 'POST':
        form = UserUrlInput(request.POST)
        if form.is_valid():
            url = form.cleaned_data['address']
            # check if link is given before or not :
            
            if  url.startswith('https://'):
                this_url_in_db = UrlModels.objects.filter(url_before_cut=url)
                if this_url_in_db.count() != 0 :
                    context = {
                        'link' : link,
                        'error_message': error_message,
                        'view' : this_url_in_db.get().number_of_visitors
                    }
                    return render(
                                request,
                                'after.html',
                                context
                                )
       
                url2 = url.replace('https://','http://')
                this_url_in_db = UrlModels.objects.filter(url_before_cut=url2)
                if this_url_in_db.count() != 0 :
                    context = {
                        'link' : link,
                        'error_message': error_message,
                        'view' : this_url_in_db.get().number_of_visitors
                    }
                    return render(
                                request,
                                'after.html',
                                context
                                )


            elif url.startswith('http://'):
                this_url_in_db = UrlModels.objects.filter(url_before_cut=url)
                if this_url_in_db.count() != 0 :
                    context = {
                        'link' : link,
                        'error_message': error_message,
                        'view' : this_url_in_db.get().number_of_visitors
                    }
                    return render(
                                request,
                                'after.html',
                                context
                                )
                url2 = url.replace('http://', 'https://')
                this_url_in_db = UrlModels.objects.filter(url_before_cut=url)
                if this_url_in_db.count() != 0 :
                    context = {
                        'link' : link,
                        'error_message': error_message,
                        'view' : this_url_in_db.get().number_of_visitors
                    }
                    return render(
                                request,
                                'after.html',
                                context
                                )
            else:
                for sample_address in all_addresses:
                    if (sample_address.url_before_cut == 'http://' + url or 
                        sample_address.url_before_cut == 'https://' + url) :
                        # if there is https or http in link
                        link = sample_address.url_after_cut
                        return render(
                                    request, 
                                    'after.html', 
                                    {
                                        'link' : link, 
                                        'error_message': error_message, 
                                        'view' : sample_address.number_of_visitors
                                    })

            if( url.startswith('http://') or url.startswith('https://')): 
                link = url 
                first_char = url[9]   
            else:
                link = 'http://' + url
                first_char = url[0]
            set = UrlModels.objects.create(
                            url_before_cut = link, 
                            number_of_visitors = 0, 
                            url_after_cut = first_char+str(count+1))
            
            set.save()
        link = first_char+str(count+1)
    arg = {
        'link' : link, 
        'error_message': error_message, 
        'view' : 'refresh to see'
        }
    return render(request, 'after.html', arg)


# rendering the form
def beforcut(request):
    form = UserUrlInput()
    arg = {'form' : form }
    return render(request, 'before.html',arg)


# redirecting after this view was requested
def rd(request, number):
    
    this_url = get_object_or_404(UrlModels, url_after_cut = number)
    
    this_url.number_of_visitors = this_url.number_of_visitors + 1
    this_url.save()
    return redirect(this_url.url_before_cut)


# DEBUG: just to see all attempts
@login_required
def all(request):
    all = UrlModels.objects.all()
    arg = {'all' : all}
    return render(request, 'all.html', arg)

