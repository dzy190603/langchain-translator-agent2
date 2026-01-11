import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from dotenv import load_dotenv

load_dotenv()

class EmailSenderTool:
    """
    QQ邮箱发送工具封装
    """
    def __init__(self):
        self.sender_email = os.getenv("QQ_EMAIL_USER")
        self.sender_password = os.getenv("QQ_EMAIL_PASSWORD") # 这里应该是QQ邮箱的授权码，而非密码
        self.smtp_server = "smtp.qq.com"
        self.smtp_port = 465

    def send_email(self, subject: str, content: str, to_email: str = None) -> str:
        """
        发送邮件
        :param subject: 邮件主题
        :param content: 邮件正文
        :param to_email: 收件人邮箱，如果不填则使用环境变量中的默认接收方
        :return: 发送结果信息
        """
        if not self.sender_email or not self.sender_password:
            return "Error: QQ Email credentials not configured in .env"

        target_email = to_email or os.getenv("TARGET_EMAIL")
        if not target_email:
            return "Error: Target email not specified"

        try:
            msg = MIMEMultipart()
            msg['From'] = formataddr(["Policy Agent", self.sender_email])
            msg['To'] = formataddr(["User", target_email])
            msg['Subject'] = subject

            msg.attach(MIMEText(content, 'html', 'utf-8'))

            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, [target_email], msg.as_string())
            server.quit()
            
            return f"Email sent successfully to {target_email}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"

# 简单的测试代码
if __name__ == "__main__":
    tool = EmailSenderTool()
    print(tool.send_email("Test Subject", "<h1>This is a test email</h1>"))