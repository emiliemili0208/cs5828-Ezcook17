from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>(\w+-){4}\w+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>(\w+-){4}\w+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^home/$', views.post_list_without_edit, name='post_list_without_edit'),
    url(r'^home/(?P<pk>(\w+-){4}\w+)/$', views.post_detail_without_edit, name='post_detail_without_edit'),

    url(r'^login/$', views.login_form, name='login_form'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_form, name='logout_form'),
    url(r'^mystock/$', views.my_stock, name='my_stock'),
    url(r'^mystock/new/$', views.add_ingredient, name='add_ingredient'),
    # url(r'^favorite/$', views.favorite_list, name='post_list_without_edit'),
    # url(r'^favorite/(?P<pk>(\w+-){4}\w+)/$', views.post_detail_without_edit, name='post_detail_without_edit'),
    # url(r'^ingredient/edit/(?P<name>\w+)/$', views.edit_ingredient, name='edit_ingredient'),
    url(r'^download/(?P<pk>(\w+-){4}\w+)/$', views.download, name='download'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='profilex'),
    url(r'^account/(?P<username>[a-zA-Z0-9]+)$', views.get_user_account, name='account'),
]
