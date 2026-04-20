import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from main.models import (
    SiteSettings, Slider, Faculty, Teacher, NewsCategory, News, NewsImage,
    Event, EventImage, Gallery, GalleryImage, FAQ, Partner, ContactMessage,
    Leadership, Department, Center,
)


def staff_only(view):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'success': False, 'error': 'Kirish taqiqlangan'}, status=403)
        return view(request, *args, **kwargs)
    wrapped.__name__ = view.__name__
    return wrapped


def img(obj, field):
    f = getattr(obj, field, None)
    return f.url if f else None


def dt(obj, field):
    v = getattr(obj, field, None)
    return v.strftime('%d.%m.%Y %H:%M') if v else None


# ── SPA shell ────────────────────────────────────────────────────────────────
@ensure_csrf_cookie
def panel_home(request):
    return render(request, 'panel/app.html')


# ── Auth ─────────────────────────────────────────────────────────────────────
@require_http_methods(['POST'])
def api_login(request):
    d = json.loads(request.body)
    user = authenticate(request, username=d.get('username'), password=d.get('password'))
    if user and user.is_staff:
        login(request, user)
        return JsonResponse({'success': True, 'username': user.username})
    return JsonResponse({'success': False, 'error': "Login yoki parol noto'g'ri"}, status=401)


@require_http_methods(['POST'])
def api_logout(request):
    logout(request)
    return JsonResponse({'success': True})


def api_me(request):
    if request.user.is_authenticated and request.user.is_staff:
        return JsonResponse({'auth': True, 'username': request.user.username})
    return JsonResponse({'auth': False})


# ── Dashboard stats ───────────────────────────────────────────────────────────
@staff_only
def api_stats(request):
    return JsonResponse({'success': True, 'data': {
        'news':       News.objects.count(),
        'teachers':   Teacher.objects.count(),
        'faculty':    Faculty.objects.count(),
        'new_msgs':   ContactMessage.objects.filter(status='new').count(),
        'events':     Event.objects.count(),
        'leadership': Leadership.objects.count(),
        'departments':Department.objects.count(),
        'centers':    Center.objects.count(),
    }})


