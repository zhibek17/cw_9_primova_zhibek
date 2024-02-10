# views.py
from audioop import reverse

from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import AnnouncementForm, CommentForm
from .models import Announcement, Comment


class IndexView(ListView):
    model = Announcement
    template_name = 'announcements/index.html'
    context_object_name = 'announcements'
    queryset = (Announcement.objects.filter(status='published'))
    ordering = ('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = 1
        return context


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'announcement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.pk
        return context

class AnnouncementCreateView(CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'announcements/announcement_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class AnnouncementUpdateView(UpdateView):
    model = Announcement
    template_name = 'announcements/announcement_update.html'
    fields = ['title', 'description', 'author', 'category', 'price', 'image']
    success_url = reverse_lazy('index')


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'announcements/announcement_delete.html'
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'delete'
        self.object.save()
        return redirect(self.get_success_url())





class CommentCreateView(CreateView):
    template_name = 'comments/comment_create.html'
    model = Comment
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context

    def form_valid(self, form):
        announcement = get_object_or_404(Announcement, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.announcement = announcement
        comment.author = self.request.user
        comment.save()
        return redirect('announcement_detail', pk=announcement.pk)



# class CommentUpdateView(UpdateView):
#     template_name = 'comments/comment_update.html'
#     model = Comment
#     form_class = CommentForm
#     permission_required = 'webapp.change_comment'
#
#     def has_permission(self):
#         return super().has_permission() or self.request.user == self.get_object().author
#
#     def get_success_url(self):
#         return reverse('webapp:article_view', kwargs={'pk': self.object.article.pk})


class CommentDeleteView(DeleteView):
    model = Comment
    permission_required = 'webapp.comment_delete'

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object().author

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:announcement_detail', kwargs={'pk': self.object.announcement.pk})
