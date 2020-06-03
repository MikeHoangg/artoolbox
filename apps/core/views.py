from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView, FormView
from django.contrib.staticfiles.templatetags.staticfiles import static

from apps.core.forms import AnalyseForm
from apps.core.models import Image, Tool


class IndexView(TemplateView):
    template_name = 'core/index.html'


class ToolsSerializerMixin:
    """
    Mixin for parsing tools into a certain structure
    """
    TOOL_IMAGES = {
        Tool.PENCIL: static('img/pencil.svg'),
        Tool.PEN: static('img/pen.svg'),
        Tool.BRUSH: static('img/brush.svg'),
        Tool.PAINT: static('img/palette.svg'),
        Tool.PASTEL: static('img/pastel.svg'),
        Tool.CHARCOAL: static('img/charcoal.svg'),
    }

    def serialize_tools(self, tools):
        recommended_tools = []
        for tool_type in Tool.TYPE_CHOICES:
            selected_tools = tools.filter(tool_type=tool_type[0])
            if selected_tools.exists():
                tmp = {
                    'name': tool_type[1],
                    'tools': selected_tools,
                    'img': self.TOOL_IMAGES[tool_type[0]]
                }
                recommended_tools.append(tmp)
        return recommended_tools


@method_decorator(csrf_exempt, name='dispatch')
class AnalyseView(FormView, ToolsSerializerMixin):
    """
    View for analysing image
    """
    http_method_names = ['post']
    form_class = AnalyseForm
    template_name = 'core/analyse.html'

    def form_valid(self, form):
        context = self.get_context_data()
        colours, tools = form.get_analysis_result()

        context.update({
            'colours': colours,
            'recommended_tools': self.serialize_tools(tools)
        })

        return self.render_to_response(context)


class ImageDetail(DetailView, ToolsSerializerMixin):
    """
    View for detailed image page
    """
    model = Image
    template_name = 'core/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ImageDetail, self).get_context_data(**kwargs)
        toolset = self.object.toolset
        if toolset:
            tools = toolset.tools.all().prefetch_related('materials')
            context['recommended_tools'] = self.serialize_tools(tools)
        return context


class ImageListView(ListView):
    """
    View for image list
    """
    paginate_by = 6
    model = Image
    template_name = 'core/image_list.html'
    ordering = 'name'

    def get_queryset(self):
        queryset = super(ImageListView, self).get_queryset()
        search = self.request.GET.get('search', None)
        if search:
            return queryset.filter(Q(name__icontains=search) | Q(artist__icontains=search))
        return queryset
