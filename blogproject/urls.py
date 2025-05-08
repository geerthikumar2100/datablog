from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views  
from django.templatetags.static import static
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_views.dashboard, name='dashboard'),  # Homepage is dashboard
    path('', include('blog.urls')),  # Other blog URLs
    path('logout/', blog_views.logout_view, name='logout'),  # Use correct alias
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
