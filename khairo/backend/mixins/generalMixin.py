from fastapi.responses import JSONResponse
import smtplib
from khairo.settings import EMAIL,PASSWORD

class KhairoFullMixin:
    @staticmethod
    def  Response(userMessage: object, success: object, status_code: object)-> object:
        if success:
            return JSONResponse(content={"status":"success", "message":userMessage}, status_code=status_code)
        return JSONResponse(content={"status": "error", "message": userMessage}, status_code=status_code)


    @staticmethod
    def mailUser(userEmail:str, emailMessage:str, emailTitle):
        ######################### setting mail server #######################
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as access360Mail:
            try:
                ######################### Authenticate account #######################
                access360Mail.login(EMAIL, PASSWORD)
                ######################### setting up mail body #######################
                # message["subject"] = emailTitle
                # message['from'] = EMAIL
                # message['to'] = userEmail
                # message.set_content(emailMessage)
                # access360Mail.send_message(message)
                message = f"subject:{emailTitle}\n\n body:{emailMessage}"
                access360Mail.sendmail(EMAIL, userEmail, message)
                ######################### return success message #######################
                print("message sent successfully")
                return "message sent successfully"
                
            except Exception:
                ######################### return error if mail failed to send #######################
                print("message sent successfully")
                return "Error sending message"
            





