from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login),
    path('register/', views.reg),
    path('logout', views.logout),
    
    # admin
    path('admin', views.admin), 
    path('emp_data', views.emp_data),
    path('emp_req', views.emp_req),
    path('emp_approve/<int:id>', views.emp_approve),
    path('emp_reject/<int:id>', views.emp_reject),
    path('emp_edit/<int:id>', views.emp_edit),
    path('emp_edit/emp_remove/<int:id>', views.emp_remove),
    path('aprrove_stock', views.approve_stock),
    path('reject_stock/<int:id>', views.reject_med),
    path('verify_stock/<int:id>', views.verify_stock),

    # employee
    path('employee', views.employee),
    path('approved_med/<int:id>', views.approved_med),
    path('medicine', views.medicine),
    path('edit_med/<int:id>', views.edit_med),
    path('medicine_data', views.medicine_data),
    path('med_req/<int:id>', views.req_more),
    path('user_data', views.user_data),
    path('user_reject/<int:id>', views.user_reject),
    path('user_approve/<int:id>', views.user_approve),
    path('user_edit/<int:id>', views.user_edit),
    path('user_edit/user_remove/<int:id>', views.user_remove),
    path('pending_purchace', views.pending_purchace),
    path('purchace_approve/<int:id>', views.purchace_approve),
    path('purchace_reject/<int:id>', views.purchace_reject),
    path('profile/<int:id>', views.profile),
    path('purchase_history_all', views.purchase_history_all),

    # user
    path('user', views.user_),
    path('add_to_cart/<int:id>', views.add_to_cart),
    path('cart_update/<int:id>/<int:p>', views.cart_update),
    path('cart_remove/<int:id>', views.cart_remove),
    path('purchase/<int:id>', views.purchase),
    path('available_med', views.available_med),
    path('purchace_history', views.purchace_history),
    path('clear_one/<int:id>', views.clear_one),
    path('clear_all/<int:id>', views.clear_all),
    path('clear_all_order/<int:id>', views.clear_all_order),
    path('profile_emp/<int:id>', views.profile_emp),

#################
    path('try/', views.tryy),
]