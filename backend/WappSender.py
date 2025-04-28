import pandas as pd
import re
import pywhatkit
import pyautogui
import time
# WappSender Class
class WappSender:
    def __init__(self, organization_name, meeting_date, meeting_time, location):
        self.organization_name = organization_name
        self.meeting_date = meeting_date
        self.meeting_time = meeting_time
        self.location = location

    @staticmethod
    def format_contact(contact):
        """
        Formats a contact number to the +880XXXXXXXXXX format.
        """
        contact = re.sub(r'\D', '', contact)
        if contact.startswith('880') and len(contact) == 13:
            return f"+{contact}"
        elif contact.startswith('1') and len(contact) == 10:
            return f"+880{contact}"
        elif contact.startswith('0') and len(contact) == 11:
            return f"+880{contact[1:]}"
        elif len(contact) == 10:
            return f"+880{contact}"
        else:
            return None

    @staticmethod
    def close_whatsapp_window():
        """
        Closes the currently opened WhatsApp window.
        """
        time.sleep(5)  # Adjust the sleep time as necessary
        pyautogui.hotkey('Ctrl', 'w')
        time.sleep(4) 
        pyautogui.hotkey('enter')

    def send_whatsapp_message(self, phone_number, name):
        """
        Sends a WhatsApp message using pywhatkit.
        """
        message = f"""
        Hi {name}, This is from {self.organization_name}. 
            
        You have been selected for the post you applied for. We look forward to meeting with you at our office. The details are given below: 
            
        Date: {self.meeting_date},
        Time: {self.meeting_time},
        Location: {self.location}.
        
        Please let us know if you have any questions or concerns."""
        try:
            pywhatkit.sendwhatmsg_instantly(phone_number, message)
            self.close_whatsapp_window()
            return "Sent"
        except Exception as e:
            return f"Error sending message to {name} ({phone_number}): {e}"

