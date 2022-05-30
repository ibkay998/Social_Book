from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Post,LikePost
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all()
    # template = loader.get_template('./templates/index.html')
    # context = {
    #     'latest_question_list': 2,
    # }
    return render(request,'index.html',{'user_profile':user_profile,'posts':posts})

@login_required(login_url='login')
def like_post(request):
    username=request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id = post_id,username=username).first()
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes +=1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')





def profile(request,pk):
    return render(request,'profile.html')

@login_required(login_url='login')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect('index')
    else:
        return redirect('index')
    # template = loader.get_template('./templates/index.html')
    # context = {
    #     'latest_question_list': 2,
    # }
    

@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            bio = request.POST.get('bio', "ibk is good")
            location = request.POST.get('location',"nigeria")

            user_profile.profile_img=image
            user_profile.bio=bio
            user_profile.location = location
            user_profile.save()


        if request.FILES.get('image') != None:
            image=request.FILES.get('image')
            bio = request.POST.get('bio', "ibk is good")
            location = request.POST.get('location',"nigeria")

            user_profile.profile_img=image
            user_profile.bio=bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')
    return render(request,'setting.html',{'user_profile':user_profile})

def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Credentials Incvalid')
            return redirect('login')
    return render(request,'signin.html')

def register(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request,'Password Not matching')
            return redirect('register')

        pass

    return render(request,'register.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')

# Create your views here.
