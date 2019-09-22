from django.core.cache import cache
from domain.models import (NewUser)
import math

#分页
class pagination:
    def __init__(self,*args,**kwargs):
        self.args=args[0]
        self.total=args[0].count()
        self.data=args[1]
        self.page=0
        self.limit=0

    def control(self):
        try:
            self.page=int(self.data.GET['page'])
            self.limit=int(self.data.GET['limit'])
        except:
            return None
        if self.page>math.ceil(self.total/self.limit) or self.limit > self.total:
            self.page=1
        slice=self.args[(self.page-1)*self.limit:self.page*self.limit]
        return slice


#获取及更新权限
class updatapermiss:
    user_url=[]

    @classmethod
    def initialize(cls,request):
        """获取用户所有权限url"""
        res = NewUser.objects.prefetch_related("role_user__relationpermiss").filter(
            username=request.user.username).first()
        for line in res.role_user.first().relationpermiss.all():
            linedict = {
                "url": line.nameurl,
                "method": line.namemethod
            }
            cls.user_url.append(linedict)
        public_url = ['/index/', '/logout/', '/welcome/', '/login/', '/nopermiss/']
        public_list = [{"url": n, "method": "GET"} for n in public_url]
        cls.user_url.extend(public_list)
        print(cls.user_url)
        cache.set("userurl", cls.user_url, None)