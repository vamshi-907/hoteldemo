from django import forms
from .models import HotelPayment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit

class HotelPaymentForm(forms.ModelForm):
    class Meta:
        model = HotelPayment
        fields = "__all__"

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'name',
            'amount',
            Submit('submit','Book Hotel',css_class="button white btn-block btn-primary")
        )
