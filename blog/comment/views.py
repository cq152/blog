from django.shortcuts import redirect
from django.views.generic import TemplateView

from comment.forms import CommentForm


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.author = request.user.username
            instance.email = request.user.email
            instance.site = '/author/' + str(request.user.id)
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target
        }

        return self.render_to_response(context)
