#url(r'^submit', views.submit)
url(r'post^$', 'core.views.RunQuery',name='RunQuery'),