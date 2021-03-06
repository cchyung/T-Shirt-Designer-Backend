from django.conf.urls import url, include
from rest_framework import routers
from django.contrib.admin.views.decorators import staff_member_required
from api import views

router = routers.DefaultRouter()

router.register(r'^styles', views.StyleViewSet)
router.register(r'^styles/(?P<style_uuid>[\w-]+)/colors', views.StyleColorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^styles/image-list', views.StyleImageList.as_view()),
    url(r'^styles/(?P<style_id>[0-9]+)/images/(?P<color>[\w-]+)$', views.StyleImageDetail.as_view()),
    url(r'^addons', views.AddonListView.as_view()),
    url(r'^upload-book', staff_member_required(views.UploadBookView.as_view())),
    url(r'^calculate-price', views.CalculatePriceView.as_view())
]
