#!/usr/bin/env python
# coding: utf-8

# In[10]:


from bs4 import BeautifulSoup as bs
from email.message import EmailMessage
import pandas as pd
import smtplib, ssl, mimetypes, requests, getpass
import schedule, time, datetime, pytz


# In[11]:


def weather_forecast_berlin(sender, password, receiver): #sender, password, receiver
    
    # define pandas dataframe to safe data of forecast
    weather_data = pd.DataFrame(    
        {'Date':[],
         'Day':[],
         'Weather':[],
         'Min temperature':[],
         'Max temperature':[],
         'Min windspeed':[],
         'Max windspeed':[],
         'Rain probability': [],
         'Rainfall':[]
        })
    
    # website for day 1 to 7 in Berlin
    path_1_7 = 'https://www.daswetter.com/wetter_Berlin-Europa-Deutschland-Berlin--1-26301.html'
    # website for day 8 to 14 in Berlin
    path_8_14 = 'https://www.daswetter.com/wetter_Berlin-Europa-Deutschland-Berlin--nxw-26301.html'

    for i in range(1,15):

        if i<8:
            soup = bs(requests.get(path_1_7).content)
        else:
            soup = bs(requests.get(path_8_14).content)

        if i==1 or i==8:
            class_='dia d'+str(i)+' activo'
        else:
            class_='dia d'+str(i)
        
        # crawl data from website
        data = soup.find(class_= class_)
        date = data.find(class_='cuando').contents[2].contents[0]
        day = data.find(class_='cuando').contents[0]
        weather = data.find(class_='simbW')['alt']
        temp_min = data.find(class_='minima changeUnitT').contents[0]
        temp_max = str(data.find(class_='maxima changeUnitT').contents[0])
        wind_speed_min = data.find(class_='velocidad').find_all(class_='changeUnitW')[0].string
        wind_speed_max = data.find(class_='velocidad').find_all(class_='changeUnitW')[1].string
        
        # rain data only available if weather is rainy
        try:
            rain_prob = data.find(class_='probabilidad-lluvia').contents[0]
            rain = data.find(class_='probabilidad-lluvia').contents[3].string
        except:
            rain_prob = 'low'
            rain = 'around 0 mm'
        
        # safe data in new pandas data frame
        new_entry = pd.DataFrame(    
        {'Date':[date],
         'Day':[day],
         'Weather':[weather],
         'Min temperature':[temp_min],
         'Max temperature':[temp_max],
         'Min windspeed':[wind_speed_min],
         'Max windspeed':[wind_speed_max],
         'Rain probability': [rain_prob],
         'Rainfall':[rain]
        })
        
        # add new weather entry to table
        weather_data = pd.concat([weather_data, new_entry], ignore_index=True)
    
    # safe data in csv file
    weather_forecast_14days = weather_data.to_csv('weather_forecast_14days.csv', index = True)


    # compose email
    # define everything that is need for the email
    subject = 'Weather forecast for Berlin for the next 14 days'
    body = """    <html>
      <head></head>
      <body>
        <p>Hi Lisa,<br>
            <p>
            You can find the weather forecast for Berlin for the next 14 days in the attached CSV file.<br>
            The data is crawled from that <a href = "https://www.daswetter.com/wetter_Berlin-Europa-Deutschland-Berlin--1-26301.html">website</a>.
            </p>
            <p>
            Best regards,<br>
            Your helping bot  
            </p>
        </p>
      </body>
    </html>
    """

    file = 'weather_forecast_14days.csv'
    path = f'{file}'

    # create an email object
    mail = EmailMessage()
    mail['From'] = sender
    mail['To'] = receiver
    mail['Subject'] = subject
    mail.add_alternative(body, subtype="html")

    # make file readable
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    
    # attach a file to email
    with open(path, 'rb') as fp:
        mail.add_attachment(fp.read(), maintype=maintype, subtype=subtype, 
                           filename=file)

    # create a secure connection with ssl & send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, mail.as_string())
        print('email send')


# In[12]:


# user input for sender and receiver email
sender = input('Which email address would you like to use to send the weather forecast?') #I used my developer email:'dev.acc1222@gmail.com'
password = getpass.getpass('Type in your password:')       #oydyjkhifrhmnjaa, input is hidden; for gmail you need a generated app-password to login
receiver = input('Who should receive the weather forcast?')

# define time period to get email (14 days) & time of the day one receives the forecast
schedule_time = input('At which time of the day would you like to receive the forecast? e.g. 14:47')
current_time = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
time_change = datetime.timedelta(days=14)
end_date = str(current_time + time_change)[:-16]

schedule.every().day.at(schedule_time).until(end_date).do(weather_forecast_berlin, sender=sender, password=password, receiver=receiver)

# repeat to check if the time of the date is equal to the "time" when you want to receive the email
while True:
    schedule.run_pending()
    time.sleep(60)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




