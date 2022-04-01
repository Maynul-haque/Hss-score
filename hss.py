import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import anvil.server


anvil.server.connect("56QKF5UQYD2UTTLNTYKDW7HY-IZ5NVFY5T7JHEZG2")

df = pd.DataFrame()

@anvil.server.callable
def show_ranking_data():
  url = 'http://103.247.238.92/webportal/pages/hss_menu_facility.php?facilitytype_id=29&division_id=&district_id='
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'lxml')
  table_row = soup.find('div', {'class':"box-body"}).find_all('tr')


  tab_link =[]
  for i in table_row:
    if (i.find('td', text = 'Cumilla')) !=  None:
      tab_link.append(i)

  name = [i.find('a').get_text() for i in tab_link ]

  all_numbers=[i.find_all("td",{"style":"text-align:center;"}) for i in tab_link]
  rank = []
  for i in all_numbers:
    j = i[0].get_text()
    rank.append(j)
  
  score = []
  for k in all_numbers:
    l = k[1].get_text()
    score.append(l)

  links_upazilla =['http://103.247.238.92/webportal/pages/'+i.find('a').get('href') for i in tab_link]


  df['Name'] = name

  for i in range(0, len(df['Name'])):
    df['Name'][i] = df['Name'][i].replace(' Upazila Health Complex','')
  
  df["Current Rank"] = rank
  df["Score (300)"] = score
  df['Link'] = links_upazilla

  # df["Score (300)"] = df['Score (300)'].astype(float)
  # plt.figure(figsize=(20, 8))
  # plt.barh(df['Name'], df['Score (300)'] )
  # plt.title("Ranking")
  # for i, v in enumerate(y):
  #   plt.text(v + 1, i + .00, str(v),
  #           color = 'blue', fontweight = 'bold')
  # plt.rc('ytick', labelsize =15)
  ranking_data = df[['Name', 'Current Rank','Score (300)']].copy()
  ranking_data = ranking_data.to_dict(orient="records")

  return ranking_data

  

dic = {
    'Service Delivery':0,
'Health Workforce':1,
'Health Information System':2,
'Access to Essential Medicines/ Equipment, logistics/ Utilities/ Infrastructure':3,
'Leadership/ Governance/ Management': 4,
'Access':5,
'Quality':6,
'Coverage':7,
'Safety':8,
'Onsite Monitoring':9
}




@anvil.server.callable
def get_data_table(upazilla,table_no):
  url = df['Link'][df.index[df['Name'] == upazilla].tolist()[0]]
  tab = pd.read_html(df['Link'][df.index[df['Name'] == f'{upazilla}'].tolist()[0]])[dic[table_no]].drop(['Dataset','Period','Numerator','Denominator','Score Calculation','Trend',"Definition",], axis = 1)
  tab = tab.to_dict(orient="records")
  return tab, url
  
  
anvil.server.wait_forever()