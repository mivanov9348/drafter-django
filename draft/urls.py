from django.urls import path
from .views import customize_draft, create_draft, drafts_list, delete_draft

app_name = 'draft'

urlpatterns = [
    path('customize/', customize_draft, name='customize_draft'),
    path('create/<int:draft_id>/', create_draft, name='create_draft'),
    path('list/', drafts_list, name='list_drafts'),
path('delete/<int:draft_id>/', delete_draft, name='delete_draft'),

]
