from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from django.db.models import Q, Count

from ..models import Question, Answer

# Create your views here.
def index(request):
    # pybo 목록 출력
    # 입력 파라미터
    page = request.GET.get("page", 1) # 페이지  If key 'page' does not exist, return 1 instead
    kw = request.GET.get("kw", "") # 검색어
    so = request.GET.get("so", "recent") # 정렬기준
    # 조회
    if so == "recommend":
        question_list = Question.objects.annotate(num_voter=Count("voter")).order_by("-num_voter", "-create_date")
    elif so == "popular":
        question_list = Question.objects.annotate(num_answer=Count("answer")).order_by("-num_answer", "-create_date")
    else: # recent part
        question_list = Question.objects.order_by("-create_date")
    # question_list = Question.objects.order_by("-create_date")
    
    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(author__username__icontains=kw) | # 글쓴이 검색
            Q(answer__author__username__icontains=kw) # 답변자 검색
        ).distinct()
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {"question_list":page_obj, "page":page, "kw":kw, "so":so}
    return render(request, "pybo/question_list.html", context)

# pybo 상세 내용 출력
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    so = request.GET.get('so', 'popular') # 정렬기준
  
    # 정렬
    if so == 'recommend':
        answer_list = question.answer_set.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        answer_list = question.answer_set.annotate(num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:  # recent
        answer_list = question.answer_set.order_by('-create_date')    
    
    # answer_list 넘기기 1차 시도
    # page = request.GET.get("page", 1) # 페이지  If key 'page' does not exist, return 1 instead
    # answer_list = Question.answer_set
    
    # paginator = Paginator(answer_list, 5)
    # page_obj = paginator.get_page(page)
    
    # context = {"question": question, "answer_list":page_obj}
    
    # answer_list 넘기기 2차 시도
    # answer_list = question.answer_set
    # paginator = Paginator(answer_list, 5)
    # context = {"question": question, "answer_list":paginator}

    # answer_list 넘기기 3차 시도
    page = request.GET.get("page", 1)
    # answer_list = question.answer_set.all()
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)
    context = {"question": question, "answer_list":page_obj}    

    # context = {"question": question}
    return render(request, "pybo/question_detail.html", context)