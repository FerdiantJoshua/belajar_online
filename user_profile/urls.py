from django.urls import path

from . import views

app_name = 'user_profile'
urlpatterns = [
    path('<username>', views.ProfileView.as_view(), name='profile'),
    # path('<teacher_username>/portfolio/', views.PortfolioListView.as_view(), name='portfolio'),
    path('<teacher_username>/portfolio/<int:pk>', views.PortfolioDetailView.as_view(), name='detail_portfolio'),
    path('portfolio/create', views.PortfolioCreateView.as_view(), name='create_portfolio'),
    path('<teacher_username>/portfolio/edit/<int:pk>', views.PortfolioUpdateView.as_view(), name='edit_portfolio'),
    path('<teacher_username>/portfolio/delete/<int:pk>', views.PortfolioDeleteView.as_view(), name='delete_portfolio'),
]
