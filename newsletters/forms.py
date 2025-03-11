from django import forms
from newsletters.models import NewsletterRecipient, Message


class NewsletterRecipientForm(forms.ModelForm):
    class Meta:
        model = NewsletterRecipient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NewsletterRecipientForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email получателя'})
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите ФИО получателя'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Добавьте комментарий'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите тему письма'})
        self.fields['text'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите текст письма'})
