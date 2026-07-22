import logging
from email.message import EmailMessage
import aiosmtplib
from src.config import settings

logger = logging.getLogger(__name__)

def create_order_email(to_email: str, order_id: int, total_price: float) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = f"Заказ №{order_id} успешно оформлен!"
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email

    text_content = f"Спасибо за ваш заказ №{order_id}! Сумма к оплате: {total_price} руб."
    msg.set_content(text_content)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px; }}
            .card {{ background-color: #ffffff; padding: 24px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .header {{ font-size: 20px; font-weight: bold; color: #111; margin-bottom: 12px; }}
            .text {{ color: #555; line-height: 1.5; font-size: 14px; }}
            .details {{ margin: 20px 0; padding: 15px; background: #fafafa; border-radius: 6px; border-left: 4px solid #111; }}
            .total {{ font-size: 16px; font-weight: bold; color: #000; }}
            .footer {{ margin-top: 20px; font-size: 12px; color: #888; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">Спасибо за заказ!</div>
            <div class="text">
                Ваш заказ <strong>№{order_id}</strong> принят в обработку и скоро будет собран.
            </div>
            <div class="details">
                <div class="text">Итого к оплате:</div>
                <div class="total">{total_price} ₽</div>
            </div>
            <div class="footer">
                Это автоматическое письмо, отвечать на него не нужно.
            </div>
        </div>
    </body>
    </html>
    """

    msg.add_alternative(html_content, subtype="html")
    return msg


async def send_order_email(to_email: str, order_id: int, total_price: float):
    """Вызывается в роутере/фоновой задаче для отправки письма по заказу."""
    message = create_order_email(to_email, order_id, total_price)
    
    use_tls = settings.SMTP_PORT == 465
    start_tls = settings.SMTP_PORT == 587 or settings.SMTP_PORT == 2525

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=start_tls,
            use_tls=use_tls,
        )
        logger.info(f"Письмо для заказа №{order_id} успешно отправлено на {to_email}")
    except Exception as e:
        logger.error(f"Ошибка при отправке письма на {to_email}: {e}")