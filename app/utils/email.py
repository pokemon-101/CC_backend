import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from app.core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
    
    async def send_email(self, to_emails: List[str], subject: str, body: str, html_body: str = None):
        """Send email to recipients"""
        if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
            print("Email configuration not complete, skipping email send")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = ', '.join(to_emails)
            
            # Add text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    async def send_welcome_email(self, user_email: str, username: str):
        """Send welcome email to new user"""
        subject = "Welcome to ChordCircle! 🎵"
        body = f"""
Hi {username},

Welcome to ChordCircle! We're excited to have you join our music community.

With ChordCircle, you can:
- Connect your Spotify and Apple Music accounts
- Sync playlists across platforms
- Discover new music with friends
- Share your favorite tracks

Get started by connecting your music accounts in your profile.

Happy listening!
The ChordCircle Team
        """
        
        html_body = f"""
<html>
<body>
    <h2>Welcome to ChordCircle! 🎵</h2>
    <p>Hi {username},</p>
    
    <p>Welcome to ChordCircle! We're excited to have you join our music community.</p>
    
    <p>With ChordCircle, you can:</p>
    <ul>
        <li>Connect your Spotify and Apple Music accounts</li>
        <li>Sync playlists across platforms</li>
        <li>Discover new music with friends</li>
        <li>Share your favorite tracks</li>
    </ul>
    
    <p>Get started by connecting your music accounts in your profile.</p>
    
    <p>Happy listening!<br>
    The ChordCircle Team</p>
</body>
</html>
        """
        
        return await self.send_email([user_email], subject, body, html_body)
    
    async def send_friend_request_email(self, user_email: str, requester_name: str):
        """Send friend request notification email"""
        subject = f"{requester_name} wants to be your friend on ChordCircle"
        body = f"""
Hi there,

{requester_name} has sent you a friend request on ChordCircle!

Log in to your account to accept or decline the request.

Best regards,
The ChordCircle Team
        """
        
        return await self.send_email([user_email], subject, body)

email_service = EmailService()