from django.urls import path

from . import views

app_name = 'finances'
urlpatterns= [
	path('home', views.index, name='index'),
	path('signup', views.signup, name='signup'),
	path('login', views.log_in, name='login'),
	path('logout', views.log_out, name='logout'),
	path('assets/view', views.assets_view, name='assets_view'),
	path('assets/add', views.assets_add, name='assets_add'),
	path('assets/update', views.assets_update, name='assets_update'),
	path('statements/view', views.statements_view, name='statements_view'),
	path('statements/add', views.statements_add, name='statements_add'),
	path('statements/update', views.statements_update, name='statements_update')
]
