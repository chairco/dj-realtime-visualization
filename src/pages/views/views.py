# pages/views.py
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from rest_framework import viewsets

from pages.serializers import UserSerializer, GroupSerializer
from pages.models import Blog
from pages.forms import BlogForm


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(
            self.get_context_data(
                form=form
            )
        )

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def form_valid(self, request, form):
        blog = form.save(commit=False)

        try:
            user_is_authenticated = request.user.is_authenticated()
        except TypeError:
            user_is_authenticated = request.user.is_authenticated

        if user_is_authenticated:
            blog.owner = request.user
        self.object = form.save()

        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class BlogCreateView(FormsetMixin, CreateView):
    template_name = 'pages/blog_formset.html'
    model = Blog
    form_class = BlogForm

    @method_decorator(permission_required('pages.delete_blog', login_url='/403/'))
    def dispatch(self, *args, **kwargs):
        return super(BlogCreateView, self).dispatch(*args, **kwargs)


class BlogUpdateView(FormsetMixin, UpdateView):
    template_name = 'pages/blog_formset.html'
    is_update_view = True
    model = Blog
    form_class = BlogForm

    @method_decorator(permission_required('pages.delete_blog', login_url='/403/'))
    def dispatch(self, *args, **kwargs):
        return super(BlogUpdateView, self).dispatch(*args, **kwargs)


class index(ListView):
    template_name = 'index.html'
    model = Blog
    paginate_by = 2


class BlogDetail(DetailView):
    model = Blog

    def get_context_data(self, *args, **kwargs):                                       
        context = super(BlogDetail, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = super(BlogDetail, self).get_object(queryset=queryset)
        obj.update_counter()
        return obj

    # (TODO) solving Manager isn't accessible via Blog instances
    #def get(self, request, *args, **kwargs):
    #    article = kwargs.get('pk')
    #    Blog.objects.update_counter(article)
    #    self.object = self.get_object()
    #    context = self.get_context_data(object=self.object)
    #    return self.render_to_response(context)

