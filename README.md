# screener-project
final opim 244 project

Hey, welcome to my screener.

#### The Mission
My project has three objectives, and I hope that this may assist in their fulfillment:

1) Give retirees peace of mind by selecting value stocks that work for them, and pairing those with bonds that provide a stalwart portfolio.

2) Let adults have control over the investments they want to pursue following their risk profile. 

3) Give young investors confidence to invest in the growth stocks of the future. 


#### How to Use

In order to use my platform, 

Access the Github Repository: https://github.com/kis11/screen-project

Fork, then clone the repository, which contains the data files you'll need to use the screener.

Navigate to the screen-project folder on your terminal. If you have a Mac and put it on your Desktop, you can navigate by doing this:

```sh
cd ~/Desktop/screen-project
```

Once you are navigated to the folder, we need to create an environment. For the sake of this example we will call it screen-env. To create screen-env, do the following: 

```sh
conda create -n screen-env python=3.7 #first time only
conda activate screen-env
```

Now we need to install the necessary packages from the requirements.txt file by doing the following:

```sh
pip install -r requirements.txt
```

You're almost all set. 

Because this screener allows the data to be emailed to you, you also need to create a .env file that has the necessary API keys. Set 3 variables in your .env file:

```sh
SENDGRID_API_KEY =
MY_EMAIL_ADDRESS =
SENDGRID_TEMPLATE_ID =
```

Set the email address to the intended recipient. The template ID should be "d-b9d8944266ab41f4908dfc84875b8720". The API key was given to you when you made your account. 

Important: Make sure you also have a .gitignore file, that includes .env.

In your virtual environment, navigate to the app folder, and then type "python screener.py". 

You will be able to choose the age profile that fits you best. Type either "young investor", "retiree", or "adult". 

You will then be prompted to set a price you are willing to pay. Type what you feel comfortable, but make sure it is a number. 

Then, you will be prompted about whether or not you care about liquidity. If you are concerned that if you want to sell your stock, that there may not be a buyer, please say yes to the question. If not, choose no. 

You will then have the output shown to you on the screen. It may be too large to fit on the terminal, so you have the option to have the csv file emailed to your account. 

When prompted, if you want it emailed, enter yes. If you don't, answer no. 

Finally, our platform gives you the ability to get more information about the stocks you care about. If you want more background on the companies that were selected for you, reply yes to the "Want to know more" question. Then type in the ticker. You can continue to do this until you say no. 