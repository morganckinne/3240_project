from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
import requests
from .models import ClassSubject, Post, Profile, Thread, Message
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
import re
#note

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'testapp/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.all()

class PostCreate(LoginRequiredMixin, generic.TemplateView):
    model = Post
    template_name = 'testapp/post_form.html'

def createPost(request):
    try:
        if request.POST['post_title']=="" or request.POST['post_text']=="" or request.POST['associated_dept']=="" or request.POST['course_id']=="":
            return render(request,'testapp/post_form.html', {
            'error_message': "You didn't fill in an input.",
            })
        else:
            Post.objects.create(post_title=request.POST['post_title'],
                                post_text=request.POST['post_text'],
                                book_ISBN=request.POST['book_ISBN'],
                                associated_dept=request.POST['associated_dept'],
                                course_id=request.POST['course_id'],
                                post_creator=request.user)
    except(KeyError, ):
        return render(request,'testapp/post_form.html', {
            'error_message': "You didn't fill in an input.",
        })
    else:
        return HttpResponseRedirect(reverse('testapp:index'))

def createPostFromClass(request, dept, id):
    context = {
        'associated_dept': dept,
        'course_id' : id
    }
    return render(request, 'testapp/post_form.html', context)

class ClassSubjectCreate(LoginRequiredMixin, CreateView):
    model = ClassSubject
    # success_url = 'course'
    fields = ['class_subject']

    # def get_context_data(self, **kwargs):
    #     content = super().get_context_data(**kwargs)
    #     response = requests.get('https://luthers-list.herokuapp.com/api/deptlist?format=json')
    #     classdata = response.json()
    #     # for item in classdata:
    #     #     print(list(item.values()))
    #     #print(classdata)
    #     #print({'subject':classdata})
    #     return ({'subject':classdata})

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['class_subject'] = self.request.POST['class_subject']
        return response

    # def listCreate(request):
    #     subject = request.session.get('class_subject')
    #     response = requests.get('http://luthers-list.herokuapp.com/api/deptlist?format=json')
    #     classdata = response.json()
    #     print(classdata)
    #     return render(request, 'testapp/classsubject.html', {'subject':classdata[0]['subject']})

def course(request):
    # Find a way to take this as input
    # code = request.POST.get('class_subject', '')
    # try:
    #     coursedata = ClassSubject.objects.get(class_subject = code)
    #     subject = coursedata.class_subject
    # except ClassSubject.DoesNotExist:
    #     subject = "CS"
    subject = request.session.get('class_subject')
    response = requests.get('https://luthers-list.herokuapp.com/api/dept/' + subject + '/?format=json')
    classdata = response.json()
    #print(classdata)
    return render(request, 'testapp/course.html', {'classdata':classdata})

def favorite_post(request, fav_id):
    postObj = get_object_or_404(Post, id=fav_id)
    postObj.favorite.add(request.user)
    return redirect('testapp:index')

def favorite_post_from_search(request, fav_id):
    postObj = get_object_or_404(Post, id=fav_id)
    postObj.favorite.add(request.user)
    return redirect('testapp:search')

def remove_favorite(request, fav_id):
    postObj = get_object_or_404(Post, id=fav_id)
    postObj.favorite.remove(request.user)
    return redirect('testapp:index')
    
def remove_favorite_from_fav(request, fav_id):
    '''
    Removes a favorite specificially from the favorites page
    '''
    postObj = get_object_or_404(Post, id=fav_id)
    postObj.favorite.remove(request.user)
    return redirect('testapp:favorites')

def remove_favorite_from_search(request, fav_id):
    '''
    Removes a favorite specificially from the search for posts page
    '''
    postObj = get_object_or_404(Post, id=fav_id)
    postObj.favorite.remove(request.user)
    return redirect('testapp:search')

class FavoritesView(LoginRequiredMixin, generic.ListView):
    template_name = 'testapp/favorites.html'
    #context_object_name = 'post_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(favorite=self.request.user)
        else:
            return None

class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'testapp/profile.html'
    def get_queryset(self):
        return Profile.objects.all()

# class UpdateProfile(UpdateView):
#     model = Profile
#     fields = ['name', 'year', 'major']
#     template_name = 'testapp/update_profile.html'
    # def get_object(self, *args, **kwargs):
    #     user = get_object_or_404(User, pk=self.kwargs['pk'])

#     def get_success_url(self, *args, **kwargs):
#         return redirect('testapp:profile')

class UpdateProfileView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'testapp/update_profile.html'
    context_object_name = 'profile'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Profile.objects.get(user=user)

