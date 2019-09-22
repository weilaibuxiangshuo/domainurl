from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.shortcuts import redirect,render
from .models import (NewUser)
class permiss_filter(MiddlewareMixin):
    def process_request(self,request):
        if request.user in NewUser.objects.only("username"):
            print(request.path,request.method,"method")
            userurl=cache.get('userurl')
            is_bool=None
            for h in userurl:
                # print(h['url'],h['method'],'组合')
                if request.path == h['url'] and request.method == h['method']:
                    is_bool=True
            print(is_bool,'is_bool')
            if not is_bool:
                print('eeee')
                # return redirect('/nopermiss/')
                return render(request,'nopermiss.html')
        else:
            pass
