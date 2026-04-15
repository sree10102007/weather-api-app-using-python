import sys

import PyQt5
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class weatherapp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter City Name:",self)
        self.textbox=QLineEdit(self)
        self.button=QPushButton("Get Weather",self)
        self.templabel=QLabel(self)
        self.description=QLabel(self)
        self.emoji=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox=QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.textbox)
        vbox.addWidget(self.button)
        vbox.addWidget(self.templabel)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.description)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.templabel.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city")
        self.textbox.setObjectName("box")
        self.button.setObjectName("button")
        self.templabel.setObjectName("temp")
        self.emoji.setObjectName("emoji")
        self.description.setObjectName("description")

        self.setStyleSheet('''
         QLabel,Qpushbutton{
         font-family:calibri;}
         
        QLabel#city{
        font-size:40px;
        font-style:italic;
        }
        
        QLineEdit#box{
        font-size:40px;
        }
        
        QPushButton#button{
        font-size:40px;
        font-weight:bold;
        background-color:rgb(114, 2, 199)}
        
        QLabel#emoji{
        font-size:100px;
        font-family:segoe UI emoji;}
        
        QLabel#temp{
        font-size:40px;
        }
        
        QLabel#description{
        font-size:40px;}
        
        
        ''')
        self.button.clicked.connect(self.getweather)


    def getweather(self):
        apikey="c12f55df4b39e78db528e1e08097413a"
        city=self.textbox.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"

        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            if data["cod"]==200:
                self.displayweather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.displayerror("Bad Request \n please check your input")
                case 401:
                    self.displayerror("unpthorized \n invalid api key")

                case 403:
                    self.displayerror("forbiden \n acess denied")

                case 404:
                    self.displayerror("not found\ncity not found")

                case 500:
                    self.displayerror("server error")

                case 502:
                    self.displayerror("bad gateway")

                case 503:
                    self.displayerror("server is down")

                case 504:
                    self.displayerror("server down")

                case _:
                    self.displayerror(f"HTTP Error{http_error}")


        except requests.exceptions.ConnectionError:
            self.displayerror("connection error \n check your connection")

        except requests.exceptions.RequestException:
            self.displayerror("Time out error \n Request time out")

        except requests.exceptions.TooManyRedirects:
            self.displayerror("too many redirects check the url")

        except requests.exceptions.RequestException as reqerror:
            self.displayerror(f"request error {reqerror}")


    def displayerror(self,message):
        self.templabel.setStyleSheet("font-size:25px")
        self.templabel.setText(message)
        self.emoji.clear()
        self.description.clear()


    def displayweather(self,data):
        self.templabel.setStyleSheet("font-size:40px")
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k-273.15
        self.templabel.setText(f"{temperature_c:.0f} °C")
        id=data["weather"][0]["id"]
        weatherdescription=data["weather"][0]["description"]
        self.description.setText(weatherdescription)
        self.description.setStyleSheet("font-size:40px")
        self.emoji.setText(self.eemoji(id))

    @staticmethod
    def eemoji(id):
        if 200<=id>=232:
            return" 🌤️"
        elif 300<= id>=321:
            return "💭"

        elif 500<= id >= 531 :
            return "🌧️"

        elif 600<=id>= 622 :
            return "❄️"

        elif 701 <=id>=741:
            return"🌫️"

        elif id==762:
            return"🌋"

        elif id==771:
            return"💨"

        elif id==781:
            return"🌪️"

        elif id==800:
            return "☀️"

        elif id==804:
            return "🌥️"

        else:
            return ""


if __name__ =='__main__':
    app=QApplication(sys.argv)
    window=weatherapp()
    window.show()
    sys.exit(app.exec_())
