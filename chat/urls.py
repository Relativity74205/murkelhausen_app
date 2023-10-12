from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path("", views.start, name="start"),
    path("qa/", views.QAView.as_view(), name="qa"),
    path("chatsystem/", views.ChatSystemView.as_view(), name="chatsystem_list"),
    path("chatsystem/add/", views.AddChatSystemView.as_view(), name="chatsystem_add"),
    path(
        "chatsystem/<int:pk>/",
        views.UpdateChatSystemView.as_view(),
        name="chatsystem_update",
    ),
    path(
        "chatsystem/<int:pk>/delete",
        views.DeleteChatSystemView.as_view(),
        name="chatsystem_delete",
    ),
    path("call_openai_api/", views.call_openai_api, name="call_openai_api"),
]
