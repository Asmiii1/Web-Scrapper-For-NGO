# Store this code in 'app.py' file
import fp as fp
from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd
global df1
global df



app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'geeklogin'
app.config["MYSQL_CURSORCLASS"] = ""

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password,))
        accounts = cursor.fetchone()
        if accounts:
            session['loggedin'] = True

            session['username'] = accounts['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/about')
def about():
    return render_template('about.html')





@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'secure password'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = "give email"
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES ( % s, % s, % s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)



def scrap():
    url1 = "https://hindrise.org"
    r1 = requests.get(url1)
    htmlContent1 = r1.content

    soup1 = BeautifulSoup(htmlContent1, 'html.parser')
    t1 = soup1.find("meta", property="og:site_name")
    title1 = t1["content"]

    a1 = soup1.find_all('a', href="contact-us")
    address1 = a1[2].text

    a11 = soup1.find_all('a', href="tel:+91-7303409010")
    tel1 = a11[0].text

    # mumbai
    url2 = "https://www.abhilasha-foundation.org"
    r2 = requests.get(url2)
    htmlContent2 = r2.content

    soup2 = BeautifulSoup(htmlContent2, 'html.parser')
    title2 = soup2.title.text

    a2 = soup2.find_all('p')
    address2 = a2[24].text
    tel2 = a2[25].text

    url3 = "https://www.connectfor.org/contact-us"
    r3 = requests.get(url3)
    htmlContent3 = r3.content

    soup3 = BeautifulSoup(htmlContent3, 'html.parser')
    title3 = "Connect For"

    a3 = soup3.find_all('p')
    address3 = a3[15].text
    tel3 = a3[17].text

    # Mumbai
    url7 = "https://www.giveindia.org/nonprofit/dignity-foundation"
    r7 = requests.get(url7)
    htmlContent7 = r7.content

    soup7 = BeautifulSoup(htmlContent7, 'html.parser')
    title7 = soup7.title.text

    a7 = soup7.find_all('p')
    address7 = a7[4].text
    tel7 = a7[5].text

    # delhi
    url8 = 'https://www.vridhcare.com/'
    r8 = requests.get(url8)
    htmlContent8 = r8.content

    soup8 = BeautifulSoup(htmlContent8, 'html.parser')
    title8 = soup8.title.text
    a8 = soup8.find_all("p")
    address8 = a8[3].text
    tel8 = a8[2].text

    inter = [['Name of NGO', 'Address', 'Contact Number'], [title1, address1, tel1], [title2, address2, tel2],
             [title3, address3, tel3], [title7, address7, tel7], [title8, address8, tel8]]
    df = pd.DataFrame(inter)

    return df


def scrap1():
    url4 = "https://www.careindia.org/contact-us/"
    r4 = requests.get(url4)
    htmlContent4 = r4.content

    soup4 = BeautifulSoup(htmlContent4, 'html.parser')
    t4 = soup4.title.text
    title4 = t4[13:]

    a4 = soup4.find_all('p')
    # Chennai
    a400 = a4[25].text

    # new delhi
    a410 = a4[0].text

    # Bihar
    a420 = a4[3].text
    a421 = a4[4].text

    # Chhattisgarh
    a430 = a4[5].text

    # Gujarat
    a440 = a4[6].text
    a441 = a4[7].text
    a442 = a4[8].text
    a443 = a4[9].text
    a444 = a4[10].text
    a445 = a4[11].text

    # Haryana
    a450 = a4[12].text

    # Bangalore
    a460 = a4[13].text
    a461 = a4[14].text

    # madhya pradesh
    a470 = a4[15].text

    # Maharashtra
    a480 = a4[16].text
    a481 = a4[17].text

    # Odisha
    a490 = a4[19].text
    a491 = a4[20].text
    a492 = a4[21].text
    a493 = a4[22].text

    # Rajasthan
    aa400 = a4[23].text
    aa401 = a4[24].text

    # Tamil Nadu
    aa410 = a4[26].text
    aa411 = a4[27].text

    # UP
    aa420 = a4[28].text

    a44 = soup4.find_all('a', href="tel:01169200000")
    tel4 = a44[0].text

    url5 = "https://www.sparkachangefoundation.org/top-ngos-in-india.php"
    r5 = requests.get(url5)
    htmlContent5 = r5.content

    soup5 = BeautifulSoup(htmlContent5, 'html.parser')
    t5 = soup5.find_all('td')

    # New Delhi
    title50 = t5[43].text
    address50 = t5[55].text

    # Mumbai
    title51 = t5[1].text
    address51 = t5[13].text
    tel51 = address51[111:]

    title52 = t5[99].text
    address52 = t5[111].text
    tel52 = address52[63:]

    title53 = t5[127].text
    address53 = t5[139].text
    tel53 = address53[106:]

    title54 = t5[141].text
    address54 = t5[153].text
    tel54 = address54[88:]

    title55 = t5[155].text
    a55 = t5[167].text
    address55 = a55[:109]
    tel55 = a55[109:]

    title56 = t5[231].text
    a56 = t5[241].text
    address56 = a56[:121]
    tel56 = a56[121:]

    title57 = t5[255].text
    a57 = t5[267].text
    address57 = a57[:131]
    tel57 = a57[131:]

    # print(t5)

    # Bangalore
    title58 = t5[183].text
    address58 = t5[193].text

    # new delhi
    title59 = t5[207].text
    a59 = t5[217].text
    address59 = a59[:39]
    tel59 = a59[39:]

    url6 = "https://www.smilefoundationindia.org/contactus.html"
    r6 = requests.get(url6)
    htmlContent6 = r6.content

    soup6 = BeautifulSoup(htmlContent6, 'html.parser')
    t6 = soup6.title.text
    title6 = t6[101:]

    a6 = soup6.find_all("p")

    # New delhi
    a60 = a6[42].text
    address60 = a60[:85]
    tel60 = a60[85:131]

    # hyderabad
    a61 = a6[44].text
    address61 = a61[:71]
    tel61 = a61[71:94]

    # mumbai
    a62 = a6[45].text
    address62 = a62[:93]
    tel62 = a62[93:119]


    # kolkata
    a63 = a6[46].text
    address63 = a63[:117]
    tel63 = a63[117:137]

    # bangalore
    a64 = a6[47].text
    address64 = a64[:114]
    tel64 = a64[114:134]

    # chennai
    a65 = a6[48].text
    address65 = a65[:102]
    tel65 = a65[102:125]

    # pune
    a66 = a6[49].text
    address66 = a66[:99]
    tel66 = a66[99:120]

    child_name = [['Name of NGO', 'Address', 'Contact Number'], [title4, a400, tel4], [title6, address65, tel65],
                  [title4, aa410, tel4], [title4, aa411, tel4],
                  [title4, a410, tel4], [title50, address50, 'null'], [title59, address59, tel59],
                  [title6, address60, tel60],
                  [title4, a420, tel4], [title4, a421, tel4],
                  [title4, a430, tel4],
                  [title4, a440, tel4], [title4, a441, tel4], [title4, a442, tel4], [title4, a443, tel4],
                  [title4, a444, tel4], [title4, a445, tel4],
                  [title4, a450, tel4],
                  [title4, a460, tel4], [title4, a461, tel4], [title58, address58, "null"], [title6, address64, tel64],
                  [title4, a470, tel4],
                  [title4, a480, tel4], [title4, a481, tel4], [title51, address51, tel51], [title52, address52, tel52],
                  [title53, address53, tel53], [title54, address54, tel54], [title55, address55, tel55],
                  [title56, address56, tel56], [title57, address57, tel57], [title6, address62, tel62],
                  [title6, address66, tel62],
                  [title4, a490, tel4], [title4, a491, tel4], [title4, a492, tel4], [title4, a493, tel4],
                  [title4, a400, tel4], [title4, aa401, tel4],
                  [title4, aa420, tel4],
                  [title6, address63, tel63]]
    df1 = pd.DataFrame(child_name)
    return df1
