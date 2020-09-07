from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chat_home', views.chat_home, name='chat_home'),
    path('call_chatbot', views.call_chatbot, name='call_chatbot'),
    path('chat_catechism', views.chat_catechism, name='chat_catechism'),
    path('call_catechism_chatbot', views.call_catechism_chatbot, name='call_catechism_chatbot'),
    path('get_bible_paragraph', views.get_bible_paragraph, name='get_bible_paragraph'),
    path('contacts', views.contacts, name='contacts'),
    path('chat_conversations', views.chat_conversations, name='chat_conversations'),
    path('call_conversations_chatbot', views.call_conversations_chatbot, name='call_conversations_chatbot'),
    path('popup_chat_home', views.popup_chat_home, name='popup_chat_home'),
    path('popup_chat_catechism', views.popup_chat_catechism, name='popup_chat_catechism'),
    path('popup_chat_conversations', views.popup_chat_conversations, name='popup_chat_conversations'),
    path('intro_chatbot_service', views.intro_chatbot_service, name='intro_chatbot_service'),
    path('popup_chat_home_ishift', views.popup_chat_home_ishift, name='popup_chat_home_ishift'),
    path('call_ishift_chatbot', views.call_ishift_chatbot, name='call_ishift_chatbot'),
]