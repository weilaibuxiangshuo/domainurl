"""domainurl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
app_name="domain"
urlpatterns = [
    path('login/', Login.as_view(),name="login"),
    path('logout/', Logout.as_view(),name="logout"),
    path('index/', Index.as_view(),name="index"),
    path('adminrole/', AdminRole.as_view(),name="adminrole"),
    path('adminroleiframe/', AdminRoleIframe.as_view(),name="adminroleiframe"),
    path('adminroleset/', AdminRoleSet.as_view(),name="adminroleset"),
    path('adminroledata/', AdminRoleData.as_view(),name="adminroledata"),
    path('adminroleedit/', AdminRoleEdit.as_view(),name="adminroleedit"),
    path('adminmenu/', AdminMenu.as_view(),name="adminmenu"),
    path('adminmenudata/', AdminMenuData.as_view(),name="adminmenudata"),
    path('adminpermission/', AdminPermission.as_view(),name="adminpermission"),
    path('adminpermissionedit/', AdminPermissionEdit.as_view(),name="adminpermissionedit"),
    path('adminpermissiondata/', AdminPermissionData.as_view(),name="adminpermissiondata"),
    path('adminuser/', AdminUser.as_view(),name="adminuser"),
    path('adminuserdata/', AdminUserData.as_view(),name="adminuserdata"),
    path('adminuseriframe/', AdminUserIframe.as_view(),name="adminuseriframe"),
    path('welcome/', Welcome.as_view(),name="welcome"),
    path('nopermiss/', Nopermiss.as_view(),name="nopermiss"),
    path('captchaview/', CaptchaView.as_view(),name="captchaview"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
