from django import forms
from newsletters.models import NewsletterRecipient, Message, Newsletter


class NewsletterRecipientForm(forms.ModelForm):
    class Meta:
        model = NewsletterRecipient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(NewsletterRecipientForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email получателя"})
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите ФИО получателя"}
        )
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Добавьте комментарий"})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Укажите тему письма"})
        self.fields["text"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст письма"})


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'finish_sending', 'comment', 'message', 'clients']
        labels = {
            'message': 'Выберите письмо',
            'clients': 'Выберите получателей рассылки',
        }

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control", "placeholder": "Введите название рассылки"})
        self.fields["finish_sending"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите дату окончания рассылки"}
        )
        self.fields["comment"].widget.attrs.update({"class": "form-control", "placeholder": "Добавьте комментарий", "style": "height: 100px;"})

        self.fields["message"].queryset = Message.objects.all()
        self.fields["message"].widget.attrs.update({"class": "form-control"})

        self.fields["clients"].queryset = NewsletterRecipient.objects.all()
        self.fields["clients"].widget.attrs.update({"class": "form-check", "style": "width: 400px;"})
