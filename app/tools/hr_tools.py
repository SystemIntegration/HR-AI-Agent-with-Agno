# app/tools/hr_tools.py
from app.app_generalize_settings import NOTIFIER_EMAIL,NOTIFIER_EMAIL_PASSWORD,HR_EMAILS,CC_EMAILS,FOLDER_NAME
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from app.configurations.agents_memory_storage import memory
from agno.memory.v2.schema import UserMemory

def send_policy_request_to_hr(user_query: str, suggested_policy_content: str, category: str, mode: str = "create") -> str:
    """
    Sends a request email to HR recommending creation of a new policy document.

    Args:
        user_query: A actual query of user.
        suggested_policy_content: AI-generated outline or content for the new policy.
        category: The category name for naming and folder organization.
        mode: `update` if the category is from the existing index, `create` otherwise.

    Returns:
        Confirmation string.
    """
    # Compose file name and email metadata
    action_text = "create a new policy document" if mode == "create" else "update the existing policy document"
    file_name = f"{category.replace(' ', '_').upper()}.pdf" if category else "GENERAL_HR_POLICY.pdf"
    subject = f"📄 Policy Request - {category or 'Uncategorized'}"

    

    email_body_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 15px;">
        <p>Hi HR Team,</p>

        <p>A recent employee query <strong>could not be answered</strong> based on current policy documents.</p>

        <hr>
        <p><strong>📌 Policy Request:</strong></p>
        <pre style="background-color: #f4f4f4; padding: 10px; border-left: 3px solid #ccc;">{user_query}</pre>

        <p><strong>📝 Suggested Policy Content:</strong></p>
        <pre style="background-color: #f4f4f4; padding: 10px; border-left: 3px solid #ccc;">{suggested_policy_content}</pre>

        <hr>
        <p>Please <strong>{action_text}</strong> in the Google Drive folder: <strong>"{FOLDER_NAME}"</strong></p>

        <p>📄 Recommended File Name: <strong>{file_name}</strong></p>

        <p>Thank you!</p>
    </body>
    </html>
    """

    # Email setup
    sender_email = NOTIFIER_EMAIL
    password = NOTIFIER_EMAIL_PASSWORD
    to_emails = HR_EMAILS
    cc_emails = CC_EMAILS
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_emails
    message["Cc"] = cc_emails

    # Attach both plain text and HTML versions
    # message.attach(MIMEText(email_body_plain, "plain"))
    message.attach(MIMEText(email_body_html, "html"))

    # Combine all recipients (To + Cc) for sending
    recipients = [to_addr.strip() for to_addr in to_emails.split(",")] + [cc_addr.strip() for cc_addr in cc_emails.split(",")]

    # Send email via secure SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            from_addr=sender_email,
            to_addrs=recipients,
            msg=message.as_string()
        )

    # print("Email sent to HR:\n", email_body_html)



    # Log memory after successful send
    memory_note = (
        f"An email was sent to HR to {action_text} for category '{category or 'Uncategorized'}'.\n"
        f"Query: {user_query}\n"
        f"Suggested Content: {suggested_policy_content[:100]}..."
    )

    memory_id = memory.add_user_memory(
    memory=UserMemory(
        memory=memory_note,
        input=user_query,
        topics=["policy_request", category.lower() if category else "uncategorized"]
    ),
    user_id="default"
)


    return f"✅ Policy request email sent to HR for category: {category or 'Uncategorized'}."
