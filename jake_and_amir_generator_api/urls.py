from django.conf.urls import patterns, include, url
from django.contrib import admin

from jake_and_amir_generator_api.views import CharacterViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'characters', CharacterViewSet, base_name="characters")
urlpatterns = router.urls

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
)
