from django.urls import path
from draft.views import DraftView, CreateDraftView, CustomizedDraftView

app_name = "draft"

urlpatterns = [
    path("", DraftView.as_view(), name="draft"),
    path("create/", CreateDraftView.as_view(), name="create_draft"),
    path("customizedraft/<int:draft_id>/", CustomizedDraftView.as_view(), name="customizedraft"),
]
