from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin

from django.urls import url
from foundry.views import *
from . import views
from foundry import views as foundry_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from puput import urls as puput_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', homepage),
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),

    # Paypal forms
    path("payment/", views.paypal_payment, name= "paypal_payment"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('/paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    path('/paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),

     path('payment2/', views.PaypalView.as_view(), name='payment2'),

    path('accounts/', include('allauth.urls')),
]


urlpatterns = urlpatterns + [
    # Companys
    url(r'^foundry/dashboard/(?P<pk>\w+)/$', dashboard),
    url(r'^foundry/report/(?P<pk>\w+)/$', report),
    url(r'^foundry/$', CompanyList.as_view(), name='company_list'),
    # Forms
    url(r'^company_add/$', CompanyCreate.as_view(), name='company_add'),
    url(r'^company_update/(?P<pk>\w+)/$', CompanyUpdate.as_view(), name='company_update'),
    url(r'^company_delete/(?P<pk>\w+)/$', CompanyDelete.as_view(), name='company_delete'),
    
    # URL for the startup application form (multi-step)
    path('startup-application/', foundry_views.startup_application, name='startup_application'),

    # URL for founder sign-up
    path('founder-signup/', foundry_views.founder_signup, name='founder_signup'),
]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(puput_urls)),
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = urlpatterns + [
        # For anything not caught by a more specific rule above, hand over to
        # the list:
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    

