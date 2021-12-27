from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from common.forms import UserForm
from pybo.models import Question, Answer

from django.db.models import Q, Count


# Create your views here.

def signup(request):
    # 계정생성
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password) # 인증
            login(request, user) # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, "common/signup.html", {'form':form})

def profile(request, user_id):
    context = {"user_id":user_id}
    return render(request, "common/profile.html", context)

def board(request, user_id):
    # URL에서 get parameter 가져오기
    page = request.GET.get("page", 1) # 페이지  If key 'page' does not exist, return 1 instead
    so = request.GET.get("so", "recent") # 정렬기준

    # 정렬 기준 정하기
    if so == "recommend":
        question_list = Question.objects.filter(author_id=user_id).annotate(num_voter=Count("voter")).order_by("-num_voter", "-create_date")       
    elif so == "popular":
        question_list = Question.objects.filter(author_id=user_id).annotate(num_answer=Count("answer")).order_by("-num_answer", "-create_date")
    else: # recent part
        question_list = Question.objects.filter(author_id=user_id).order_by("-create_date")
    
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {"question_list":page_obj, "page":page, "so":so, "user_id":user_id}    
    return render(request, "common/board.html", context)