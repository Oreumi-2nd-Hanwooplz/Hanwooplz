from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

def index(request):
    return render(request, 'index.html')

# 게시글 작성 화면
def write(request):
    return render(request, 'write.html')
    
# 게시글 수정 화면
# def edit(request, id):
#     post = get_object_or_404(Post, id=id)
#     if post:
#         post.description = post.description.strip()
#     if request.method == "POST":
#         post.title = request.POST['title']
#         post.description = request.POST['description']
#         post.save()
#         return redirect('hanwooplz_app:trade_post', pk=id)

#     return render(request, 'write.html', {'post': post})

def current_chat(request):
    return render(request, 'chat.html')
