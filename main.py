import pickle
import pandas as pd
import clipboard
from tkinter import Frame,Label,Entry,Button,StringVar,Tk
import webbrowser
from url_feature_extraction import *

root =Tk()
root.configure(bg='#6787d6')

# setting the windows size
root.geometry("600x600")
loaded_model = pickle.load(open("RandomForest.pickle.dat", "rb"))
    
#Function to extract features
def featureExtraction(url):
  print('Feature Extracting....')
  features = []
  #Address bar based features (10)
  #features.append(0)
  #features.append(getLength(url))
  #features.append(getDepth(url))

  features.append(havingIP(url))
  features.append(haveAtSign(url))
  features.append(redirection(url))
  features.append(httpDomain(url))
  features.append(tinyURL(url))
  features.append(prefixSuffix(url))
  
  #Domain based features (4)
  dns = 0
  try:
    domain_name = whois.whois(urlparse(url).netloc)
  except:
    dns = 1
  features.append(dns)
  features.append(web_traffic(url))
  features.append(1 if dns == 1 else domainAge(domain_name))
  features.append(1 if dns == 1 else domainEnd(domain_name))
  
  # HTML & Javascript based features
  import requests
  try:
    response = requests.get(url)
  except:
    response = ""

  features.append(iframe(response))
  features.append(mouseOver(response))
  features.append(rightClick(response))
  features.append(forwarding(response))  
  
  legi_features = []
  legi_features.append(features)
    
  #converting the list to dataframe
  feature_names = ['Have_IP', 'Have_At','Redirection','https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic', 
                          'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards']
    
  urlclass = pd.DataFrame(legi_features,columns = feature_names)
    
  detect = loaded_model.predict(urlclass)
  
  if detect==0:
      print("Done Extracting")
      print("Given Website is Legitimate")
      outputlabel.configure(text= getDomain(url) + '\nis legitimate')
  else:
      print("Done Extracting")
      print("Given Website is Phishing")
      temp = getDomain(url) + ' is phishing'
      " ".join(temp.split())
      if len(outputlabel['text']) > 20:
          outputlabel.configure(text= 'Above website \nis phishing')
      else:
          outputlabel.configure(text= getDomain(url) + '\nis phishing')
  return 0

def setTextInput(text):
    print(1)
    textEntry.set(text)

def callback(url):
    webbrowser.open_new(url)

def clearentry():
    url_entry.delete(0,'end')
    outputlabel.configure(text= 'Output will be shown here')
    
displayFrame = Frame(root,bg ='#6787d6')
displayFrame.pack()

detailsframe = Frame(displayFrame,bg='#d8dbe3')
detailsframe.pack(padx=40,pady=100)

desclabel= Label(detailsframe,text = 'Phishing Website Detection Using \n Machine Learning Techinque ',height=2,bg='#d8dbe3',font=('default',20))
desclabel.grid(columnspan=5)

asklabel= Label(detailsframe,text = 'Paste url to check',font=('default',14),bg='#d8dbe3',height=2)
asklabel.grid(row=1,padx=80,columnspan=5)

textEntry = StringVar()
url_entry = Entry(detailsframe,textvariable = textEntry,width=20,font=('default',12))
url_entry.grid(row = 2,column=1,columnspan=3,pady=10,rowspan=2)

pastebutton = Button(detailsframe,text='Paste',width=5,bg='#6787d6',font=('default',8),command=lambda:setTextInput(clipboard.paste()))
pastebutton.grid(row =2,column=3,pady=1,columnspan=2)

clearbutton = Button(detailsframe,text='Clear',width=5,bg='#de4b69',font=('default',8),command=lambda:clearentry())
clearbutton.grid(row =3,column=3,pady=1,columnspan=2)

checkbutton = Button(detailsframe,text='Check',width=10,bg='#6787d6',font=('default',13),command=lambda:featureExtraction(url_entry.get()))
checkbutton.grid(columnspan=5,pady=10)

outputlabel = Label(detailsframe,text='output will be shown here',font=('default',12),bg='#d8dbe3',height=2)
outputlabel.grid(padx=80,columnspan=5,pady=15)

link1 = Label(detailsframe, text="Know more about phishing", fg="blue", cursor="hand2",font=('default',12),bg='#d8dbe3',height=2)
link1.grid(columnspan=5,pady=10)
link1.bind("<Button-1>", lambda e: callback("https://en.wikipedia.org/wiki/Phishing"))

root.mainloop()