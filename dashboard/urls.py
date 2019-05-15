from django.conf.urls import url

from dashboard.views import DashboardsApiView, DashboardDetailApiView, FavoriteDashboards
from dashboard.views import ChartsApiView, ChartDetailApiView

# Urls para la app graph_types
urlpatterns = [
    url('dashboards', DashboardsApiView.as_view(), name='dashboards'),
    url('favorite', FavoriteDashboards.as_view(), name='favorite_dashboards'),
    url('dashboard_detail/(?P<pk>[\w:|-]+)/', DashboardDetailApiView.as_view()),
    url('charts', ChartsApiView.as_view(), name='charts'),
    url('chart_detail/(?P<pk>[\w:|-]+)/', ChartDetailApiView.as_view()),
]
