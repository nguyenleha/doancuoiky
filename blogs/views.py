from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse

from NEWS_WEBAPP.forms import CommentForm, CustomPostForm
from blogs.models import Post, Comment


# Create your views here.
def home_view(request):
    object_list = Post.objects.all().order_by('-date')
    return render(request, 'home.html', {
        'object_list': object_list
    })


def about_view(request):
    return render(request, 'about.html')


class DetailPost(DetailView):
    model = Post
    template_name = 'detail_post.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_posts'] = Post.objects.all().order_by('-date')
        return context
    # def listbaipost(request):
    #     object_list_about = Post.objects.all().order_by('-date')
    #     return render(request, 'detail_post.html', {
    #         'object_list': object_list_about
    #     })


# def add_comment(request, pk):
#     if request.method == 'POST':
#         cmt_form = CommentForm(request.POST, instance=request.post.comments)
#         if cmt_form.is_valid():
#             cmt_form.save()
#             messages.success(request, 'Comment Added')
#             return redirect('detailpost')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         cmt_form = CommentForm(instance=request.post.comments)
#     return render(request, 'detail_post.html', {
#         'cmt_form': cmt_form,
#     })


class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CustomPostForm
    template_name = 'add_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Thêm bài viết thành công')
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = CustomPostForm
    success_message = 'Cập nhật bài viết thành công'
    template_name = 'update_post.html'


class DeletePost(DeleteView):
    model = Post
    template_name = 'detail_post.html'
    success_url = reverse_lazy('home')
    def get_success_url(self):
        messages.success(self.request, "Xóa bài thành công")
        return reverse('home')


class AddCommentPost(CreateView):
    model = Comment
    template_name = 'detailpost.html'
    fields = ('name', 'body')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.author = self.request.user
        messages.success(self.request, 'Thêm bình luận thành công')
        return super().form_valid(form)

    def get_success_url(self):
        postid = self.kwargs['pk']
        return reverse_lazy('detailpost', kwargs={'pk': postid})

def search_bar(request):
    if request.method == "POST":
        searched = request.POST['search']
        search_content = Post.objects.filter(title__icontains=searched)
        return render(request, 'search.html', {'searched': searched,'search_content':search_content})
    else:
        return render(request, 'search.html', {})

class DeleteComment(SuccessMessageMixin, DeleteView):
    model = Comment
    template_name = "detail_post.html"
    fields = ('author', 'name', 'body')

    def get_success_url(self):
        messages.success(self.request,"Xóa bình luận thành công")
        return reverse('detailpost', kwargs={'pk': self.object.post.pk})