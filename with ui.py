from multiprocessing import process
from multiprocessing.context import Process
import sys

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QScrollArea
import requests
from bs4 import BeautifulSoup
import random
width = 1600
height = 900
x = 0
y = 0
reddy = True
class WallhavenDownloader(QtWidgets.QMainWindow):
    global x
    global y
    global reddy
    def __init__(self):
        global x
        global y
        super(WallhavenDownloader, self).__init__()
        uic.loadUi('wallhaven_downloader.ui', self)
        self.show()
        #widget = QtWidgets.QWidget()
        #self.layout = QtWidgets.QGridLayout(widget)#QVBoxLayout(widget)
        # Get the page with the latest wallpapers
        self.add_widgets(5)
        self.adding_widgets = False
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.check_scroll_position)
        
        # Set the widget as the scroll area's widget
        #self.scroll_area.setWidget(self.widget)
    
    def check_scroll_position(self):
        if not self.adding_widgets and self.scroll_area.verticalScrollBar().value() == self.scroll_area.verticalScrollBar().maximum():
            print("loading more")
            self.add_widgets(5)
            
        else:
            pass

    def add_widgets(self, n):
        global x
        global y
        self.adding_widgets = True
        chance = random.randint(1,5)
        if chance == 1:
            url = f'https://wallhaven.cc/search?categories=010&purity=100&ratios=landscape&sorting=hot&order=desc&ai_art_filter=1&page='+str(random.randint(1,7))
        if chance == 2 or chance == 3:
            url = f'https://wallhaven.cc/search?categories=010&purity=100&ratios=landscape&sorting=random&order=desc&ai_art_filter=1&page='+str(random.randint(1,1000))
        if chance == 4 or chance == 5:
            url = f'https://wallhaven.cc/search?categories=010&purity=100&ratios=landscape&topRange=1M&sorting=toplist&order=desc&ai_art_filter=1&page='+str(random.randint(1,40))
        print(chance)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all the thumbnail links
        thumbs = soup.find_all('a', {'class': 'preview'})[:30]
        self.thumb_links = [thumb['href'] for thumb in thumbs]
        thumbnails = soup.find_all('img', class_='lazyload')
        # Create a scroll area to display the thumbnails
        
        #scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        #self.setCentralWidget(self.scroll_area)
        
        # Create a widget to hold the thumbnails
        #widget = QtWidgets.QWidget()
        #self.layout = QtWidgets.QGridLayout(widget)#QVBoxLayout(widget)
        '''
        # Add the thumbnails to the layout
        for thumb_link in self.thumb_links:
            # Get the page for the thumbnail
            response = requests.get(thumb_link)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the thumbnail image link
            img = soup.find('img', {'id': 'wallpaper'})
            thumb_img_link = img['src']#.replace('//w.', '//th.')
            
            # Download the thumbnail image
            response = requests.get(thumb_img_link)
        '''

        for thumbnail in thumbnails:
            global x
            global y

            image_url = thumbnail['data-src']
            response = requests.get(image_url)
            
            # Create a label to display the thumbnail image
            label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            label.setPixmap(pixmap)
            
            # Add the label to the layout
            if x <= 4:
                self.layout.addWidget(label,y,x)
                x = x+1
                print("x incremented")

            elif x>4:
                self.layout.addWidget(label,y,x)
                y= y+1
                x = 0
                print("x deducted")
            print(x,y)

            
            # Connect the label's clicked signal to the download_image method
            label.mousePressEvent = lambda event, thumb_linkk=thumbnail: self.download_image(event, thumb_linkk)
        
        #self.scroll_area.setWidget(self.widget)
        
        QtCore.QTimer.singleShot(100, lambda: setattr(self, 'adding_widgets', False))

    
    def download_image(self, event, thumb_link):
        # Get the page for the chosen thumbnail
        thumb_link = str(thumb_link)
        print("bhai ye hai raww", thumb_link)
        image_id = thumb_link.replace('<img alt="loading" class="lazyload" data-src="',"").replace('" src=""/>',"")
        image_id=image_id.split("small")
        image_id = image_id[1]
        print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",image_id)
        image_id=image_id.split("/")
        image_id=image_id[2].replace(".jpg","")

        print("It's a nice dayyyy",image_id)
        thumb_linkkk = 'https://wallhaven.cc/w/'+image_id
        print("thumblinkkkkkkk",thumb_linkkk)
        response = requests.get(thumb_linkkk)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the full-size image link
        img = soup.find('img', {'id': 'wallpaper'})
        img_link = img['src']
        print(img_link)
        
        # Download the image
        response = requests.get(img_link,headers={"User-Agent": "Mozilla/5.0"})
        
        # Save the image to a file
        filename = img_link.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(response.content)

app = QtWidgets.QApplication(sys.argv)
window = WallhavenDownloader()
app.exec_()
