from django.urls import path,include
from httpx import main
from rest_framework import routers


from . import views
router = routers.DefaultRouter()
router.register(r'TweetsView', views.TweetsViewSet)

urlpatterns = [
    
        #path('like',views.like,name='like'),
         path('lake',views.lake,name='lake'),
         path('bbc',views.bbc,name='bbc'),
       path('forest',views.forest,name='forest'),
           path('news',views.news,name='news'),
            path('c',views.c,name='c'),
            path('cvd',views.cvd,name='cvd'),
            path('youtube',views.youtube,name='youtube'),
           # path('TweetsView',views.TweetsViewSet,name='TweetsView')
             path('api/', include(router.urls)),
             path('kar',views.kar,name='kar'),
             path('tesla',views.tesla,name='tesla'),
             path('tech',views.tech,name='tech'),
             path('img',views.img,name='img'),
             path('infl',views.infl,name='infl'),
             path('lake',views.lake,name='lake')
            # path('ap', include('rest_framework.urls', namespace='ap'))   
         
      
     
    

]