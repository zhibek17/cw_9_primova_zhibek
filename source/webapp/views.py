from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Announcement, Comment
from .forms import AnnouncementForm, CommentForm

class IndexView(ListView):
    model = Announcement
    template_name = 'announcements/index.html'
    context_object_name = 'announcements'
    queryset = Announcement.objects.filter(status='published')
    ordering = ('-published_at')

class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcements/announcement_detail.html'
    context_object_name = 'announcement'

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
        self.object.status = 'deleted'
        self.object.save()
        return redirect(self.get_success_url())

class CommentCreateView(CreateView):
    template_name = 'comments/comment_create.html'
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        announcement = get_object_or_404(Announcement, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.announcement = announcement
        comment.author = self.request.user
        comment.save()
        return redirect('announcement_detail', pk=announcement.pk)

class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('announcement_detail', kwargs={'pk': self.object.announcement.pk})
