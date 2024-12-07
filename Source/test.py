# from imap_tools import MailBox, AND

# # Get date, subject and body len of all emails from INBOX folder
# with MailBox('imap.gmail.com').login('shubhammurtadak6@gmail.com',"wpon kzsw cqcy lmdf") as mailbox:
#     for msg in mailbox.fetch():
#         print(msg.date, msg.subject, len(msg.text or msg.html))



import time
from imap_tools import MailBox, A
from datetime import datetime, timedelta

# Define the time window (1 minute ago), ensure it's naive (no timezone info)
time_threshold = datetime.now() - timedelta(minutes=1)
time_threshold = time_threshold.replace(tzinfo=None)  # Make it naive

with MailBox('imap.gmail.com').login('shubhammurtadak6@gmail.com',"wpon kzsw cqcy lmdf") as mailbox:

    for msg in mailbox.fetch(A(seen=False),mark_seen=True):  # Only unread messages
        # Compare message date with time threshold
        print(f"New email from {msg.from_} with subject: {msg.subject} at {msg.date}")
           
    else:
        print('No updates in the last 60 seconds.')
