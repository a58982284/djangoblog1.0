import sys
from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post

from.models import Comment
from.forms import CommentForm

# Create your views here.
def post_comment(request, post_pk):
    post = get_object_or_404(Post,pk=post_pk)


    if request.method == 'POST':
        #用户提交的数据存在request.POST中，这是一个类字典对象
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            #comment 和 post 是一对多的关系，model 中用 foreignkey 关联。可以通过 comment.post 引用与这个 comment 关联的 post，也可以设置新的关联关系。
            comment.post = post
            comment.save()

            return redirect(post)

        else:
            comment_list = post.comment_set.all()
            context ={'post':post,
                      'form':form,
                      'comment_list':comment_list
                      }
            return render(request,'blog/detail.html',context=context)
    return redirect(post)