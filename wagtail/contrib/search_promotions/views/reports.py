from django.utils.translation import gettext_lazy as _
from django_filters import DateFromToRangeFilter

from wagtail.admin.auth import permission_denied
from wagtail.admin.filters import DateRangePickerWidget, WagtailFilterSet
from wagtail.admin.ui.tables import Column
from wagtail.admin.views.reports import ReportView
from wagtail.contrib.search_promotions.models import Query


class SearchTermsReportFilterSet(WagtailFilterSet):
    created_at = DateFromToRangeFilter(
        label=_("Date"),
        field_name="daily_hits__date",
        widget=DateRangePickerWidget,
    )

    class Meta:
        model = Query
        fields = []


class SearchTermsReportView(ReportView):
    results_template_name = "wagtailsearchpromotions/search_terms_report_results.html"
    page_title = _("Search terms")
    header_icon = "search"
    is_searchable = True
    search_fields = ["query_string"]
    filterset_class = SearchTermsReportFilterSet
    index_url_name = "wagtailsearchpromotions:search_terms"
    index_results_url_name = "wagtailsearchpromotions:search_terms_results"
    columns = [
        Column("query_string", label=_("Search term(s)")),
        Column("_hits", label=_("Views")),
    ]
    export_headings = {
        "query_string": _("Search term(s)"),
        "_hits": _("Views"),
    }
    list_export = [
        "query_string",
        "_hits",
    ]

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_base_queryset()
        return kwargs

    def get_base_queryset(self):
        return Query.get_most_popular()

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)