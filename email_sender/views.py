import smtplib
import ssl
from email.message import EmailMessage
from django.shortcuts import render, redirect
from .forms import EmailForm


def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the email data to the database
            email = form.save()

            # Prepare the email message using EmailMessage class
            email_msg = EmailMessage()
            email_msg['From'] = 'mingloktesting@gmail.com'
            email_msg['To'] = email.to_email
            if email.cc_email:
                email_msg['Cc'] = email.cc_email
            email_msg['Subject'] = email.subject
            email_msg.set_content(email.body)

            # Attach the file to the email
            if email.attachment:
                email_msg.add_attachment(email.attachment.read(), maintype='application', subtype='pdf', filename=email.attachment.name)

            # Create a secure SSL context
            context = ssl.create_default_context()

            # Send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login('mingloktesting@gmail.com', 'rvoopwztdpbktfzy')
                try:
                    smtp.send_message(email_msg)
                    smtp.quit()
                    return redirect('success')
                except Exception as e:
                    # Handle any errors that might occur during sending
                    # For simplicity, we'll just print the error message here
                    print(f"Failed to send email: {e}")
    else:
        form = EmailForm()
    return render(request, 'index.html', {'form': form})


def email_success(request):
    return render(request, 'success.html')