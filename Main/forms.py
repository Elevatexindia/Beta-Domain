from django import forms
from .models import ContactForm, PhoneCall, CustomerStats  # Adjust based on your model name and location

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactForm  # Replace with your actual model name
        fields = ['name', 'company', 'email', 'phone_number', 'message', 'website_development', 'app_development', 'marketing', 'other', 'other_description']
        
class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)


class PhoneCallForm(forms.ModelForm):
    class Meta:
        model = PhoneCall
        fields = ['phone']

class CustomerStatsForm(forms.ModelForm):
    class Meta:
        model = CustomerStats
        fields = '__all__'

