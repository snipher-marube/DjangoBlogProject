from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
import threading
from django.contrib.auth.models import User

from .models import Newsletter, NewsletterText


class EmailThread(threading.Thread):

    def __init__(self, subject, message, from_email, to_email, fail_silently, html_message):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.to_email = to_email
        self.fail_silently = fail_silently
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.message, self.from_email, self.to_email, self.fail_silently, self.html_message)

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Newsletter.objects.filter(email=email).exists():
            messages.error(request, 'You are already subscribed to our newsletter')
            # check if the email is verified
            if Newsletter.objects.filter(email=email, verified=True).exists():
                messages.error(request, 'Your email is already verified')
                return redirect('blog:home')
            else:
                messages.error(request, 'Your email is not verified')
                return redirect('blog:home')

            return redirect('blog:home')
        else:
            Newsletter.objects.create(email=email)
            messages.success(request, 'You have successfully subscribed to our newsletter')

            # send email to user
            subject = '[Joined our Newsletter Subscriber]'
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email for instance in Newsletter.objects.all()]
            with open(settings.BASE_DIR / 'templates/newsletter/welcome_email.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject,
                body=signup_message,
                from_email=from_email,
                to=to_email
            )
            html_template = get_template("newsletter/welcome_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()

            # Send email to admin
            # get admin email
            admin_email = User.objects.get(is_superuser=True).email
            send_mail(
                'New newsletter subscriber',
                'A new user has subscribed to your newsletter',
                from_email,
                [admin_email, 'sniphermarube@gmail.com'],
                fail_silently=False,
            )

            thread = EmailThread(subject, message, from_email, to_email, False, html_template)
            thread.start()

            return redirect('blog:home')

def newsletter_unsubscribe(request):
    # get email from url
    email = request.GET.get('email')
    if Newsletter.objects.filter(email=email).exists():
        Newsletter.objects.filter(email=email).delete()
        messages.success(request, 'You have successfully unsubscribed from our newsletter')
        return redirect('blog:home')
    else:
        messages.error(request, 'You are not subscribed to our newsletter')
        return redirect('blog:home')

# send newsletter to all subscribers

def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.email for instance in Newsletter.objects.all()]
        html_message = get_template("newsletter/newsletter.html").render({'message': body})
        send_mail(
            subject,
            body,
            from_email,
            to_email,
            fail_silently=False,
            html_message=html_message,
        )

        # save newsletter to database
        newsletter = NewsletterText.objects.create(subject=subject, body=body, status='Published')
        newsletter.save()

        messages.success(request, 'Newsletter sent successfully')
        return redirect('blog:home')
    return render(request, 'newsletter/send_newsletter.html')










