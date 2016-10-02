from django.conf.urls import url, include
from django.conf.urls.static import static

from django.contrib import admin
from django.conf import settings

# fundraisers
from api.fundraiser.views import (
	FundraiserProcessView, 
	TrackEmailOrder, 
	FundraisersViewSet,
	FundraiserBySlugViewSet,
	FundraiserTypesView,
	FundraiserTypesView,
	FundraiserPlansView,
	APIAllFundraisers,
	APIFundrasierCreate
)

# organizations
from api.organization.views import (
	APIOrganizationTypes,
	APIOrganizationsList,
	APIOrganizationById,
	APIOrganizationsContacts,
	APIOrganizationsCreate
)

# contacts 
from api.contact.views import (
	APIContactsList,
	APIContactsCreate,
	APIContactTypes
)

# profiles
from api.account.views import (
	APIProfileView,
	APIProfileCreateView,
	APIProfileUpdateView,
	APIPaginatedProfilesView,
	APIUserAccountList,
	APIUserAccountCreate
)

# dashboard
from api.dashboard.views import(
	APIDashboardStats,
)

# shipment
from api.shipment.views import APIGetRates

# email
from api.email.views import APISendEmail,APISendConfirmEmail

# products
from api.product.views import QueryProductView,APIProductListByCategory,APIProductList

from home import views as home_views
from account import views as account_views
from product import views as product_views
from fundraiser import views as fundraiser_views
from marketing import views as marketing_views
from dashboard import views as dashboard_views


# base
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

# home 
urlpatterns += [
	url(r'^$', home_views.home,name='home'),
	url(r'^plan/(?P<id>\d+)/$', home_views.plan_type, name='plan_type'),
	url(r'^download-forms-packet/(?P<id>\d+)/$', home_views.download_forms, name='download_forms'),
]

# account
urlpatterns += [
	url(r'^account/login',account_views.auth_login,name='auth_login'),
	url(r'^account/simple-sign-up',account_views.auth_simple_sign_up, name='auth_simple_sign_up'),
	url(r'^account/logout',account_views.auth_logout,name='auth_logout'),
	url(r'^account/fundraiser/login',account_views.auth_login_and_add_account_to_fundraiser),
	url(r'^account/create',account_views.auth_create_account,name='auth_create_account'),
	url(r'^account/send-password-reset/$',account_views.send_reset_email,name='send_reset_email'),
	url(r'^account/password-reset/(?P<key>.{0,100})/$',account_views.receive_password_reset),
	url(r'^account/submit-password-reset/$',account_views.submited_password_reset),

	# profile
	url(r'^profile/$',account_views.profile_show,name='profile_show'),
	url(r'^profile/(?P<slug>[-\w]+)/$',account_views.profile_detail,name='profile_detail'),
	url(r'^profile/fundraiser/(?P<id>\d+)/$',account_views.profile_fundraiser_detail,name='profile_fundraiser_detail'),
	url(r'^profile/edit/(?P<slug>[-\w]+)/$',account_views.profile_edit,name='profile_edit'),

]

# product
urlpatterns += [
	url(r'^products/show-salsas/$',product_views.show_all_salsas,name='show_all_salsas'),
	url(r'^categories/(?P<slug>[-\w]+)/$',product_views.show_by_category,name='show_by_category'),
	url(r'^search-salsas/$',product_views.search_salsas,name='search_salsas'),
]