def updateProfile(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
        Profile.objects.filter(user=user).update(name=request.POST['name'], year=request.POST['year'], major=request.POST['major'])
    except(KeyError, ):
        return render(request, 'testapp/update_profile.html', {
            'error_message': "Please fill out all inputs",
        })
    else:
        return HttpResponseRedirect(reverse('testapp:profile'))

class ThreadList(LoginRequiredMixin, generic.ListView):
    template_name = 'testapp/thread_list.html'
    context_object_name = 'thread_list'

    def get_queryset(self):
        return Thread.objects.filter(Q(user1=self.request.user) | Q(user2=self.request.user))

class ThreadCreate(LoginRequiredMixin, generic.TemplateView):
    model = Thread
    template_name = 'testapp/create_thread.html'

def createThread(request):
    try:
        if User.objects.filter(username=request.POST['reciever']).exists():
            if request.POST['subject'] != "":
                Thread.objects.create(user1=User.objects.get(username=request.POST['reciever']), user2=request.user, subject_text=request.POST['subject'])
            else:
                Thread.objects.create(user1=User.objects.get(username=request.POST['reciever']), user2=request.user)
        else:
            return render(request, 'testapp/create_thread.html', {
                'error_message': "Please enter a valid username.",
            })
    except(KeyError, ):
        return render(request,'testapp/create_thread.html', {
            'error_message': "You didn't fill in an input.",
        })
    else:
        return HttpResponseRedirect(reverse('testapp:threads'))

class addNewFriend(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'testapp/add_friend.html'
    context_object_name = 'profile'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return Profile.objects.get(user=user)

#working on this
def addFriend(request,pk):
    try:
        userObj = get_object_or_404(User,pk=pk)
        if User.objects.filter(username=request.POST['reciever']).exists():
            print('COOL!!!!!!!!!!!!!!!!!')
            buddy = User.objects.filter(username=request.POST['reciever']).first()
            userObj.profile.friends.add(buddy)
        else:
            return render(request, 'testapp/add_friend.html', {
                'error_message': "Please enter a valid username",
            })
    except(KeyError, ):
        return render(request,'testapp/add_friend.html', {
            'error_message': "No username was inputed.",
        })
    else:
        return HttpResponseRedirect(reverse('testapp:profile'))

class ThreadView(LoginRequiredMixin, generic.ListView):
    template_name = 'testapp/thread_view.html'
    context_object_name = 'message_list'

    def get_queryset(self):
        return Message.objects.filter(thread__pk__contains=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadView, self).get_context_data(*args, **kwargs)
        context['thread_pk'] = self.kwargs['pk']
        threadObj = get_object_or_404(Thread, pk=self.kwargs['pk'])
        if threadObj.user1 != self.request.user:
            context['thread_username'] = threadObj.user1.username
        else:
            context['thread_username'] = threadObj.user2.username
        return context

def createMessage(request, pk):
    try:
        threadObj = get_object_or_404(Thread, pk=pk)
        if request.POST['message'] == "":
            messages = Message.objects.filter(thread__pk__contains=pk)
            if threadObj.user1 != request.user:
                return render(request,'testapp/thread_view.html', {
                'error_message': "You didn't fill in a message.",
                'thread_pk': pk,
                'thread_username': threadObj.user1.username,
                'message_list': messages
                })
            else:
                return render(request,'testapp/thread_view.html', {
                'error_message': "You didn't fill in a message.",
                'thread_pk': pk,
                'thread_username': threadObj.user2.username,
                'message_list': messages
                })
        if threadObj.user1 != request.user:
            Message.objects.create(thread=threadObj, sender=request.user, receiver=threadObj.user1, message_text=request.POST['message'])
        else:
            Message.objects.create(thread=threadObj, sender=request.user, receiver=threadObj.user2, message_text=request.POST['message'])
    except(KeyError, ):
        return render(request,'testapp/thread_view.html', {
            'error_message': "You didn't fill in a message.",
            'thread_pk': pk
        })
    else:
        return HttpResponseRedirect(reverse('testapp:thread_view', kwargs={'pk': pk}))

# def search(request):
#     template_name = 'testapp/index.html'
#     context_object_name = 'post_list'
#     query = request.GET.get('q')
#     if query:
#         results = Post.objects.filter(Q(post_title__icontains=query) | Q(post_text__icontains=query) | Q(book_ISBN__icontains=query) | Q(associated_dept__icontains=query) | Q(course_id__icontains=query))
#     else:
#         results = Post.objects.filter()
#     return render(request, template_name)

class searchView(LoginRequiredMixin, generic.ListView):
    template_name = 'testapp/post_search.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        # print(query)
        if query:
            query
            query_no_spaces = query.replace(" ", "")
            # course_info.group(1) contains class dept, course_info.group(2) contains class id
            course_info = re.search('([A-Za-z][A-Za-z]+)(\d+)', query_no_spaces)
            if course_info: # If a potential class dept and id are found
                post_list = Post.objects.filter(Q(associated_dept__icontains=query) | Q(post_title__icontains=query) | Q(post_text__icontains=query) | Q(book_ISBN__icontains=query) | Q(associated_dept__icontains=query) | Q(course_id__icontains=query) | 
                (Q(associated_dept__icontains=course_info.group(1)) & Q(course_id__icontains=course_info.group(2))))
            else:
                post_list = Post.objects.filter(Q(associated_dept__icontains=query) | Q(post_title__icontains=query) | Q(post_text__icontains=query) | Q(book_ISBN__icontains=query) | Q(associated_dept__icontains=query) | Q(course_id__icontains=query))
            # print(post_list)
            return post_list
        else:
            # print("reached")
            return None


