<img src="amz.jpg" alt="leech" width="500" height="500">

## AMZ-LEECH: Amazon rewards account creator

[!] JUST A PoC!!!! YOU WILL GET BANNED!!!!!!!
[!] JUST A PoC!!!! YOU WILL GET BANNED!!!!!!!

AMZ-LEECH its a script designed to automate the creation of amz accounts and take adventage of [amazon affiliates program](https://afiliados.amazon.es/).

* [Wedding Form](http://www.amazon.es/wedding?tag=) gives you **3.5 €**
* [Baby Form](http://www.amazon.es/baby-reg/homepage?tag=)  gives you **1.5€**

A close friend noticed that by having the right services to receive temporary [SMS](https://sms-man.com) and [mails](https://www.byom.de), amazon accounts could be created with high frequency, so I decided to automate that process

```
git clone https://TOKEN@github.com/blueudp/amz-leech.git
pip install -r requirements.txt
install "firefox 78.11.0esr" (64-bit)
install geckodriver (mv deps/geckodriver /usr/bin)
python3 leech.py REF_CODE country

```

# How to

Run the script and wait until the program prints `Send form and continue>`, then wait until leech.py prints `Captcha>`, this time do not send form!
Otherwise program wont find send button so it will crash

# PoC 5 € in 1 minute



https://user-images.githubusercontent.com/41192980/130110078-26d98c6e-9a00-4bbb-9182-4f1d6f840fad.mp4



# SMS Man

each message received costs about 0.22 €

AMZ-leech use sms-man.com API services, countries are written in **deps/phones.txt**, following this structure

```
country,smsmanAPIcountryID,AmzCountryIDFromDesplegableList
portugal,263,166
francia,155,69
alemania,123,2
grecia,222,76
irlanda,106,93
italia,163,108
uk,100,170
españa,155,61

```
# CONFIG
API=SMS_MAN_API_KERE

Proxy=False

# Proxy
If you want to use proxy in amz browser set **proxy=True** in CONFIG

Then add proxys in this format `IP:PORT` to **deps/proxy.txt**

# Other features

1. random screen size
2. random ua
3. random proxy
4. auto fill every form
5. If API returns no number try another country
6. select phone country
