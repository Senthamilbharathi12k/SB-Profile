# # # from django.shortcuts import render

# # # def home(request):
# # #     # return render(request, 'Portfoliohtmlpages/base.html')
# # #     return render(request, 'Portfoliohtmlpages/index.html')

import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect


logger = logging.getLogger(__name__)


# Base Page
def base(request):
    return render(request, "Portfoliohtmlpages/base.html")


# Home Page
def home(request):
    return render(request, "Portfoliohtmlpages/home.html")


# Contact Page + Email Sending
def contact(request):

    # GET: Open contact page
    if request.method == "GET":
        return render(
            request,
            "portfoliohtmlpages/contact.html"
        )

    # POST: Process submitted form
    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        visitor_email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        # Validate required fields
        if not all([name, visitor_email, subject, message]):
            messages.error(request, "Please fill in all fields.")
            return redirect("/#contact")

        # Validate input lengths
        if (
            len(name) > 100
            or len(visitor_email) > 254
            or len(subject) > 200
            or len(message) > 5000
        ):
            messages.error(
                request,
                "One or more fields are too long."
            )
            return redirect("/#contact")

        # Validate email address
        try:
            validate_email(visitor_email)
        except ValidationError:
            messages.error(
                request,
                "Please enter a valid email address."
            )
            return redirect("/#contact")

        try:
            # 1. Send visitor's message to portfolio owner
            owner_email = EmailMessage(
                subject=f"SB PROFILE Contact: {subject}",
                body=(
                    "New message from your portfolio website.\n\n"
                    f"Name: {name}\n"
                    f"Email: {visitor_email}\n"
                    f"Subject: {subject}\n\n"
                    f"Message:\n{message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECEIVER_EMAIL],
                reply_to=[visitor_email],
            )

            owner_email.send(fail_silently=False)

            # 2. Send confirmation email to visitor
            visitor_confirmation = EmailMessage(
                subject="Thank you for contacting SB PROFILE",
                body=(
                            
                            f"Hi {name},\n\n"
                            
                            "Thank you for taking the time to reach out to me "
                            
                            "through my portfolio. I truly appreciate your "
                            
                            "interest in connecting with me.\n\n"
                            
                            "I've received your message and will take the time "
                            
                            "to review it carefully. I'll get back to you as "
                            
                            "soon as possible.\n\n"
                            
                            "For your reference, here are the details of your inquiry:\n\n"
                            
                            f"Subject: {subject}\n\n"
                            
                            "Thank you once again for your interest and for "
                            
                            "considering me. I look forward to connecting with "
                            
                            "you and exploring how we might work together.\n\n"
                            
                            "Warm regards,\n"
                            
                            "Senthamilbharathi Kasinathan\n"
                            
                            "SB PROFILE\n"
                            
                            "Building ideas into meaningful digital experiences."
                            
                            ),

                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[visitor_email],
            )

            visitor_confirmation.send(fail_silently=False)

            messages.success(
                request,
                "Your message has been sent successfully!"
            )

        except Exception:
            logger.exception("Contact email sending failed")

            messages.error(
                request,
                "Email could not be sent right now. Please try again later."
            )

        return redirect("/#contact")