def scrap2():
    url1 = "https://hindrise.org"
    r1 = requests.get(url1)
    htmlContent1 = r1.content

    soup1 = BeautifulSoup(htmlContent1, 'html.parser')
    t1 = soup1.find("meta", property="og:site_name")
    title1 = t1["content"]

    a1 = soup1.find_all('a', href="contact-us")
    address1 = a1[2].text

    a11 = soup1.find_all('a', href="tel:+91-7303409010")
    tel1 = a11[0].text

    # mumbai
    url2 = "https://www.abhilasha-foundation.org"
    r2 = requests.get(url2)
    htmlContent2 = r2.content

    soup2 = BeautifulSoup(htmlContent2, 'html.parser')
    title2 = soup2.title.text

    a2 = soup2.find_all('p')
    address2 = a2[24].text
    tel2 = a2[25].text

    url3 = "https://www.connectfor.org/contact-us"
    r3 = requests.get(url3)
    htmlContent3 = r3.content

    soup3 = BeautifulSoup(htmlContent3, 'html.parser')
    title3 = "Connect For"

    a3 = soup3.find_all('p')
    address3 = a3[15].text
    tel3 = a3[17].text

    # Mumbai
    url7 = "https://www.giveindia.org/nonprofit/dignity-foundation"
    r7 = requests.get(url7)
    htmlContent7 = r7.content

    soup7 = BeautifulSoup(htmlContent7, 'html.parser')
    title7 = soup7.title.text

    a7 = soup7.find_all('p')
    address7 = a7[4].text
    tel7 = a7[5].text

    # delhi
    url8 = 'https://www.vridhcare.com/'
    r8 = requests.get(url8)
    htmlContent8 = r8.content

    soup8 = BeautifulSoup(htmlContent8, 'html.parser')
    title8 = soup8.title.text
    a8 = soup8.find_all("p")
    address8 = a8[3].text
    tel8 = a8[2].text

    old_age = [['Name of NGO', 'Address', 'Contact Number'], [title1, address1, tel1], [title2, address2, tel2],
               [title3, address3, tel3], [title7, address7, tel7], [title8, address8, tel8]]

    df2 = pd.DataFrame(old_age)
    return df2
@app.route('/Table/')
def table():
    sdata = scrap()
    print(sdata)

    return render_template('table.html', sdata=[sdata.to_html()],titles=[''])

@app.route('/Table1/')
def table1():
    sdata = scrap1()
    print(sdata)

    return render_template('table1.html', sdata=[sdata.to_html()],titles=[''])




@app.route('/Table2/')
def table2():
    sdata = scrap2()
    print(sdata)

    return render_template('table2.html', sdata=[sdata.to_html()],titles=[''])



if __name__ == "__main__":
    app.run(debug=True)
