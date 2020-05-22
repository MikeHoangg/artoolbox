from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from apps.core.forms import AnalyseForm
from apps.core.models import Image


class IndexView(TemplateView):
    template_name = 'core/index.html'


@method_decorator(csrf_exempt, name='dispatch')
class AnalyseView(FormView):
    http_method_names = ['post']
    form_class = AnalyseForm
    template_name = 'core/analyse.html'

    def form_invalid(self, form):
        context = self.get_context_data()

        context.update({
            'result': _("Failed to retrieve data")
        })
        return self.render_to_response(context)

    def form_valid(self, form):
        context = self.get_context_data()

        context.update({
            'result': form.get_analysis_result()
        })
        return self.render_to_response(context)


class ImageDetail(DetailView):
    model = Image
    template_name = 'core/image_detail.html'


class ImageListView(ListView):
    paginate_by = 6
    model = Image
    template_name = 'core/image_list.html'
    ordering = 'name'

    def get_queryset(self):
        queryset = super(ImageListView, self).get_queryset()
        search = self.request.GET.get('search', None)
        if search:
            return queryset.filter(Q(name__icontains=search) | Q(artist_icontains=search))
        return queryset
