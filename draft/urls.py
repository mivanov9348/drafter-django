from django.urls import path
from .views import customize_draft, create_draft, drafts_list, delete_draft, add_wrestler_to_brand, auto_pick, \
    finalize_draft

app_name = 'draft'

urlpatterns = [
    path('customize/', customize_draft, name='customize_draft'),
    path('draft/<int:draft_id>/', create_draft, name='create_draft'),
    path('add-wrestler/', add_wrestler_to_brand, name='add_wrestler'),
    path('draft/auto-pick/<int:draft_id>/', auto_pick, name='auto_pick'),
    path('draft/finalize/<int:draft_id>/', finalize_draft, name='finalize_draft'),
    path('list/', drafts_list, name='list_drafts'),
    path('delete/<int:draft_id>/', delete_draft, name='delete_draft'),

]
