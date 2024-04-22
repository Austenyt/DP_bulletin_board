from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView, DetailView

from board.forms import ReviewForm

from board.models import Advertisement, Review


class IndexView(TemplateView):      # Главная страница
    template_name = 'boards/index.html'
    extra_context = {
        'title': ''
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Advertisement.objects.all()[:3]
        return context_data


# class ContactsView(View):
#     template_name = 'board/contacts.html'
# 
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {'title': 'Контакты'})
# 
#     def post(self, request, *args, **kwargs):
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         print(f'{name} ({email}): {message}')
# 
#         return render(request, self.template_name, {'title': 'Контакты'})


class AdvertisementListView(ListView):   # Категории в главном выпадающем меню
    model = Advertisement
    extra_context = {
        'title': 'Категории'
    }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = get_categories(self.object.pk)
    #     return context


class ReviewListView(LoginRequiredMixin, ListView):   # Cписок товаров при нажатии "Открыть" в списке категорий
    model = Review

    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         category_id=self.kwargs.get('pk'),
    #         owner=self.request.user
    #     )

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(*args, **kwargs)
    #     category_item = Advertisement.objects.get(pk=self.kwargs.get('pk'))
    #     context_data['advertisement_pk'] = ad_item.pk
    #     context_data['title'] = f'Объявления {category_item.name}'
    #     return context_data


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    template_name = 'board/review_detail.html'
    context_object_name = 'review'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    success_url = reverse_lazy('board:index')

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации


class ReviewUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    permission_required = ['board.can_unpublish_Review', 'board.can_change_Review_description', 
                           'board.can_change_Review_category']

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('board:Review_update', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Review
    successful_url = reverse_lazy('board:contacts')

    def test_func(self):
        return self.request.user.is_authenticated  # Метод для определения авторизации пользователя

    def handle_no_permission(self):
        return LoginView.as_view(template_name='users/login.html')(self.request)  # Метод для возврата пользователя
        # на страницу авторизации при попытке доступа без авторизации
