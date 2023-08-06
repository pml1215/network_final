from django.core.mail import EmailMessage
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import EmailForm


def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the form data
            email_data = form.cleaned_data

            # Convert the comma-separated string into a list of emails, and remove any whitespace
            to_email_list = [email.strip() for email in email_data['to_email'].split(',')]
            # Validate the email addresses
            for email in to_email_list:
                try:
                    EmailValidator()(email)
                except ValidationError:
                    return render(request, 'index.html', {'form': form, 'error_to': 'Invalid email address'})

            # Convert the comma-separated string into a list of cc emails, and remove any whitespace
            if email_data['cc_email']:
                cc_email_list = [email.strip() for email in email_data['cc_email'].split(',')]
                # Validate the email addresses
                for email in cc_email_list:
                    try:
                        EmailValidator()(email)
                    except ValidationError as e:
                        return render(request, 'index.html', {'form': form, 'error_cc': 'Invalid email address'})
            else:
                cc_email_list = ''

            # Prepare the email message using EmailMessage class
            email_msg = EmailMessage(email_data['subject'],
                                     email_data['body'],
                                     'mingloktesting@gmail.com',
                                     to_email_list,
                                     cc=cc_email_list)

            # Attach the file to the email
            if email_data['attachment']:
                email_msg.attach(email_data['attachment'].name, email_data['attachment'].read())

            # Send the email
            try:
                email_msg.send()
                # Save the email data to the database
                save_email = form.save(commit=False)
                save_email.to_email = to_email_list
                save_email.cc_email = cc_email_list
                save_email.save()
                return redirect('success')
            # Handle any errors that might occur during sending
            # For simplicity, we'll just print the error message here
            except Exception as e:
                print(f"Failed to send email: {e}")
    else:
        return render(request, 'index.html')


def email_success(request):
    return render(request, 'success.html')