# ── Generic helpers ───────────────────────────────────────────────────────────
def paginate(qs, request, per=20):
    page = int(request.GET.get('page', 1))
    total = qs.count()
    items = list(qs[(page-1)*per : page*per])
    return items, total, page, -(-total // per)


# ══════════════════════════════════════════════════════════════════════════════
#  SiteSettings
# ══════════════════════════════════════════════════════════════════════════════
def serialize_settings(o):
    return {
        'id': o.pk, 'site_name': o.site_name, 'site_name_full': o.site_name_full,
        'logo': img(o, 'logo'), 'favicon': img(o, 'favicon'),
        'address': o.address, 'phone1': o.phone1, 'phone2': o.phone2,
        'email': o.email, 'work_hours': o.work_hours,
        'facebook': o.facebook, 'instagram': o.instagram,
        'telegram': o.telegram, 'youtube': o.youtube,
        'founded_year': o.founded_year, 'student_count': o.student_count,
        'teacher_count': o.teacher_count, 'direction_count': o.direction_count,
        'about_text': o.about_text, 'hero_title': o.hero_title, 'hero_subtitle': o.hero_subtitle,
    }


@staff_only
def api_settings(request):
    obj = SiteSettings.get()
    if request.method == 'POST':
        d = request.POST
        fields = ['site_name','site_name_full','address','phone1','phone2','email',
                  'work_hours','facebook','instagram','telegram','youtube',
                  'founded_year','student_count','teacher_count','direction_count',
                  'about_text','hero_title','hero_subtitle']
        for f in fields:
            if f in d: setattr(obj, f, d[f])
        for imgf in ['logo', 'favicon']:
            if imgf in request.FILES: setattr(obj, imgf, request.FILES[imgf])
        obj.save()
        return JsonResponse({'success': True, 'data': serialize_settings(obj)})
    return JsonResponse({'success': True, 'data': serialize_settings(obj)})


# ══════════════════════════════════════════════════════════════════════════════
#  Slider
# ══════════════════════════════════════════════════════════════════════════════
def serialize_slider(o):
    return {'id':o.pk,'title':o.title,'subtitle':o.subtitle,'image':img(o,'image'),
            'btn_text':o.btn_text,'btn_url':o.btn_url,'order':o.order,'is_active':o.is_active}


@staff_only
def api_sliders(request):
    if request.method == 'POST':
        d = request.POST
        o = Slider(title=d['title'], subtitle=d.get('subtitle',''),
                   btn_text=d.get('btn_text',''), btn_url=d.get('btn_url','/'),
                   order=int(d.get('order',0)), is_active=d.get('is_active')=='true')
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success': True, 'data': serialize_slider(o)})
    items, total, page, pages = paginate(Slider.objects.all(), request)
    return JsonResponse({'success':True,'data':[serialize_slider(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_slider_detail(request, pk):
    try: o = Slider.objects.get(pk=pk)
    except Slider.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['title','subtitle','btn_text','btn_url']:
            if f in d: setattr(o,f,d[f])
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_slider(o)})
    return JsonResponse({'success':True,'data':serialize_slider(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  Faculty (Yo'nalishlar)
# ══════════════════════════════════════════════════════════════════════════════
def serialize_faculty(o):
    return {'id':o.pk,'name':o.name,'slug':o.slug,'short_name':o.short_name,'icon':o.icon,
            'image':img(o,'image'),'description':o.description,'degree':o.degree,
            'study_forms':o.study_forms,'duration':o.duration,'order':o.order,'is_active':o.is_active}


@staff_only
def api_faculty(request):
    if request.method == 'POST':
        d = request.POST
        o = Faculty(name=d['name'], short_name=d.get('short_name',''), icon=d.get('icon','🎓'),
                    description=d.get('description',''), degree=d.get('degree','bachelor'),
                    study_forms=d.get('study_forms',''), duration=int(d.get('duration',4)),
                    order=int(d.get('order',0)), is_active=d.get('is_active')=='true')
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_faculty(o)})
    items, total, page, pages = paginate(Faculty.objects.all(), request)
    return JsonResponse({'success':True,'data':[serialize_faculty(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_faculty_detail(request, pk):
    try: o = Faculty.objects.get(pk=pk)
    except Faculty.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['name','short_name','icon','description','degree','study_forms']:
            if f in d: setattr(o,f,d[f])
        if 'duration' in d: o.duration = int(d['duration'])
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_faculty(o)})
    return JsonResponse({'success':True,'data':serialize_faculty(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  Teacher
# ══════════════════════════════════════════════════════════════════════════════
def serialize_teacher(o):
    return {'id':o.pk,'full_name':o.full_name,'slug':o.slug,'position':o.position,
            'kafedra_id':o.kafedra_id,'kafedra_name':str(o.kafedra) if o.kafedra else None,
            'photo':img(o,'photo'),'bio':o.bio,'email':o.email,'phone':o.phone,
            'linkedin':o.linkedin,'experience':o.experience,'order':o.order,'is_active':o.is_active}


@staff_only
def api_teachers(request):
    if request.method == 'POST':
        d = request.POST
        o = Teacher(full_name=d['full_name'], position=d.get('position',''),
                    bio=d.get('bio',''), email=d.get('email',''), phone=d.get('phone',''),
                    linkedin=d.get('linkedin',''), experience=int(d.get('experience',0)),
                    order=int(d.get('order',0)), is_active=d.get('is_active')=='true')
        if d.get('kafedra_id'): o.kafedra_id = int(d['kafedra_id'])
        if 'photo' in request.FILES: o.photo = request.FILES['photo']
        o.save()
        return JsonResponse({'success':True,'data':serialize_teacher(o)})
    items, total, page, pages = paginate(Teacher.objects.select_related('kafedra').all(), request)
    return JsonResponse({'success':True,'data':[serialize_teacher(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_teacher_detail(request, pk):
    try: o = Teacher.objects.get(pk=pk)
    except Teacher.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['full_name','position','bio','email','phone','linkedin']:
            if f in d: setattr(o,f,d[f])
        if 'experience' in d: o.experience = int(d['experience'])
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'kafedra_id' in d: o.kafedra_id = int(d['kafedra_id']) if d['kafedra_id'] else None
        if 'photo' in request.FILES: o.photo = request.FILES['photo']
        o.save()
        return JsonResponse({'success':True,'data':serialize_teacher(o)})
    return JsonResponse({'success':True,'data':serialize_teacher(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  News
# ══════════════════════════════════════════════════════════════════════════════
def serialize_news(o):
    return {'id':o.pk,'title':o.title,'slug':o.slug,
            'category_id':o.category_id,'category_name':str(o.category) if o.category else None,
            'image':img(o,'image'),'short_text':o.short_text,'body':o.body,'author':o.author,
            'views':o.views,'is_active':o.is_active,'is_featured':o.is_featured,
            'created_at':dt(o,'created_at')}


@staff_only
def api_news(request):
    if request.method == 'POST':
        d = request.POST
        o = News(title=d['title'], short_text=d.get('short_text',''), body=d.get('body',''),
                 author=d.get('author',''), is_active=d.get('is_active')=='true',
                 is_featured=d.get('is_featured')=='true')
        if d.get('category_id'): o.category_id = int(d['category_id'])
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_news(o)})
    items, total, page, pages = paginate(News.objects.select_related('category').all(), request)
    return JsonResponse({'success':True,'data':[serialize_news(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_news_detail(request, pk):
    try: o = News.objects.get(pk=pk)
    except News.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['title','short_text','body','author']:
            if f in d: setattr(o,f,d[f])
        if 'category_id' in d: o.category_id = int(d['category_id']) if d['category_id'] else None
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'is_featured' in d: o.is_featured = d['is_featured']=='true'
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_news(o)})
    return JsonResponse({'success':True,'data':serialize_news(o)})


@staff_only
def api_news_images(request, pk):
    try: news = News.objects.get(pk=pk)
    except News.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'POST':
        o = NewsImage(news=news, caption=request.POST.get('caption',''),
                      order=int(request.POST.get('order',0)))
        if 'image' in request.FILES: o.image = request.FILES['image']
        else: return JsonResponse({'success':False,'error':'Rasm yuklanmadi'},status=400)
        o.save()
        return JsonResponse({'success':True,'data':{'id':o.pk,'image':img(o,'image'),'caption':o.caption,'order':o.order}})
    data = [{'id':o.pk,'image':img(o,'image'),'caption':o.caption,'order':o.order} for o in news.images.all()]
    return JsonResponse({'success':True,'data':data})


@staff_only
@require_http_methods(['DELETE'])
def api_news_image_delete(request, pk):
    try: o = NewsImage.objects.get(pk=pk)
    except NewsImage.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    o.delete()
    return JsonResponse({'success':True})


@staff_only
def api_news_categories(request):
    cats = [{'id':c.pk,'name':c.name,'color':c.color} for c in NewsCategory.objects.all()]
    return JsonResponse({'success':True,'data':cats})


# ══════════════════════════════════════════════════════════════════════════════
#  Leadership
# ══════════════════════════════════════════════════════════════════════════════
def serialize_leadership(o):
    return {'id':o.pk,'full_name':o.full_name,'rank':o.rank,'position':o.position,
            'qualification':o.qualification,'photo':img(o,'photo'),'bio':o.bio,
            'email':o.email,'phone':o.phone,'reception_days':o.reception_days,
            'reception_time':o.reception_time,'order':o.order,'is_active':o.is_active}


@staff_only
def api_leadership(request):
    if request.method == 'POST':
        d = request.POST
        o = Leadership(full_name=d['full_name'], rank=d.get('rank',''), position=d.get('position',''),
                       qualification=d.get('qualification',''), bio=d.get('bio',''),
                       email=d.get('email',''), phone=d.get('phone',''),
                       reception_days=d.get('reception_days',''), reception_time=d.get('reception_time',''),
                       order=int(d.get('order',0)), is_active=d.get('is_active')=='true')
        if 'photo' in request.FILES: o.photo = request.FILES['photo']
        o.save()
        return JsonResponse({'success':True,'data':serialize_leadership(o)})
    items, total, page, pages = paginate(Leadership.objects.all(), request)
    return JsonResponse({'success':True,'data':[serialize_leadership(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_leadership_detail(request, pk):
    try: o = Leadership.objects.get(pk=pk)
    except Leadership.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['full_name','rank','position','qualification','bio','email','phone','reception_days','reception_time']:
            if f in d: setattr(o,f,d[f])
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'photo' in request.FILES: o.photo = request.FILES['photo']
        o.save()
        return JsonResponse({'success':True,'data':serialize_leadership(o)})
    return JsonResponse({'success':True,'data':serialize_leadership(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  Department
# ══════════════════════════════════════════════════════════════════════════════
def serialize_dept(o):
    return {'id':o.pk,'name':o.name,'slug':o.slug,'head':o.head,'description':o.description,
            'image':img(o,'image'),'order':o.order,'is_active':o.is_active}


@staff_only
def api_departments(request):
    if request.method == 'POST':
        d = request.POST
        o = Department(name=d['name'], head=d.get('head',''), description=d.get('description',''),
                       order=int(d.get('order',0)), is_active=d.get('is_active')=='true')
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_dept(o)})
    items, total, page, pages = paginate(Department.objects.all(), request)
    return JsonResponse({'success':True,'data':[serialize_dept(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_department_detail(request, pk):
    try: o = Department.objects.get(pk=pk)
    except Department.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['name','head','description']:
            if f in d: setattr(o,f,d[f])
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_dept(o)})
    return JsonResponse({'success':True,'data':serialize_dept(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  Center
# ══════════════════════════════════════════════════════════════════════════════
def serialize_center(o):
    return {'id':o.pk,'name':o.name,'slug':o.slug,'icon':o.icon,'head':o.head,
            'head_role':o.head_role,'head_phone':o.head_phone,'head_email':o.head_email,
            'work_hours':o.work_hours,'description':o.description,'image':img(o,'image'),
            'order':o.order,'is_active':o.is_active}


@staff_only
def api_centers(request):
    if request.method == 'POST':
        d = request.POST
        o = Center(name=d['name'], icon=d.get('icon','🏢'), head=d.get('head',''),
                   head_role=d.get('head_role',''), head_phone=d.get('head_phone',''),
                   head_email=d.get('head_email',''), work_hours=d.get('work_hours',''),
                   description=d.get('description',''), order=int(d.get('order',0)),
                   is_active=d.get('is_active')=='true')
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_center(o)})
    items, total, page, pages = paginate(Center.objects.all(), request)
    return JsonResponse({'success':True,'data':[serialize_center(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_center_detail(request, pk):
    try: o = Center.objects.get(pk=pk)
    except Center.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['name','icon','head','head_role','head_phone','head_email','work_hours','description']:
            if f in d: setattr(o,f,d[f])
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_center(o)})
    return JsonResponse({'success':True,'data':serialize_center(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  Event
# ══════════════════════════════════════════════════════════════════════════════
def serialize_event(o):
    return {'id':o.pk,'title':o.title,'slug':o.slug,'image':img(o,'image'),
            'description':o.description,'body':o.body,'location':o.location,
            'event_date':o.event_date.strftime('%Y-%m-%dT%H:%M') if o.event_date else None,
            'is_active':o.is_active,'views':o.views}


@staff_only
def api_events(request):
    if request.method == 'POST':
        d = request.POST
        from django.utils.dateparse import parse_datetime
        o = Event(title=d['title'], description=d.get('description',''),
                  body=d.get('body',''), location=d.get('location',''),
                  event_date=parse_datetime(d['event_date']), is_active=d.get('is_active')=='true')
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_event(o)})
    items, total, page, pages = paginate(Event.objects.all(), request)
    return JsonResponse({'success':True,'data':[serialize_event(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_event_images(request, pk):
    try: event = Event.objects.get(pk=pk)
    except Event.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'POST':
        o = EventImage(event=event, caption=request.POST.get('caption',''),
                       order=int(request.POST.get('order',0)))
        if 'image' in request.FILES: o.image = request.FILES['image']
        else: return JsonResponse({'success':False,'error':'Rasm yuklanmadi'},status=400)
        o.save()
        return JsonResponse({'success':True,'data':{'id':o.pk,'image':img(o,'image'),'caption':o.caption,'order':o.order}})
    data = [{'id':o.pk,'image':img(o,'image'),'caption':o.caption,'order':o.order} for o in event.images.all()]
    return JsonResponse({'success':True,'data':data})


@staff_only
@require_http_methods(['DELETE'])
def api_event_image_delete(request, pk):
    try: o = EventImage.objects.get(pk=pk)
    except EventImage.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    o.delete()
    return JsonResponse({'success':True})


@staff_only
def api_event_detail(request, pk):
    try: o = Event.objects.get(pk=pk)
    except Event.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        from django.utils.dateparse import parse_datetime
        d = request.POST
        for f in ['title','description','body','location']:
            if f in d: setattr(o,f,d[f])
        if 'event_date' in d: o.event_date = parse_datetime(d['event_date'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'image' in request.FILES: o.image = request.FILES['image']
        o.save()
        return JsonResponse({'success':True,'data':serialize_event(o)})
    return JsonResponse({'success':True,'data':serialize_event(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  FAQ
# ══════════════════════════════════════════════════════════════════════════════
@staff_only
def api_faqs(request):
    if request.method == 'POST':
        d = json.loads(request.body)
        o = FAQ(question=d['question'], answer=d['answer'],
                order=int(d.get('order',0)), is_active=d.get('is_active',True))
        o.save()
        return JsonResponse({'success':True,'data':{'id':o.pk,'question':o.question,'answer':o.answer,'order':o.order,'is_active':o.is_active}})
    items = [{'id':o.pk,'question':o.question,'answer':o.answer,'order':o.order,'is_active':o.is_active}
             for o in FAQ.objects.all()]
    return JsonResponse({'success':True,'data':items,'total':len(items)})


@staff_only
def api_faq_detail(request, pk):
    try: o = FAQ.objects.get(pk=pk)
    except FAQ.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = json.loads(request.body)
        if 'question' in d: o.question = d['question']
        if 'answer' in d: o.answer = d['answer']
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = bool(d['is_active'])
        o.save()
    return JsonResponse({'success':True,'data':{'id':o.pk,'question':o.question,'answer':o.answer,'order':o.order,'is_active':o.is_active}})


# ══════════════════════════════════════════════════════════════════════════════
#  Partner
# ══════════════════════════════════════════════════════════════════════════════
def serialize_partner(o):
    return {'id':o.pk,'name':o.name,'logo':img(o,'logo'),'website':o.website,'order':o.order,'is_active':o.is_active}


@staff_only
def api_partners(request):
    if request.method == 'POST':
        d = request.POST
        o = Partner(name=d['name'], website=d.get('website',''),
                    order=int(d.get('order',0)), is_active=d.get('is_active')=='true')
        if 'logo' in request.FILES: o.logo = request.FILES['logo']
        o.save()
        return JsonResponse({'success':True,'data':serialize_partner(o)})
    items, total, page, pages = paginate(Partner.objects.all(), request)
    return JsonResponse({'success':True,'data':[serialize_partner(o) for o in items],'total':total,'pages':pages})


@staff_only
def api_partner_detail(request, pk):
    try: o = Partner.objects.get(pk=pk)
    except Partner.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'DELETE':
        o.delete(); return JsonResponse({'success':True})
    if request.method == 'POST':
        d = request.POST
        for f in ['name','website']:
            if f in d: setattr(o,f,d[f])
        if 'order' in d: o.order = int(d['order'])
        if 'is_active' in d: o.is_active = d['is_active']=='true'
        if 'logo' in request.FILES: o.logo = request.FILES['logo']
        o.save()
        return JsonResponse({'success':True,'data':serialize_partner(o)})
    return JsonResponse({'success':True,'data':serialize_partner(o)})


# ══════════════════════════════════════════════════════════════════════════════
#  ContactMessage (read only)
# ══════════════════════════════════════════════════════════════════════════════
@staff_only
def api_messages(request):
    qs = ContactMessage.objects.all()
    if request.GET.get('status'): qs = qs.filter(status=request.GET['status'])
    items, total, page, pages = paginate(qs, request)
    data = [{'id':o.pk,'name':f"{o.first_name} {o.last_name}",'phone':o.phone,'email':o.email,
             'direction':o.direction,'message':o.message,'status':o.status,'created_at':dt(o,'created_at')}
            for o in items]
    return JsonResponse({'success':True,'data':data,'total':total,'pages':pages})


@staff_only
def api_message_detail(request, pk):
    try: o = ContactMessage.objects.get(pk=pk)
    except ContactMessage.DoesNotExist: return JsonResponse({'success':False,'error':'Topilmadi'},status=404)
    if request.method == 'POST':
        d = json.loads(request.body)
        if 'status' in d: o.status = d['status']; o.save()
    return JsonResponse({'success':True,'data':{
        'id':o.pk,'first_name':o.first_name,'last_name':o.last_name,
        'phone':o.phone,'email':o.email,'direction':o.direction,
        'message':o.message,'status':o.status,'created_at':dt(o,'created_at')}})


# ══════════════════════════════════════════════════════════════════════════════
#  Departments dropdown (for Teacher form)
# ══════════════════════════════════════════════════════════════════════════════
@staff_only
def api_departments_select(request):
    return JsonResponse({'success':True,'data':[{'id':o.pk,'name':o.name} for o in Department.objects.all()]})
