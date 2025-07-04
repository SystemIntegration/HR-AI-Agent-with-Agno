import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

if not os.path.exists("./logs"):
    os.mkdir("./logs")

file_handler = RotatingFileHandler(
    "./logs/agno_agents.log",
    maxBytes=500000,
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
logger.addHandler(file_handler)

try:
    mail_handler = SMTPHandler(
        mailhost=(os.getenv("MAIL_SERVER"),587),
        fromaddr=os.getenv("FROM_ADDRESS"),
        toaddrs=[addr.strip() for addr in os.getenv("TO_ADDRESS", "").split(",")],
        subject='[ERROR] CortexHR Application Exception',
        credentials=(
            os.getenv("FROM_ADDRESS"),
            os.getenv("EMAIL_PASS")
        ),
        secure=()
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '''Timestamp: %(asctime)s
        Level: %(levelname)s
        Message: %(message)s
        Location: %(pathname)s:%(lineno)d
        '''
    ))
    logger.addHandler(mail_handler)
except Exception as e:
    logger.error("Failed to set up SMTPHandler", exc_info=True)

logger.info("Virtual HR logger initialized")
