from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django_recaptcha.fields import ReCaptchaField

from scoutsalesapp.models import Item


class ItemForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Item
        fields = ["seller_email", "seller_name", "title", "description", "price", "donation", "captcha"]
        labels = {
            "seller_email": "Your email address",
            "seller_name": "Your name",
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-lg-2'
        helper.field_class = 'col-lg-10'
        helper.layout = Layout(
            'seller_name',
            'seller_email',
            'title',
            'description',
            PrependedText('price', '£'),
            AppendedText('donation', '%'),
            # FormActions(
            #     Submit('submit', 'Submit', css_class="btn-primary"),
            # )
        )
        return helper
