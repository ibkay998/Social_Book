from site import USER_BASE
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Post,LikePost,FollowersCount
from django.contrib.auth.decorators import login_required
from itertools import chain

@login_required(login_url='login')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    user_following_list=[]
    feed=[]
    user_following = FollowersCount.objects.filter(signed_in_following = request.user.username)
    print(user_following)
    for user in user_following:
        user_following_list.append(user)
    for username in user_following_list:
        feed_lists = Post.objects.filter(user=username)
        feed.append(feed_lists)
    
    feed_lists=list(chain(*feed))
    print(feed_lists)
    print(feed)
    return render(request,'index.html',{'user_profile':user_profile,'posts':feed_lists})


@login_required(login_url='login')
def follow(request):
    if request.method =='POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowersCount.objects.filter(signed_in_following = follower,user = user).first():
            delete_follower = FollowersCount.objects.get(signed_in_following = follower, user = user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(signed_in_following = follower, user = user)
            new_follower.save()
            return redirect('/profile/'+user)
        
    else:
        return redirect('/')


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




@login_required(login_url='login')
def profile(request,pk):
    follower = request.user.username
    user = pk
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_length = len(user_post)
    if FollowersCount.objects.filter(signed_in_following = follower,user=user):
        button_text = "UnFollow"
    else:
        button_text = "Follow"
    context = {
        'user_object': user_object,
        'user_profile':user_profile,
        'user_posts': user_post,
        'user_post_length':user_post_length,
        "button_text":button_text
    }
    return render(request,'profile.html',context)

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



# Create your views here.
