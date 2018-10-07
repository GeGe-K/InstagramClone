from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Image,Profile,Likes,Comment
from django.contrib.auth import login, authenticate
from .forms import SignupForm,ImageForm,CommentForm,ProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block

@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    images = Image.objects.all()
    comments = Comment.objects.all()
    likes = Likes.objects.all
    profile = Profile.objects.all()
    return render(request,'index.html',locals())


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Instagram account.'
            message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.''<a href="/accounts/login/"> click here </a>')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required(login_url='accounts/login/')
def add_new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            add=form.save(commit=False)
            add.profile = current_user
            add.save()
            return redirect('indexpage')
    else:
        form = ImageForm()


    return render(request,'post.html',locals())

@login_required(login_url='/login')
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile =form.save(commit=False)
            profile.user = current_user
            profile.save()
    else:
        form=ProfileForm()

    return render(request, 'profile/new_profile.html', locals())

@login_required(login_url='/accounts/login/')
def view_profile(request, id):
    searched_user=User.objects.filter(id=id).first()
    profile = searched_user.profile
    details = Profile.get_profile_by_id(id)
    images = Image.get_images_on_profile(id)

    users = User.objects.get(id=id)
    follower = len(Follow.objects.followers(users))
    following = len(Follow.objects.following(users))
    app_users=User.objects.all()
    guys_following=Follow.objects.following(request.user)

    return render(request,'profile/user_profile.html',locals())


def search(request):
    profile_info = User.objects.all()

    if 'username' in request.GET and request.GET['username']:
        search_term = request.GET.get('username')
        search_results = User.objects.filter(username__icontains=search_term)
        print(search_results)

        return render(request,'search.html',locals())

    return redirect(index)

def comment(request,image_id):
    current_user=request.user
    image = Image.objects.get(id=image_id)
    profile_user = User.objects.get(username=current_user)
    the_comments = Comment.objects.all()
    print(the_comments)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_itself = form.save(commit=False)
            comment_itself.image = image
            comment_itself.commenter = request.user
            
            comment_itself.save()

            print(the_comments)


        return redirect(index)

    else:
        form = CommentForm()

    return render(request, 'comment.html', locals())

def follow(request,user_id):
    users=User.objects.get(id=user_id)
    follow = Follow.objects.add_follower(request.user, users)

    return redirect('/profile/', locals())

def like(request, image_id):
    current_user = request.user
    liked_image=Image.objects.get(id=image_id)
    new_like,created= Likes.objects.get_or_create(who_liked=current_user, liked_image=liked_image)
    new_like.save()

    return redirect('indexpage')

# def images(request):
#   '''
#   View function that queries the database and returns images added
#   '''
#   pictures = Image.get_all_images()

#   return render(request,'index.html',{"pictures":pictures})