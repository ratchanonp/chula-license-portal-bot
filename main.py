import requests
import datetime
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()


class ProgramLicenseID(Enum):
    """ Enum of the program license ID"""
    AdobeCreativeCloud = 5
    Zoom = 2


class ChulaLicenseBorrow():
    def __init__(self, username: str, password: str, azure_user_id: str):
        """Borrow the license from the license portal

        Args:
            username (str): CUNET username
            password (str): CUNET password
            azure_user_id (str): Azure User ID (GUID)
        """
        self.username = username
        self.password = password
        self.azure_user_id = azure_user_id
        self.login_url = "https://licenseportal.it.chula.ac.th/"
        self.borrow_url = "https://licenseportal.it.chula.ac.th/Home/Borrow"
        self.cookie = None

    def login(self):
        """ Login to the license portal and get the cookie for later use

        Raises:
            Exception: Login failed
        """

        payload = {
            'UserName': self.username,
            'Password': self.password
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.request(
            "POST", self.login_url, headers=headers, data=self.payload_encoder(payload), allow_redirects=False)

        if response.status_code != 302:
            raise Exception("Login failed")

        print("Login success")

        self.cookie = response.headers['Set-Cookie']

    def borrow(self,
               borrowDate: datetime.datetime,
               expiryDate: datetime.datetime,
               programLicenseID: ProgramLicenseID
               ):
        """Borrow the license from the license portal

        Args:
            borrowDate (datetime.datetime): start date of the license
            expiryDate (datetime.datetime): end date of the license
            programLicenseID (ProgramLicenseID): Enum of the program license ID

        Raises:
            Exception: Borrow failed
        """

        payload = {
            'AzureUserId': self.azure_user_id,
            'UserPrincipalName': self.username,
            'BorrowStatus': 'Borrowing',
            'ProgramLicenseID': programLicenseID.value,
            'BorrowDateStr': borrowDate.strftime("%d/%m/%Y"),
            'ExpiryDateStr': expiryDate.strftime("%d/%m/%Y"),
            'Domain': 'student.chula.ac.th'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': self.cookie
        }

        response = requests.request("POST", self.borrow_url, headers=headers,
                                    data=self.payload_encoder(payload), allow_redirects=False)

        if response.status_code != 302:
            raise Exception("Borrow failed")

        print("Borrow success")

    def payload_encoder(self, payload):
        return "&".join("%s=%s" % (k, v) for k, v in payload.items())


if __name__ == "__main__":
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    azure_user_id = os.getenv("AZURE_USER_ID")

    bot = ChulaLicenseBorrow(username, password, azure_user_id)
    bot.login()

    today = datetime.datetime.now()
    next_7_days = today + datetime.timedelta(days=7)

    bot.borrow(today, next_7_days, ProgramLicenseID.AdobeCreativeCloud)
