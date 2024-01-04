
import PySimpleGUI as sg
import pyotp
import os


# Setup Shoonya Connection Details
# TODO : Get the password and API details from the database and decrypt using salt from db and
#  pepper from windows keyring using Argon2id

def otp_shoonya(user_string='Prakash'):
    user_string = user_string.upper()[0:3]
    # API credentials
    token = os.getenv('SHOONYA_TOTP_TOKEN_' + user_string)
    factor2 = pyotp.TOTP(token).now()
    return factor2


layout = [
    [sg.Text("Rajas - " + str(otp_shoonya("RAJ")), key="-OTP_RAJ-")],
    [sg.Text("Ree - " + str(otp_shoonya("REE")), key="-OTP_REE-")],
    [sg.Text("Prakash - " + str(otp_shoonya("PRA")), key="-OTP_PRA-")],
    [sg.Text("Veena   - " + str(otp_shoonya("VEE")), key="-OTP_VEE-")],
    [sg.Text("Radhika - " + str(otp_shoonya("RAD")), key="-OTP_RAD-")],
    [sg.Text("Anuradha - " + str(otp_shoonya("ANU")), key="-OTP_ANU-")],
    [sg.Button("Refresh")]
]
count = 0
window = sg.Window(title="Shoonya OTP Generator", layout=layout, margins=(100, 50))

while count < 5:
    event, values = window.read()
    # print(event, values)
    if event == "Refresh":
        window["-OTP_RAJ-"].update(value="Rajas - " + str(otp_shoonya("RAJ")))
        window["-OTP_PRA-"].update(value="Prakash - " + str(otp_shoonya("PRA")))
        window["-OTP_VEE-"].update(value="Veena   - " + str(otp_shoonya("VEE")))
        window["-OTP_RAD-"].update(value="Radhika - " + str(otp_shoonya("RAD")))
        window["-OTP_ANU-"].update(value="Anuradha - " + str(otp_shoonya("ANU")))
        window["-OTP_REE-"].update(value="Reema - " + str(otp_shoonya("REE")))
        window.refresh()
        # print("This was triggered.")
    if event == sg.WIN_CLOSED:
        break
window.close()
