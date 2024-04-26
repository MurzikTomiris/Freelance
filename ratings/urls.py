from django.urls import path

from ratings.views import RatingListView, RatingUpdateView

app_name = 'ratings'
urlpatterns = [
    path("all", RatingListView.as_view(), name="rating_list"),
    path("update/<int:order>/", RatingUpdateView.as_view(), name="rating_update"),
]