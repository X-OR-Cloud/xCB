"""
src/integrations/email_service.py — Service gửi email tự động của xHR
Sử dụng aiosmtplib để gửi async.
"""
import ssl
from email.message import EmailMessage

import aiosmtplib
import structlog

from src.config import settings

log = structlog.get_logger(__name__)

async def send_email(to_email: str, subject: str, content: str) -> bool:
    """Gửi email HTML/Text đến địa chỉ nhận."""
    if not settings.smtp_username or not settings.smtp_password:
        log.warning("email_skip_no_config", to=to_email, reason="SMTP credentials not set")
        return False

    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(content)
    
    # Ở phiên bản xHR, chúng tôi khuyên dùng HTML để email chuyên nghiệp hơn
    message.add_alternative(f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">Thinh Long Group</h2>
                <div style="padding: 10px 0;">
                    {content.replace('\n', '<br>')}
                </div>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 12px; color: #888;">
                    Đây là email tự động từ hệ thống xHR. Vui lòng không phản hồi email này.<br>
                    Website: <a href="https://thinhlonggroup.com">thinhlonggroup.com</a>
                </p>
            </div>
        </body>
    </html>
    """, subtype="html")

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=settings.smtp_port == 465,
            start_tls=settings.smtp_port == 587,
        )
        log.info("email_sent_success", to=to_email, subject=subject)
        return True
    except Exception as exc:
        log.error("email_sent_failed", to=to_email, error=str(exc))
        return False
