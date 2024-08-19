import os
import time

from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.BooksModel import BooksModel
from models.UsersModel import UsersModel

load_dotenv()


class NotificationService:
    def __init__(self):
        self.user_model = UsersModel()
        self.book_model = BooksModel()

    def get_user_email(self, user_id):
        try:
            user = self.user_model.get_user_by_id(user_id)
            if not user:
                raise ValueError(f"User {user_id} not found")
            return user["email"]
        except ValueError as e:
            print(f"Error getting user email for user {user_id}: {e}")
            return None
        except Exception as e:
            print(f"Internal error: {e}")
            return None

    def get_book_title(self, book_id):
        try:
            book = self.book_model.get_book_by_id(book_id)
            if not book:
                raise ValueError(f"Book {book_id} not found")
            return book["title"]
        except ValueError as e:
            print(f"Error getting book title for book {book_id}: {e}")
            return None
        except Exception as e:
            print(f"Internal error: {e}")
            return None

    def send_due_soon_email(self, user_id, book_id, due_date):
        try:
            user_email = self.get_user_email(user_id)
            if not user_email:
                raise ValueError(f"User {user_id} not found")
            book_title = self.get_book_title(book_id)
            if not book_title:
                raise ValueError(f"Book {book_id} not found")

            subject = "Reminder: Book Due Soon"
            message = f"Dear user, the book '{book_title}' is due on {due_date}. Please return it on time."

            self.send_email(user_email, subject, message)
        except ValueError as e:
            print(f"ValueError sending due soon email to user {user_id} for book {book_id}: {e}")
            return None
        except Exception as e:
            print(f"Error sending due soon email to user {user_id} for book {book_id}: {e}")
            return None

    def send_due_today_email(self, user_id, book_id, due_date):
        try:
            user_email = self.get_user_email(user_id)
            if not user_email:
                raise ValueError(f"User {user_id} not found")
            book_title = self.get_book_title(book_id)
            if not book_title:
                raise ValueError(f"Book {book_id} not found")

            subject = "Reminder: Book Due Today"
            message = f"Dear user, the book '{book_title}' is due today ({due_date}). Please return it today."

            self.send_email(user_email, subject, message)
        except ValueError as e:
            print(f"ValueError sending due today email to user {user_id} for book {book_id}: {e}")
        except Exception as e:
            print(f"Error sending due today email to user {user_id} for book {book_id}: {e}")

    def send_overdue_email(self, user_id, book_id):
        try:
            user_email = self.get_user_email(user_id)
            if not user_email:
                raise ValueError(f"User {user_id} not found")
            book_title = self.get_book_title(book_id)
            if not book_title:
                raise ValueError(f"Book {book_id} not found")

            subject = "Overdue Notice: Book Not Returned"
            message = (f"Dear user, the book '{book_title}' was due but has not been returned. Please return it as "
                       f"soon as possible.")

            self.send_email(user_email, subject, message)
        except ValueError as e:
            print(f"ValueError sending overdue email to user {user_id} for book {book_id}: {e}")
        except Exception as e:
            print(f"Error sending overdue email to user {user_id} for book {book_id}: {e}")

    @staticmethod
    def send_email(to_email, subject, message):
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        from_email = os.getenv("EMAIL_USER")
        from_password = os.getenv("EMAIL_PASSWORD")

        if not all([smtp_server, smtp_port, from_email, from_password]):
            raise ValueError("Missing email configuration environment variables")

        try:
            email_message = MIMEMultipart()
            email_message['From'] = from_email
            email_message['To'] = to_email
            email_message['Subject'] = subject
            email_message.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
                server.ehlo()
                server.starttls()
                server.login(from_email, from_password)
                server.sendmail(from_email, to_email, email_message.as_string())

            print(f"Email sent to {to_email}: {subject}")
        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")
