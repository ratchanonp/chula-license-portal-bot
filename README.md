# License Borrow Bot

## Description

Have you ever wanted to use adobe creative cloud or zoom but you forgot to borrow it from IT Chula? Well, this bot is here to help you. This bot will borrow the license for you and return it when you are done. You can also set a time limit for the license to be borrowed.

If you want it to automatically borrow the license for you, you can set cronjob to run the bot every week (for adobe creative cloud) or every 3 months (for zoom).

## How to use

1. Clone this repository
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a .env file and add your username, password, and azure User ID

```env
USERNAME=your_username
PASSWORD=your_password
AZURE_USER_ID=your_azure_user_id
```

Note that:

- Username is your Chula Email
- Password is your Chula Password
- You can get your azure user id by going to [Borrow Page](https://licenseportal.it.chula.ac.th/Home/Borrow) and inspecting the page. Then, search for `AzureUserId` and copy the value.

4. Run the bot

```python
python main.py
```

## How to set cronjob

1. Open terminal and type

```terminal
crontab -e
```

2. Add this line to the file

```terminal
0 0 * * 0 python /path/to/main.py
```

for more cronjob syntax, you can check [here](https://crontab.guru/)

3. Save the file and you are done!
