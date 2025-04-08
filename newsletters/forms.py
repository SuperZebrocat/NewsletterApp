from datetime import datetime, time

from django import forms

from newsletters.models import Message, Newsletter, NewsletterRecipient


class NewsletterRecipientForm(forms.ModelForm):
    class Meta:
        model = NewsletterRecipient
        fields = "__all__"
        exclude = ("owner",)

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
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({"class": "form-control", "placeholder": "Укажите тему письма"})
        self.fields["text"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст письма"})


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["title", "finish_sending", "comment", "message", "clients"]
        labels = {
            "message": "Выберите письмо",
            "clients": "Выберите получателей рассылки",
        }

    def __init__(self, *args, user=None, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control", "placeholder": "Введите название рассылки"})
        self.fields["finish_sending"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Укажите дату окончания рассылки"}
        )
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Добавьте комментарий", "style": "height: 100px;"}
        )

        if user is not None:
            self.fields["clients"].queryset = NewsletterRecipient.objects.filter(owner=user)
        else:
            self.fields["clients"].queryset = NewsletterRecipient.objects.none()
        if user is not None:
            self.fields["message"].queryset = Message.objects.filter(owner=user)
        else:
            self.fields["message"].queryset = Message.objects.none()

        self.fields["message"].widget.attrs.update({"class": "form-control"})
        self.fields["clients"].widget.attrs.update({"class": "form-check", "style": "width: 400px;"})

    def clean_finish_sending(self):
        finish_sending = self.cleaned_data.get("finish_sending")
        if finish_sending:
            # Устанавливаем время на полночь
            finish_sending = datetime.combine(finish_sending.date(), time.min)
        return finish_sending
