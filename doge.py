
#!/usr/bin/env python

import gtk
import appindicator
import urllib2
import os 
import Tkinter
from Tkinter import *
import urllib
'''
TODO:
vverify url to get data. show error text insted of hashrate

'''

class DogeCoin:
  def __init__(self):
    self.ind = appindicator.Indicator("hashrate-indicator",os.path.join(os.getcwd(),Settings.ImageName),appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status(appindicator.STATUS_ACTIVE)
    self.ind.set_label("HR: ")
    self.menu_setup()
    self.ind.set_menu(self.menu)

  def menu_setup(self):
    self.menu = gtk.Menu()
    self.quit_item = gtk.MenuItem("Quit")
    self.quit_item.connect("activate", self.quit)
    self.quit_item.show()
    self.setting_item = gtk.MenuItem("Settings")    
    self.setting_item.connect("activate", self.settings)
    self.setting_item.show()
    self.menu.append(self.setting_item)
    self.menu.append(self.quit_item)

  def main(self):
    self.getHash()
    gtk.main()

  def quit(self, widget):
    sys.exit(0)
    
  def settings(self, widget):
      app = settingsWindow(None)
      app.title('DogeCoin Settings')
      img = PhotoImage(file=os.path.join(os.getcwd(),Settings.ImageName))
      app.tk.call('wm', 'iconphoto', app._w, img)
      app.mainloop()
  
  def getHash(self):
    req = urllib2.Request("http://nissil.si/doge/index.php?url="+urllib.quote(Settings.Request_Url, ''))
    try:
      page = urllib2.urlopen(req)
      content = page.read()
      self.ind.set_label("HR: "+content+" KH/s")
    except urllib2.HTTPError, e:
        print e.fp.read()
    gtk.timeout_add(Settings.PING_FREQUENCY * 1000, self.getHash)
    
    


class settingsWindow(Tkinter.Tk):
  def __init__(self,parent):
    Tkinter.Tk.__init__(self,parent)
    self.parent = parent
#    parent.protocol('WM_DELETE_WINDOW', parent.destroy())
    self.initialize()
    self.center()

  def initialize(self):     
      self.inputUrl = Tkinter.Entry(self, width=30)
      self.inputUrl.grid(column=0,row=2,sticky='EW')
      self.inputUrl.insert(0,Settings.Request_Url)
      button = Tkinter.Button(self,text=u"Change url", command=self.ChangeSettings)
      button.grid(column=1,row=2)
      label = Tkinter.Label(self,anchor="w",text="Please enter URL of pool API")
      label.grid(column=0,row=1,columnspan=2,sticky='EW')
      self.var = StringVar()
      self.var.set(Settings.Request_Rrequency)
      dropdown=Tkinter.OptionMenu(self, self.var, *Settings.choices, command=self.ChangeRefresh)
      dropdown.grid(column=0,row=5)
      label = Tkinter.Label(self,anchor="w",text="Select refresh interval")
      label.grid(column=0,row=4,columnspan=2,sticky='EW')
      self.grid()   
 
  def ChangeRefresh(self, *args):
      reversePrettify(args[0])
      
  def ChangeSettings(self):
    Settings.Request_Url=self.inputUrl.get()

  def center(self):
      w = 350
      h = 150
      # get screen width and height
      ws = self.winfo_screenwidth()*1.5
      hs = self.winfo_screenheight()
      # calculate position x, y
      x = (ws/2) - (w/2)
      y = (hs/2) - (h/2)
      self.geometry('%dx%d+%d+%d' % (w, h, x, y))

class Settings(object):
    PING_FREQUENCY = 10 # seconds
    Request_Rrequency = "10s"
    Request_Url="https://doge.nut2pools.com/index.php?page=api&action=getuserstatus&api_key=7ee47e8208499ea007b2d803ae70e57babba13f86cadc45ac442ee1e78170787&id=5133"
    choices = ['10s', '30s', '1m', '2m','5m', '10m', '30m']
    ImageName = "dogeLogo.png"

def reversePrettify(freq):
  if freq == "10s":
    Settings.Request_Rrequency = "10s"
    Settings.PING_FREQUENCY = 10
  elif freq == "30s":
    Settings.Request_Rrequency = "30s"
    Settings.PING_FREQUENCY = 30
  elif freq == "1m":
    Settings.Request_Rrequency = "1m"
    Settings.PING_FREQUENCY = 60
  elif freq == "2m":
    Settings.Request_Rrequency = "2m"
    Settings.PING_FREQUENCY = 120
  elif freq == "5m":
    Settings.Request_Rrequency = "5m"
    Settings.PING_FREQUENCY = 300
  elif freq == "10m":
    Settings.Request_Rrequency = "10m"
    Settings.PING_FREQUENCY = 600
  elif freq == "30m":
    Settings.Request_Rrequency = "30m"
    Settings.PING_FREQUENCY = 1800
    
    
if __name__ == "__main__":
  indicator = DogeCoin()
  indicator.main()
    
