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
    # Static Pages
    path('api/pages/',          views.api_pages,       name='api_pages'),
    path('api/pages/<int:pk>/', views.api_page_detail, name='api_page_detail'),
    # Select helpers
    path('api/faculty-select/',            views.api_faculty_select,            name='api_faculty_select'),
    path('api/article-categories-select/', views.api_article_categories_select, name='api_article_categories_select'),
    # Article Categories
    path('api/article-categories/',          views.api_article_categories,        name='api_article_categories'),
    path('api/article-categories/<int:pk>/', views.api_article_category_detail,   name='api_article_category_detail'),
    # Scientific Articles
    path('api/articles/',          views.api_articles,       name='api_articles'),
    path('api/articles/<int:pk>/', views.api_article_detail, name='api_article_detail'),
    # Dissertations
    path('api/dissertations/',          views.api_dissertations,       name='api_dissertations'),
    path('api/dissertations/<int:pk>/', views.api_dissertation_detail, name='api_dissertation_detail'),
    # Conferences
    path('api/conferences/',          views.api_conferences,       name='api_conferences'),
    path('api/conferences/<int:pk>/', views.api_conference_detail, name='api_conference_detail'),
    # Contests
    path('api/contests/',          views.api_contests,       name='api_contests'),
    path('api/contests/<int:pk>/', views.api_contest_detail, name='api_contest_detail'),
    # Video Lessons
    path('api/videos/',          views.api_videos,       name='api_videos'),
    path('api/videos/<int:pk>/', views.api_video_detail, name='api_video_detail'),
    # Talented Students
    path('api/talented/',          views.api_talented,       name='api_talented'),
    path('api/talented/<int:pk>/', views.api_talent_detail,  name='api_talent_detail'),
    # Journal Issues
    path('api/journals/',          views.api_journals,       name='api_journals'),
    path('api/journals/<int:pk>/', views.api_journal_detail, name='api_journal_detail'),
    # Schedule Files
    path('api/schedules/',          views.api_schedules,       name='api_schedules'),
    path('api/schedules/<int:pk>/', views.api_schedule_detail, name='api_schedule_detail'),
    # Library Resources
    path('api/library/',          views.api_library,        name='api_library'),
    path('api/library/<int:pk>/', views.api_library_detail, name='api_library_detail'),
]
