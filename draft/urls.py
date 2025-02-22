from django.urls import path
from .views import customize_draft, create_draft, drafts_list, delete_draft, add_wrestler_to_brand, \
    finalize_draft, auto_pick_wrestler, save_draft, edit_draft

app_name = 'draft'

urlpatterns = [
    path('customize/', customize_draft, name='customize_draft'),
    path('draft/<int:draft_id>/', create_draft, name='create_draft'),
    path('add-wrestler/', add_wrestler_to_brand, name='add_wrestler'),
    path('auto-pick/<int:draft_id>/', auto_pick_wrestler, name='auto_pick'),
    path('draft/finalize/<int:draft_id>/', finalize_draft, name='finalize_draft'),
    path('save/<int:draft_id>/', save_draft, name='save_draft'),
    path('edit/<int:draft_id>/', edit_draft, name='edit_draft'),
    path('list/', drafts_list, name='list_drafts'),
    path('delete/<int:draft_id>/', delete_draft, name='delete_draft'),

]
