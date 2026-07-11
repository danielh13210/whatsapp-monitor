import utils
import subprocess

def get_sender_message_pairs(notification):
  messages=[]
  if type(notification['text'])==str: lines=notification['text'].splitlines()
  elif type(notification['text']) in [list,tuple]: lines=notification['text']
  if notification['title']=="String (WhatsApp)": # sender info is not here
    for line in lines:
      message=line.split(':',maxsplit=1)
      message[1]=message[1][1:] # remove the space left behind after the :. we don't use lstrip so that any spaces in the message is preserved
      messages.append(message)
  else:
    sender=utils.extract_value(r'String \((.*)\)',notification['title'])
    for line in lines:
      messages.append([sender,line])
  return messages

def contact_to_jid(contact):
  if not contact.startswith('+'):
    # looks like data1=1234567890@s.whatsapp.net
    raw_response=subprocess.check_output(["adb","shell","content","query","--uri","content://com.android.contacts/data","--projection","data1","--where",f"\"data1 like '%@s.whatsapp.net' and display_name='{contact}'\""],text=True).splitlines()[0]
    # Get only the phone number part
    phone_jid=utils.extract_value(r'data1=(\d+)@s.whatsapp.net',raw_response)
    return phone_jid
  else:
    return "".join([char for char in contact if char.isdigit()])
