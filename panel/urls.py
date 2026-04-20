from django.urls import path
from . import views

urlpatterns = [
    path('', views.panel_home, name='panel_home'),
    # Auth
    path('api/login/',   views.api_login,   name='api_login'),
    path('api/logout/',  views.api_logout,  name='api_logout'),
    path('api/me/',      views.api_me,      name='api_me'),
    path('api/stats/',   views.api_stats,   name='api_stats'),
    # Settings
    path('api/settings/', views.api_settings, name='api_settings'),
    # Sliders
    path('api/sliders/',        views.api_sliders,       name='api_sliders'),
    path('api/sliders/<int:pk>/', views.api_slider_detail, name='api_slider_detail'),
    # Faculty
    path('api/faculty/',         views.api_faculty,        name='api_faculty'),
    path('api/faculty/<int:pk>/', views.api_faculty_detail, name='api_faculty_detail'),
    # Teachers
    path('api/teachers/',          views.api_teachers,       name='api_teachers'),
    path('api/teachers/<int:pk>/',  views.api_teacher_detail, name='api_teacher_detail'),
    path('api/departments-select/', views.api_departments_select, name='api_departments_select'),
    # News
    path('api/news/',                    views.api_news,              name='api_news'),
    path('api/news/<int:pk>/',           views.api_news_detail,       name='api_news_detail'),
    path('api/news/<int:pk>/images/',    views.api_news_images,       name='api_news_images'),
    path('api/news/images/<int:pk>/',    views.api_news_image_delete, name='api_news_image_delete'),
    path('api/news-categories/',         views.api_news_categories,   name='api_news_categories'),
    # Leadership
    path('api/leadership/',          views.api_leadership,        name='api_leadership'),
    path('api/leadership/<int:pk>/',  views.api_leadership_detail, name='api_leadership_detail'),
    # Departments
    path('api/departments/',          views.api_departments,        name='api_departments'),
    path('api/departments/<int:pk>/',  views.api_department_detail,  name='api_department_detail'),
    # Centers
    path('api/centers/',          views.api_centers,       name='api_centers'),
    path('api/centers/<int:pk>/', views.api_center_detail, name='api_center_detail'),
    # Events
    path('api/events/',                      views.api_events,            name='api_events'),
    path('api/events/<int:pk>/',             views.api_event_detail,      name='api_event_detail'),
    path('api/events/<int:pk>/images/',      views.api_event_images,      name='api_event_images'),
    path('api/events/images/<int:pk>/',      views.api_event_image_delete,name='api_event_image_delete'),
    # FAQ
    path('api/faqs/',          views.api_faqs,       name='api_faqs'),
    path('api/faqs/<int:pk>/', views.api_faq_detail, name='api_faq_detail'),
    # Partners
    path('api/partners/',          views.api_partners,       name='api_partners'),
    path('api/partners/<int:pk>/', views.api_partner_detail, name='api_partner_detail'),
    # Messages
    path('api/messages/',          views.api_messages,       name='api_messages'),
    path('api/messages/<int:pk>/', views.api_message_detail, name='api_message_detail'),
]
