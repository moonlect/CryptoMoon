"""Email notification service."""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings


class EmailService:
    """Service for sending email notifications."""

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
    ) -> bool:
        """Send email via SMTP."""
        if not all([settings.smtp_host, settings.smtp_user, settings.smtp_password]):
            print("SMTP not configured, skipping email send")
            return False

        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = settings.smtp_from_email
            message["To"] = to_email

            # Add text and HTML parts
            if text_body:
                text_part = MIMEText(text_body, "plain")
                message.attach(text_part)

            html_part = MIMEText(html_body, "html")
            message.attach(html_part)

            # Send email
            await aiosmtplib.send(
                message,
                hostname=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_user,
                password=settings.smtp_password,
                use_tls=settings.smtp_port == 587,
            )

            return True

        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")
            return False

    def generate_signal_email_html(
        self,
        signal_type: str,
        coin_name: str,
        signal_data: dict,
    ) -> tuple[str, str, str]:
        """Generate HTML email template for signal notification.
        
        Returns:
            tuple: (subject, html_body, text_body)
        """
        signal_type_names = {
            "mexc_spot_futures": "MEXC Spot & Futures",
            "funding_rate": "Funding Rate Spread",
            "mexc_dex": "MEXC & DEX Price Spread",
        }

        signal_name = signal_type_names.get(signal_type, signal_type)
        subject = f"New {signal_name} Signal: {coin_name}"

        # Build HTML content
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; }}
                .signal-info {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                .button {{ display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 New Signal Alert</h1>
                </div>
                <div class="content">
                    <h2>{coin_name} - {signal_name}</h2>
                    <div class="signal-info">
        """

        # Add signal-specific information
        if signal_type == "mexc_spot_futures":
            spread = signal_data.get("spread")
            position = signal_data.get("position", "N/A")
            spot_price = signal_data.get("mexc_spot_price")
            futures_price = signal_data.get("mexc_futures_price")

            html += f"""
                        <p><strong>Position:</strong> {position}</p>
                        <p><strong>Spread:</strong> {spread}%</p>
                        <p><strong>Spot Price:</strong> ${spot_price}</p>
                        <p><strong>Futures Price:</strong> ${futures_price}</p>
            """

        elif signal_type == "funding_rate":
            profit = signal_data.get("hourly_profit")
            html += f"""
                        <p><strong>Hourly Profit:</strong> {profit}%</p>
            """

        elif signal_type == "mexc_dex":
            spread = signal_data.get("spread_percent")
            mexc_price = signal_data.get("mexc_price")
            dex_price = signal_data.get("dex_price")
            html += f"""
                        <p><strong>Spread:</strong> {spread}%</p>
                        <p><strong>MEXC Price:</strong> ${mexc_price}</p>
                        <p><strong>DEX Price:</strong> ${dex_price}</p>
            """

        html += """
                    </div>
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="https://cryptotracker.com/signals" class="button">View Signal</a>
                    </p>
                </div>
                <div class="footer">
                    <p>This is an automated notification from CryptoTracker</p>
                    <p>You can manage your notification preferences in your profile settings.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Plain text version
        text = f"""
New Signal Alert: {coin_name} - {signal_name}

Signal Details:
"""

        if signal_type == "mexc_spot_futures":
            text += f"Position: {position}\nSpread: {spread}%\n"
        elif signal_type == "funding_rate":
            text += f"Hourly Profit: {profit}%\n"
        elif signal_type == "mexc_dex":
            text += f"Spread: {spread}%\n"

        text += "\nView signal at: https://cryptotracker.com/signals"

        return subject, html, text


# Global email service instance
email_service = EmailService()

