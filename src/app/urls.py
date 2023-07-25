from django.contrib import admin
from django.urls import path, include
from user.views import Login

urlpatterns = [
    path('', Login.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('user/', include('user.urls')),
]
