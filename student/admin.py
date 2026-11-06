from django.contrib import admin

from .models import (
    UserStudyProfile,
    TopicExplanation,
    InterviewQuestionSet,
    Quiz,
    ChatMessage
)


admin.site.register(UserStudyProfile)
admin.site.register(TopicExplanation)
admin.site.register(InterviewQuestionSet)
admin.site.register(Quiz)
admin.site.register(ChatMessage)