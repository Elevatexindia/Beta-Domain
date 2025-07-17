from django.contrib import auth
import os
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import ContactForm, NewsletterSubscriptionForm, PhoneCallForm
from .models import NewsletterSubscription, PhoneCall, CustomerStats
from datetime import datetime
from django.contrib import messages
from dotenv import load_dotenv
import threading

load_dotenv()

def send_email_async(subject, text_content, html_content, from_email, recipient_list):
    def _send():
        try:
            msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            import traceback
            print("EMAIL SEND ERROR:", e)
            traceback.print_exc()
    threading.Thread(target=_send).start()

def home(request):
    if request.method == 'POST':
        newsletter_form = NewsletterSubscriptionForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            if NewsletterSubscription.objects.filter(email=email).exists():
                messages.warning(request, 'You are already subscribed to our newsletter.')
                return redirect('/home/#newsletter')
            else:
                # Create a new NewsletterSubscription object
                NewsletterSubscription.objects.create(email=email)

                # Send email to user confirming subscription
                user_subject = 'Subscription Confirmation'
                user_context = {
                    'email': email,
                    'message': 'Thank you for subscribing to our newsletter!',
                    'company_name': 'ElevateBharat',  # Replace with your company name
                    'tagline': 'Elevate your business and rise to new heights with ElavateBharat',
                    'year': datetime.now().year,
                }

                user_html_content = render_to_string('mail_templates/newsletter_customer.html', user_context)
                user_text_content = strip_tags(user_html_content)

                send_email_async(user_subject, user_text_content, user_html_content, settings.EMAIL_HOST_USER, [email])

                messages.success(request, 'You have successfully subscribed to our newsletter!')
                return redirect('/home/#newsletter')
        else:
            messages.error(request, 'Failed to subscribe. Please check your email and try again.')
            return redirect('/home/#newsletter')
    else:
        newsletter_form = NewsletterSubscriptionForm()

    return render(request, 'index.html', {'newsletter_form': newsletter_form})

def services(request):
    return render(request,'services.html')
def about(request):
    if request.method == 'POST':
        call_form = PhoneCallForm(request.POST)
        if call_form.is_valid():
            phone = call_form.cleaned_data['phone']
            if PhoneCall.objects.filter(phone=phone).exists():
                messages.warning(request, 'Your call is already scheduled.')
            else:
                PhoneCall.objects.create(phone=phone)
                messages.success(request, 'Your call is successfully scheduled!')
            return redirect('/about/#schedule_call')  # Correct redirect here
        else:
            messages.error(request, 'Failed to schedule. Please check your phone number and try again.')
    else:
        call_form = PhoneCallForm()
    
    customer_stats = CustomerStats.objects.first()
    if not customer_stats:
        customer_stats = {
            'happy_clients': 0,
            'projects_completed': 0,
            'full_time_specialists': 0,
            'awards_won': 0
        }
    return render(request, 'about.html', {'phonecallform': call_form,'customer_stats': customer_stats})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            company = form.cleaned_data.get('company', '')

            # Save form data
            form.save()

            # Prepare data for owner email
            owner_subject = 'New Contact Form Submission'
            owner_context = {
                'name': name,
                'company': form.cleaned_data['company'],
                'email': email,
                'phone_number': phone_number,
                'message': message,
                'website_development': form.cleaned_data.get('website_development', False),
                'app_development': form.cleaned_data.get('app_development', False),
                'marketing': form.cleaned_data.get('marketing', False),
                'other': form.cleaned_data.get('other', False),
                'other_description': form.cleaned_data.get('other_description', ''),
                'company_name': 'ElevateBharat',
                'tagline': 'Elevate your business and rise to new heights with ElavateBharat',
                'year': datetime.now().year,
            }

            owner_html_content = render_to_string('mail_templates/contact_owner.html', owner_context)
            owner_text_content = strip_tags(owner_html_content)
            MAILSEND_HOSTS = os.environ.get("MAILSEND_HOSTS").split(" ")
            send_email_async(owner_subject, owner_text_content, owner_html_content, settings.EMAIL_HOST_USER, MAILSEND_HOSTS)

            # Prepare data for user email
            user_subject = 'Thank You for Contacting Us'
            user_context = {
                'name': name,
                'company': form.cleaned_data['company'],
                'email': email,
                'phone_number': phone_number,
                'message': message,
                'website_development': form.cleaned_data.get('website_development', False),
                'app_development': form.cleaned_data.get('app_development', False),
                'marketing': form.cleaned_data.get('marketing', False),
                'other': form.cleaned_data.get('other', False),
                'other_description': form.cleaned_data.get('other_description', ''),
                'company_name': 'ElevateBharat',
                'tagline': 'Elevate your business and rise to new heights with ElavateBharat',
                'year': datetime.now().year,
            }
            user_html_content = render_to_string('mail_templates/contact_customer.html', user_context)
            user_text_content = strip_tags(user_html_content)
            send_email_async(user_subject, user_text_content, user_html_content, settings.EMAIL_HOST_USER, [email])

            return redirect('/success/')
        else:
            # Redirect to a "form invalid" page if the form is not valid
            return redirect('/form-invalid/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def welcome(request):
    return render(request,'welcome.html')
def signin(request):
    return render(request,'signin.html')
def signup(request):
    return render(request,'signup.html')
def recovery(request):
    return render(request,'recovery.html')
def maintenance(request):
    return render(request,'maintenance.html')
def redirect_to_lakhiram(request):
    return redirect('http://lakhiramdairyfarm.in/')
def comingsoon(request):
    return render(request,'coming.html')
def error_404(request, exception):
    return render(request, '404.html', status=404)
def Page404(request, exception):
    return render(request, '404.html', status=404)
def success(request):
    return render(request, 'success.html')
def denied(request):
    return render(request, 'denied.html')
def tracking(request):
    return render(request,'000357.html')

