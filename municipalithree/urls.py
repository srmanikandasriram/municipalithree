from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'municipalithree.views.home', name='home'),
    url(r'^submit/', 'municipalithree.views.submit', name='submit'),
    url(r'^api/', 'municipalithree.views.api', name='api'),
    url(r'^auth/', 'municipalithree.views.auth', name='auth'),
    url(r'^browse/', 'municipalithree.views.browse', name='browse'),
    url(r'^stats/', 'municipalithree.views.stats', name='stats'),
    url(r'^images/', 'municipalithree.views.image', name='images'),
    url(r'^dashboard/', 'municipalithree.views.dashboard', name='dashboard'),
    url(r'^browsers/', 'municipalithree.views.browsers', name='browsers'),
    # url(r'^municipalithree/', include('municipalithree.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
