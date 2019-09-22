from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from .models import NewUser,Role,Permission,Menu
from django.http import JsonResponse,QueryDict
from django.db.models import Q
from django.contrib.auth import authenticate,logout,login
from .allforms import LoginForm
from django.core.cache import cache
import math,json
from domain.captcha.captcha import Captcha
from domain.system import (pagination,updatapermiss)


class CaptchaView(View):
    """获取图片验证码"""
    def get(self, request):
        text, img = Captcha.generate_captcha()
        print(text,'text')
        # 存入缓存中, 验证码有效期5分钟
        cache.set("captcha", text.lower(), 5 * 60)
        # 返回图片
        return HttpResponse(img, content_type='image/png')


class Login(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        obj = LoginForm(request.POST)
        if obj.is_valid():
            username=request.POST.get('username','')
            password=request.POST.get('password','')
            captcha=request.POST.get('captcha','')
            print(username,password)
            cache_captcha=cache.get("captcha")
            # NewUser.objects.create_user(username=username,password=password)
            user=authenticate(username=username,password=password)
            if user:
                if captcha==cache_captcha:
                    login(request,user)
                    # updata=updatapermiss()
                    # updata.initialize(request)
                    updatapermiss.initialize(request)


                    # user_url=[]
                    # """获取用户所有权限url"""
                    # res = NewUser.objects.prefetch_related("role_user__relationpermiss").filter(
                    #     username=user.username).first()
                    # for line in res.role_user.first().relationpermiss.all():
                    #     linedict={
                    #         "url":line.nameurl,
                    #         "method":line.namemethod
                    #     }
                    #     user_url.append(linedict)
                    # # print(user_url)
                    # public_url=['/index/','/logout/','/welcome/','/login/','/nopermiss/']
                    # public_list=[{"url":n,"method":"GET"} for n in public_url]
                    # user_url.extend(public_list)
                    # print(user_url)
                    # cache.set("userurl",user_url,None)
                    return redirect('/index/')
                else:
                    return render(request, 'login.html', {"msg": "验证码错误"})
            else:
                return render(request,'login.html',{"msg":"用户名或者密码错误"})
        else:
            # print(obj.errors['username'], '666')
            # obj.errors['username']="测试一下"
            # print(obj.errors['username'], '555')
            return render(request, 'login.html', {"form": obj})


class Index(View):
    def get(self,request):
        temp=Menu.objects.all()
        data=[]
        orderlist=[x.order for x in temp]
        orderlist.sort()
        tempdata=[]
        """菜单排序"""
        for t in orderlist:
            for h in temp:
                if t==h.order:
                    tempdata.append(h)
        for i in tempdata:
            dict={"menu":i.name,"submenu":i.permission_menu.all().order_by('id')}
            data.append(dict)
        return render(request,'index.html',{'data':data})

#管理员列表
class AdminUser(View):
    def get(self,request):
        roleshow=Role.objects.all()
        return render(request,'adminuser.html',{"data":roleshow})


#管理员数据
class AdminUserData(View):
    """用户表格渲染"""
    def get(self, request):
        searchdata = request.GET.get('search', [])
        if len(searchdata) != 0 and not isinstance(searchdata, list):
            temp = NewUser.objects.filter(username=searchdata)
        else:
            temp = NewUser.objects.all()
        dataPagination = pagination(temp, request)
        tempdata = dataPagination.control()
        if tempdata is None:
            return render(request, 'error.html')
        data = []
        for i in tempdata:
            dict = {"id": i.id, "username": i.username,"rolename":i.role_user.first().name,"roleid":i.role_user.first().id}
            data.append(dict)
        defaultData = {
            "code": 0,
            "msg": "",
            "count": temp.count(),
        }
        defaultData.update({"data": data})
        return JsonResponse(defaultData)

    """用户管理员"""
    def post(self,request):
        title1=request.POST.get('title1',[])
        title2=request.POST.get('title2',[])
        rolename=request.POST.get('rolename',[])
        roleone=Role.objects.filter(id=rolename).first()
        print(roleone,"role")
        if all([title1,title2]):
            temp=NewUser.objects.filter(username=title1).first()
            if temp is not None:
                temp.set_password(title2)
                temp.role_user.clear()
                temp.role_user.add(roleone)
                temp.save()
            else:
                createuser=NewUser.objects.create_user(username=title1,password=title2)
                createuser.role_user.add(roleone)
        return redirect('/adminuser/')

    """用户删除"""
    def delete(self,request):
        temp_del=QueryDict(request.body)
        _data=temp_del.get('data',[])
        if len(_data)!=0:
            for i in json.loads(_data):
                temp=NewUser.objects.filter(id=i['id'])
                temp.delete()
        return JsonResponse({'code':0})


#用户内嵌网页
class AdminUserIframe(View):
    def get(self,request):
        return render(request,'adminuseriframe.html')



#角色管理
class AdminRole(View):
    def get(self,request):
        return render(request, 'adminrole.html')


#角色内嵌网页
class AdminRoleIframe(View):
    def get(self,request):
        """渲染角色所有权限"""
        menulist=Menu.objects.all()
        # perlist=Permission.objects.filter(relationself=None)
        data=[]
        for i in menulist:
            i.permission_menu.all()
            subdata = []
            subid = []
            # print(i.permission_menu.all())
            for m in i.permission_menu.all():
                subdata.append(m)
                m.permission_self.all()
                # print(m.permission_self.all(),'m')
                for n in m.permission_self.all():
                    subdata.append(n)
            _dict={"menu":i,"submenu": subdata}
            data.append(_dict)
        # print(data)
        return render(request,'adminroleiframe.html',{"data":data})



#根据角色渲染权限
class AdminRoleSet(View):
    def get(self,request):
        """获取角色对应的权限"""
        title=request.GET.get('roleid',[])
        roleone=Role.objects.filter(id=title).first()
        # print(roleone,'userone')
        userid=[]
        # print(roleone.relationpermiss.all(),'有没有')
        for _i in roleone.relationpermiss.all():
            # print('kkkkkk')
            # print(_i.name)
            userid.append(_i.id)
        print(userid,'userid')
        return JsonResponse({'code':userid})



#角色权限设置
class AdminRoleEdit(View):
    def post(self,request):
        data=request.POST.get('data',[])
        print(data,"看一下")
        if len(data)!=0:
            data = json.loads(data)
            roledata = Role.objects.filter(id=data['id']).first()
            if roledata is not None:
                roledata.relationpermiss.clear()
                datalist=[]
                permissdata=Permission.objects.all()
                for i in permissdata:
                    if str(i.id) in data['data']:
                        datalist.append(i)
            print(datalist,"datalist")
            roledata.relationpermiss.set(datalist)
            """重新初始化权限关系"""
            updatapermiss.initialize(request)
        return JsonResponse({'code':0})



#角色数据渲染
class AdminRoleData(View):
    def get(self,request):
        searchdata=request.GET.get('search',[])
        # print(searchdata,'kk')
        if len(searchdata)!=0 and not isinstance(searchdata,list):
            temp=Role.objects.filter(name=searchdata)
        else:
            temp=Role.objects.all()
        dataPagination=pagination(temp,request)
        tempdata=dataPagination.control()
        if tempdata is None:
            return render(request,'error.html')
        data=[]
        for i in tempdata:
            dict={"id":i.id,"name":i.name}
            data.append(dict)
        defaultData={
            "code": 0,
            "msg": "",
            "count": temp.count(),
        }
        defaultData.update({"data":data})
        return JsonResponse(defaultData)

    def post(self,request):
        roleadd=request.POST.get('title1',[])
        # print(roleadd,"kk")
        if len(roleadd)!=0:
            title=Role.objects.filter(name=roleadd)
            if len(title)==0:
                Role.objects.all().create(name=roleadd)
        return redirect('/adminrole/')

    def delete(self,request):
        temp_del=QueryDict(request.body)
        _data=temp_del.get('data',[])
        if len(_data)!=0:
            for i in json.loads(_data):
                temp=Role.objects.filter(id=i['id'])
                temp.delete()
        return JsonResponse({'code':0})


#菜单分类
class AdminMenu(View):
    def get(self,request):
        return render(request,'adminmenu.html')

#菜单数据渲染
class AdminMenuData(View):
    def get(self,request):
        searchdata=request.GET.get('search',[])
        if len(searchdata)!=0 and not isinstance(searchdata,list):
            temp=Menu.objects.filter(name=searchdata)
        else:
            temp=Menu.objects.all()
        dataPagination=pagination(temp,request)
        tempdata=dataPagination.control()
        if tempdata is None:
            return render(request,'error.html')
        data=[]
        for i in tempdata:
            dict={"id":i.id,"name":i.name,"order":i.order}
            data.append(dict)
        defaultData={
            "code": 0,
            "msg": "",
            "count": temp.count(),
        }
        defaultData.update({"data":data})
        return JsonResponse(defaultData)

    def post(self,request):
        title1=request.POST.get('title1',[])
        title2=request.POST.get('title2',[])
        if all([title1,title2,str(title2).isnumeric()]):
            title=Menu.objects.filter(name=title1)
            if len(title)==0:
                Menu.objects.all().create(name=title1,order=title2)
            else:
                title.update(order=title2)
        return redirect('/adminmenu/')

    def delete(self,request):
        temp_del=QueryDict(request.body)
        _data=temp_del.get('data',[])
        if len(_data)!=0:
            for i in json.loads(_data):
                temp=Menu.objects.filter(id=i['id'])
                temp.delete()
        return JsonResponse({'code':0})


#权限管理
class AdminPermission(View):
    def get(self,request):
        menulist=Menu.objects.all()
        perlist=Permission.objects.filter(relationself=None)
        # perlist=Permission.objects.all()
        # perlist.delete()
        return render(request,'adminpermission.html',{"menu":menulist,"submenu":perlist})
        # return render(request,'adminpermission.html')


#权限编辑
class AdminPermissionEdit(View):
    def get(self,request):
        menulist=Menu.objects.all()
        perlist=Permission.objects.filter(relationself=None)
        # perlist=Permission.objects.all()
        # perlist.delete()
        return render(request,'adminpermissionedit.html',{"menu":menulist,"submenu":perlist})




#权限管理
class AdminPermissionData(View):
    def get(self,request):
        searchdata=request.GET.get('search',[])
        if len(searchdata)!=0 and not isinstance(searchdata,list):
            temp=Permission.objects.filter(name=searchdata)
        else:
            temp=Permission.objects.all()
        dataPagination=pagination(temp,request)
        tempdata=dataPagination.control()
        if tempdata is None:
            return render(request,'error.html')
        data=[]
        for i in tempdata:
            if i.relationself==None:
                parent=i.relationship.name+"(一级)"
            else:
                parent=i.relationself.name+"(二级)"
            dict={"id":i.id,"name":i.name,"nameurl":i.nameurl,"namemethod":i.namemethod,"relationship":parent}
            data.append(dict)
        defaultData={
            "code": 0,
            "msg": "",
            "count": temp.count(),
        }
        defaultData.update({"data":data})
        return JsonResponse(defaultData)

    def post(self,request):
        title1=request.POST.get('title1',[])
        title2=request.POST.get('title2',[])
        title3=request.POST.get('interest1',[])
        title4=request.POST.get('interest2',[])
        if all([title1,title2]):
            if title4[-3:]=="AAA":
                title4=title4[:-3]
                menuone = Menu.objects.filter(name=title4).first()
                title=Permission.objects.filter(Q(name=title1)&Q(nameurl=title2)&Q(namemethod=title3))
                if len(title)==0:
                    Permission.objects.all().create(name=title1,nameurl=title2,namemethod=title3,relationship=menuone)
            else:
                title4 = title4[:-3]
                perone=Permission.objects.filter(Q(name=title4) & Q(relationself=None)).first()
                title = Permission.objects.filter(Q(name=title1) & Q(nameurl=title2) & Q(namemethod=title3))
                if len(title)==0:
                    Permission.objects.all().create(name=title1,nameurl=title2,namemethod=title3,relationself=perone)

        return redirect('/adminpermission/')

    def put(self,request):
        temp=QueryDict(request.body)
        data=temp.get('data',[])
        if len(data)!=0:
            try:
                _data=json.loads(data)
                _id=_data['id']
                _name=_data['name']
                _namemethod=_data['method']
                _nameurl=_data['nameurl']
                _relation=_data['relation']
            except:
                return JsonResponse({"code": 0})
            _res=_relation[-3:]
            result=_relation[:-3]
            if _res=="AAA":
                _restitle = Permission.objects.filter(name=_name,relationself=None).first()
                if _restitle is not None:
                    _parent=Menu.objects.filter(name=result).first()
                    Permission.objects.filter(Q(id=_id)&Q(name=_name)).update(nameurl=_nameurl,relationship=_parent)
            elif _res=="BBB":
                _resdata=Permission.objects.filter(name=_name).first()
                if _resdata is not None:
                    _parent=Permission.objects.filter(Q(name=result)&Q(relationself=None)).first()
                    Permission.objects.filter(Q(id=_id)&Q(name=_name)).update(nameurl=_nameurl,namemethod=_namemethod,relationself=_parent)
        return JsonResponse({"code":0})

    def delete(self,request):
        temp_del=QueryDict(request.body)
        _data=temp_del.get('data',[])
        if len(_data)!=0:
            for i in json.loads(_data):
                temp=Permission.objects.filter(id=i['id'])
                temp.delete()
        return JsonResponse({'code':0})



#首页
class Welcome(View):
    def get(self,request):
        return render(request,'welcome.html')

#权限页面
class Nopermiss(View):
    def get(self,request):
        return render(request,'nopermiss.html')



#退出
class Logout(View):
    def get(self,request):
        cache.clear()
        logout(request)
        return redirect('/login/')