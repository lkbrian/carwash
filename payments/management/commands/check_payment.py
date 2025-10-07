from django.core.management.base import BaseCommand
from app import settings
from payments.models import Paywall
import imaplib
import email


class Command(BaseCommand):
    help = "Checks email replies for 'PAID' and updates Paywall status"

    def handle(self, *args, **options):
        IMAP_SERVER = "imap.gmail.com"
        EMAIL = settings.EMAIL_HOST_USER
        PASSWORD = settings.EMAIL_HOST_PASSWORD

        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, '(UNSEEN SUBJECT "Payment Confirmation")')
        if status != "OK":
            self.stdout.write(self.style.ERROR("No messages found"))
            return

        for num in messages[0].split():
            status, data = mail.fetch(num, "(RFC822)")
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body += part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()

            if "paid" in body.lower():
                paywall = Paywall.objects.first()
                if paywall:
                    paywall.status = "paid"
                    paywall.save()
                    self.stdout.write(self.style.SUCCESS("✅ Payment marked as PAID"))
            else:
                self.stdout.write("No payment confirmation found in this email.")

            # mark as seen
            mail.store(num, "+FLAGS", "\\Seen")

        mail.logout()
