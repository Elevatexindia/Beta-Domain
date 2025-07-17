from django.db import models
from django.contrib.auth.models import User

class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    website_development = models.BooleanField(default=False)
    app_development = models.BooleanField(default=False)
    marketing = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Contact Form Entry'
        verbose_name_plural = 'Contact Form Entries'
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscription'

class PhoneCall(models.Model):
    phone = models.CharField(max_length=15, verbose_name='Phone Number')
    scheduled_at = models.DateTimeField(auto_now_add=True, verbose_name='Scheduled At')
    def __str__(self):
        return self.phone
    class Meta:
        verbose_name = 'Scheduled call'
        verbose_name_plural = 'Scheduled call'

class CustomerStats(models.Model):
    happy_clients = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    full_time_specialists = models.PositiveIntegerField(default=0)
    awards_won = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Customer Stats (ID: {self.id})"

# User Profile model for uploading profile images
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True, verbose_name='Portfolio Link')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'