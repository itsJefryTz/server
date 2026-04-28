from django.core.mail import send_mail
from django.conf import settings
import threading

def _send_email_logic(to, subject, body):
  try:
    send_mail(
      subject=subject,
      message='',
      from_email=settings.DEFAULT_FROM_EMAIL,
      recipient_list=[to],
      fail_silently=False,
      html_message=body,
    )
  except Exception as e:
    print(f"error: {e}")
  
def send_email_async(*args, **kwargs):
  thread = threading.Thread(target=_send_email_logic, args=args, kwargs=kwargs)
  thread.start()