import pytest
from unittest.mock import patch, Mock
from src.services.NotificationService import NotificationService

import pytest
from unittest.mock import patch, Mock
from src.services.NotificationService import NotificationService


@patch("src.services.NotificationService.smtplib.SMTP")
@patch("src.services.NotificationService.os.getenv")
def test_send_email_success(mock_getenv, mock_smtp):
    """
    Scenario: Successfully send an email
      Given valid email configuration and recipient information
      When the send_email function is called
      Then an email should be sent without errors
    """
    mock_getenv.side_effect = lambda key: {
        "SMTP_SERVER": "smtp.example.com",
        "SMTP_PORT": "587",
        "EMAIL_USER": "user@example.com",
        "EMAIL_PASSWORD": "password123"
    }.get(key)

    mock_smtp_instance = Mock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

    notification_service = NotificationService()

    to_email = "recipient@example.com"
    subject = "Test Subject"
    message = "This is a test email."

    notification_service.send_email(to_email, subject, message)

    mock_getenv.assert_any_call("SMTP_SERVER")
    mock_getenv.assert_any_call("SMTP_PORT")
    mock_getenv.assert_any_call("EMAIL_USER")
    mock_getenv.assert_any_call("EMAIL_PASSWORD")

    mock_smtp.assert_called_with("smtp.example.com", 587)
    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_with("user@example.com", "password123")
    mock_smtp_instance.sendmail.assert_called_once()


@patch("src.services.NotificationService.smtplib.SMTP")
@patch("src.services.NotificationService.os.getenv")
def test_send_email_failure_due_to_missing_env_vars(mock_getenv, mock_smtp):
    """
    Scenario: Failure to send an email due to missing environment variables
      Given that the environment variables for email configuration are missing
      When the send_email function is called
      Then the function should not attempt to send the email
      And should raise a ValueError
    """
    mock_getenv.return_value = None

    notification_service = NotificationService()

    to_email = "recipient@example.com"
    subject = "Test Subject"
    message = "This is a test email."

    with pytest.raises(ValueError, match="Missing email configuration environment variables"):
        notification_service.send_email(to_email, subject, message)

    mock_smtp.assert_not_called()
