from django.forms import ModelForm, HiddenInput
from .models import BlogComment, BottomComment
from ckeditor.fields import CKEditorWidget

class BlogCommentForm(ModelForm):
    class Meta:
        model = BlogComment
        fields = ['comment', 'followed_blog']
        widgets = {
            'comment': CKEditorWidget,
        }

class BottomCommentForm(ModelForm):
    class Meta:
        model = BottomComment
        fields = ['comment', 'followed_comment', 'followed_self']
        widgets = {
            'followed_comment': CKEditorWidget,
            'followed_self': CKEditorWidget,
        }