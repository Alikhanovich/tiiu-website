from django.urls import path
from . import views

urlpatterns = [
    path("",                      views.index,          name="index"),
    path("about/",                views.about,           name="about"),
    path("faculties/",            views.faculties,       name="faculties"),
    path("faculties/<slug:slug>/",views.faculty_detail,  name="faculty_detail"),
    path("news/",                 views.news_list,       name="news_list"),
    path("news/<slug:slug>/",     views.news_detail,     name="news_detail"),
    path("events/",               views.events,          name="events"),
    path("events/<slug:slug>/",   views.event_detail,    name="event_detail"),
    path("gallery/",              views.gallery,         name="gallery"),
    path("gallery/<slug:slug>/",  views.gallery_detail,  name="gallery_detail"),
    path("contact/",              views.contact,         name="contact"),
    path("contact/submit/",       views.contact_submit,  name="contact_submit"),
    path("teachers/",             views.teachers,        name="teachers"),
    path("leadership/",           views.leadership,      name="leadership"),
    path("departments/",          views.departments,     name="departments"),
    path("centers/",              views.centers,         name="centers"),
    path("pages/<slug:slug>/",    views.static_page,     name="static_page"),
]
