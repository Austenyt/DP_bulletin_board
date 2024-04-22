from django import forms

from board.models import Review


class StyleFormMixin:
    """
        Миксин для добавления стилей к полям формы.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ReviewForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'author', 'ad', 'created_at',)
