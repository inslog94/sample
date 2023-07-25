from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='user/user_login.html'), name='index'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('user/', include('user.urls')),
]
