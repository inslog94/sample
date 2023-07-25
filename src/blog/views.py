from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Tag, Comment
from .forms import PostForm, TagForm, CommentForm


class Index(View):
    def get(self, req):
        posts = Post.objects.all().order_by('-pk')
        tags = Tag.objects.all()
        comments = Comment.objects.all().order_by('-pk')
        context = {
            "posts": posts,
            "tags": tags,
            "comments": comments[:3],
        }
        
        return render(req, "blog/post_list.html", context)
    

class PostDetail(View):
    def get(self, req, pk):
        # post = Post.objects.get(pk=pk)
        # print(post)
        post = get_object_or_404(Post, pk=pk)
        print(post)
        
        if post.is_deleted:
            return render(req, "blog/post_deleted.html")
        
        # comments = Comment.objects.select_related('post').filter(post=post)
        comments = post.comment_set.all()
        print('comments', comments)
        
        comment_form = CommentForm()
        
        # tags = Tag.objects.select_related('post').filter(post__pk=pk)
        tags = post.tags.all()
        print("tags", tags)
        context = {
            "post": post,
            "tags": tags,
            "comments": comments,
            "comment_form": comment_form,
        }
        
        return render(req, "blog/post_detail.html", context)


class Search(View):
    def get(self, req):
        query = req.GET.get('name')
        print(query)
        posts = Post.objects.filter(title__contains=query)
        print(posts)
        context = {
            "query": query,
            "posts": posts
        }
        
        return render(req, 'blog/post_search.html', context)
    

class TagSearch(View):
    def get(self, req):
        query = req.GET.get('name')
        print(query)
        tag = Tag.objects.get(content=query)
        posts = tag.post_set.all()
        print(posts)
        context = {
            "query": query,
            "posts": posts
        }
        
        return render(req, 'blog/post_search.html', context)

    
class PostDelete(LoginRequiredMixin, View):
    def post(self, req, pk):
        post = Post.objects.get(pk=pk)
        print("delete", post)
        post.is_deleted = True
        post.save()
        
        return redirect('blog:list')
    
    
class PostWrite(LoginRequiredMixin, View):
    def get(self, req):
        form = PostForm()
        tagForm = TagForm()
        context = {
            'form': form,
            'tagForm': tagForm
        }
        
        return render(req, "blog/post_form.html", context)
    
    def post(self, req):
        post_form_data = {
            "title": req.POST.get("title"),
            "content": req.POST.get("content"),
        }
        
        form = PostForm(data=post_form_data)
        
        tag_form_data = {
            "content": req.POST.get("tags")
        }
        
        tag_form = TagForm(data=tag_form_data)
        if form.is_valid() and tag_form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            writer = req.user
            post = Post(title=title, content=content, writer=writer)
            post.save()
            
            form_content = tag_form.cleaned_data['content']
            tags = []
            if form_content:
                form_content = form_content.split(",")
                if tag_form:
                    print(form_content)
                    for i in form_content:
                        tag, created = Tag.objects.get_or_create(content=i)
                        tags.append(tag)
            post.tags.set(tags)
        
            return redirect('blog:list')


class PostUpdate(LoginRequiredMixin, View):
    def get(self, req, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(initial={'title': post.title, 'content': post.content})
        tags = post.tags.all()
        context = {
            'content': post.content,
            'form': form,
            'post': post,
            'tags': tags,
        }
        
        return render(req, 'blog/post_edit.html', context)
    
    def post(self, req, pk):
        post = Post.objects.get(pk=pk)
        post_form_data = {
            "title": req.POST.get("title"),
            "content": req.POST.get("content"),
        }
        
        form = PostForm(data=post_form_data)
        
        tag_form_data = {
            "content": req.POST.get("tags")
        }
        
        print(req.POST.get("tags"))
        tag_form = TagForm(data=tag_form_data)
        if form.is_valid() and tag_form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            
            form_content = tag_form.cleaned_data['content']
            tags = []
            post.tags.all().delete()
            if form_content:
                form_content = form_content.split(",")
                if tag_form:
                    print("clean", form_content)
                    for i in form_content:
                        tag, created = Tag.objects.get_or_create(content=i)
                        tags.append(tag)
            post.tags.set(tags)
        
            return redirect('blog:list')


class CommentWrite(View):
    def post(self, req, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm(req.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            writer = req.user
            print("댓글 작성자", writer)

            if not req.user.is_authenticated:
                print("익명입니다")
                comment = Comment.objects.create(post=post, content=content, writer=None)
            else:
                comment = Comment.objects.create(post=post, content=content, writer=writer)

            return redirect('blog:detail', pk=pk)


class CommentDelete(View):
    def post(self, req, pk):
        comment = Comment.objects.get(pk=pk)
        post_id = comment.post.id
        comment.delete()
        
        return redirect('blog:detail', pk=post_id)