# fundraiser
urlpatterns += [
	# test checkout
	url(r'^test-checkout/$', fundraiser_views.test_checkout,name='test_checkout'),

	# describe
	url(r'^start-process/$', fundraiser_views.start_process,name='start_process'),
	url(r'^start-over/$', fundraiser_views.start_over,name='start_over'),
	url(r'^lets-do-a-fundraiser/$', fundraiser_views.describe_fundraiser,name='describe_fundraiser'),
	url(r'^choose-profile-for-fundraiser/$', fundraiser_views.choose_profile_for_fundraiser,name='choose_profile_for_fundraiser'),
	url(r'^(?P<slug>[-\w]+)/lets-do-another-fundraiser/$', fundraiser_views.logged_in_describe_fundraiser,name='logged_in_describe_fundraiser'),
	# fundraiser type
	url(r'^fundraiser/$', fundraiser_views.choose_fundraiser,name='choose_fundraiser'),
	url(r'^fundraiser/choose-salsas/$', fundraiser_views.chosen_fundraiser_type,name='chosen_fundraiser_type'),
	# choose salsas
	url(r'^pick-salsas/$', fundraiser_views.choose_salsas,name='choose_salsas'),
	# shipment
	url(r'^fundraiser-shipment', fundraiser_views.create_shipment,name='create_shipment'),
	url(r'^fundraiser/shipment/edit/(?P<id>\d+)$', fundraiser_views.edit_shipment,name='edit_shipment'),
	url(r'^fundraiser-get-back-on-track/$', fundraiser_views.get_back_on_track,name='get_back_on_track'),
	# checkout
	url(r'^checkout/$', fundraiser_views.checkout,name='checkout'),
	url(r'^summary-invoice/$', fundraiser_views.process_checkout,name='process_checkout'),
	url(r'^type-selection/(?P<id>\d+)$',fundraiser_views.get_fundraiser_selections_via_ajax),
]

# marketing
urlpatterns += [
	url(r'^valid-discount/',marketing_views.process_discount,name='process_discount'),
	url(r'^view/',marketing_views.add_email_to_newsletter_list,name='add_email_to_newsletter_list'),
]

# admin-dashboard
urlpatterns += [
	url(r'^dashboard/login/$',dashboard_views.jmi_admin_login,name='jmi_admin_login'),
	url(r'^dashboard/$', dashboard_views.dashboard_index,name='dashboard_index'),
	url(r'^dashboard/fundraiser/(?P<id>\d+)/update/$', dashboard_views.fundraiser_update,name='fundraiser_update'),
	url(r'^dashboard/shipment/(?P<id>\d+)/$',dashboard_views.shipment_detail,name='shipment_detail'),
]

# api
urlpatterns += [
	# fundraiserTypes
	url(r'^api/fundraisers/types/',FundraiserTypesView.as_view()),
	url(r'^api/fundraisers/plans/',FundraiserPlansView.as_view()),
	# fundraiser
	url(r'^api/process-fundraiser/',FundraiserProcessView.as_view(),name='process_fundraiser'),
	url(r'^api/fundraisers/$',FundraisersViewSet.as_view()),
	url(r'^api/fundraisers/all/$',APIAllFundraisers.as_view()),
	url(r'^api/fundraisers/create/$',APIFundrasierCreate.as_view()),
	url(r'^api/fundraisers/(?P<id>\d+)$',FundraiserBySlugViewSet.as_view()),

	# product
	url(r'^api/products/$',APIProductList.as_view()),
	url(r'^api/products-by-category/$',APIProductListByCategory.as_view()),
	url(r'^api/product/(?P<id>\d+)',QueryProductView.as_view()),
	# account
	url(r'^api/paginated-profiles/$',APIPaginatedProfilesView.as_view()),
	url(r'^api/profiles/$',APIProfileView.as_view()),
	url(r'^api/profiles/create/$',APIProfileCreateView.as_view()),
	url(r'^api/profiles/(?P<id>\d+)/edit/$',APIProfileUpdateView.as_view()),
	url(r'^api/user-accounts/$',APIUserAccountList.as_view()),
	url(r'^api/users/create/$',APIUserAccountCreate.as_view()),
	
	# dashboard
	url(r'^api/dashboard/stats/$',APIDashboardStats.as_view()),
	
	# organizations
	url(r'^api/organizations/types/$',APIOrganizationTypes.as_view()),
	url(r'^api/organizations/$',APIOrganizationsList.as_view()),
	url(r'^api/organizations/create$',APIOrganizationsCreate.as_view()),
	url(r'^api/organizations/(?P<id>\d+)$',APIOrganizationById.as_view()),
	url(r'^api/organizations/(?P<id>\d+)/contacts$',APIOrganizationsContacts.as_view()),
	# contact
	url(r'^api/contacts/$',APIContactsList.as_view()),
	url(r'^api/contacts/types/$',APIContactTypes.as_view()),
	url(r'^api/contacts/create/$',APIContactsCreate.as_view()),
	# email
	url(r'^api/send-email$',APISendEmail.as_view()),
	url(r'^api/send-confirm/(?P<id>\d+)$',APISendConfirmEmail.as_view()),
	# shipment
	url(r'^api/shipment/rates$',APIGetRates.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	import debug_toolbar
	urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
