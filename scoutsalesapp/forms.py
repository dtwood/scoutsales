import crispy_forms.layout
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.urls import reverse
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha import widgets

from scoutsalesapp.models import Item


class ItemForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=widgets.ReCaptchaV3)

    class Meta:
        model = Item
        fields = ["seller_email", "seller_name", "title", "description", "price", "donation", "captcha"]
        labels = {
            "seller_email": "Your email address",
            "seller_name": "Your name",
            "title": "Item name",
            "description": "Item description",
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-lg-2'
        helper.field_class = 'col-lg-10'
        helper.form_action = reverse('items-create')
        helper.form_method = 'POST'
        helper.layout = Layout(
            'seller_name',
            'seller_email',
            'title',
            'description',
            PrependedText('price', '£'),
            AppendedText('donation', '%'),
            crispy_forms.layout.Div('captcha'),
            FormActions(
                Submit('btnSubmit', 'Submit', css_class="btn-primary"),
            )
        )
        return helper
