import sys
from os import path
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.soccerstats.com/"

class scraper():

    def __init__(self, **kwargs):

        self.league = kwargs.get("league", 'france_2020')
        self.months = kwargs.get("months", ['month8'])

    #------------------------------------------------
    # Fetching URLS
    #------------------------------------------------
    def scrape_url_matches_by_month(self, month):
        print(f'fetching urls for month {month}')
        #Request
        response = requests.get(
            BASE_URL + 'results.asp',
            params={'league': self.league, 'pmtype': month}
            )
        #Soup
        soup = BeautifulSoup(response.text, "html.parser")
        #Table of matches
        table = soup.find('table', id= 'btable')

        #Fill dico score
        self.dico_data['url'] = self.dico_data['url'] + [matche['href'] for matche in table.find_all('a', class_= "vsmall")]
        self.dico_data['score'] = self.dico_data['score'] + [score.text for score in table.find_all('font', color = "gray")]
        self.dico_data['date'] = self.dico_data['date'] + [date.text for date in table.find_all('font', color = "green")]
        
        #Return list of href
        month_url = [matche['href'] for matche in table.find_all('a', class_= "vsmall")]
        print(f'found {len(month_url)} urls')
        return month_url

    def scrape_url_matches_by_year(self):
        print(f"Searching {self.league}")
        self.urls = []
        for month in self.months:
            self.urls = self.urls + self.scrape_url_matches_by_month(month)

    
    #------------------------------------------------
    # Init Dico
    #------------------------------------------------
    def init_dico_data(self):
    #Initialize Dico data
        self.dico_data = {}
        dico_keys = ['tm1_name', 'tm2_name', 'date' , 'score', 'url', \
                     'tm1_points_h', 'tm1_PPGH_h', 'tm1_GS_h', 'tm1_GC_h', 'tm0_GS_h',\
                    'tm2_points_a', 'tm2_PPGA_a', 'tm2_GS_a', 'tm2_GC_a', 'tm0_GS_a', 'tm0_PPGH', 'tm1_wins',\
                    'tm2_wins', 'tm0_wins', 'tm1_defeats', 'tm2_defeats', 'tm0_defeats', 'tm1_GSG', 'tm2_GSG',\
                    'tm0_GSG', 'tm1_GCG', 'tm2_GCG', 'tm0_GCG', 'tm1_D', 'tm2_D', 'tm0_D', 'tm1_TGG', 'tm2_TGG',\
                    'tm0_TGG', 'tm1_25', 'tm2_25', 'tm0_25', 'tm1_35', 'tm2_35', 'tm0_35', 'tm1_BTS', 'tm2_BTS',\
                    'tm0_BTS', 'tm0_PPGH_h', 'tm1_wins_h', 'tm0_wins_h', 'tm1_defeats_h', 'tm0_defeats_h',\
                    'tm1_GSG_h', 'tm0_GSG_h', 'tm1_GCG_h', 'tm0_GCG_h', 'tm1_D_h', 'tm0_D_h', 'tm1_TGG_h',\
                    'tm0_TGG_h', 'tm1_25_h', 'tm0_25_h', 'tm1_35_h', 'tm0_35_h', 'tm1_BTS_h', 'tm0_BTS_h',\
                    'tm0_PPGH_a', 'tm2_wins_a', 'tm0_wins_a', 'tm2_defeats_a', 'tm0_defeats_a', 'tm2_GSG_a',\
                    'tm0_GSG_a', 'tm2_GCG_a', 'tm0_GCG_a', 'tm2_D_a', 'tm0_D_a', 'tm2_TGG_a', 'tm0_TGG_a',\
                    'tm2_25_a', 'tm0_25_a', 'tm2_35_a', 'tm0_35_a', 'tm2_BTS_a', 'tm0_BTS_a']
        for k in dico_keys :
            self.dico_data[k] = []
            
    #------------------------------------------------
    # Scraping DATA
    #------------------------------------------------
    def scrape_data_from_url(self, url):
        print(url)
        #Request
        response = requests.get(BASE_URL + url)

        #Soup
        soup = BeautifulSoup(response.text, "html.parser")
        
        #Separate columns teams
        datas = soup.find_all('div', class_= "six columns")
        tm1 = datas[2].find_all('table') #infos on team 1
        tm2 = datas[3].find_all('table') #infos on team 2

        #------team names
        #tm0 = average for the league
        self.dico_data['tm1_name'].append(tm1[0].find('h2').text)
        self.dico_data['tm2_name'].append(tm2[0].find('h2').text)

        #------Home and away records
        #TM1 -> home
        tm1_records = tm1[5].find_all('tr')
        self.dico_data['tm1_points_h'].append(tm1_records[2].find_all('td')[2].text.replace('%','')) #home points in %
        self.dico_data['tm1_PPGH_h'].append(tm1_records[4].find_all("td")[1].text) #  Points Per Game at Home
        self.dico_data['tm1_GS_h'].append(tm1_records[7].find_all('td')[2].text.replace('%','')) # goals score in %
        self.dico_data['tm1_GC_h'].append(tm1_records[8].find_all('td')[2].text.replace('%','')) # goals conceded in %
        self.dico_data['tm0_GS_h'].append(tm1_records[9].find_all('td')[2].text.replace('%',''))#  League average (% goals)
        #TM2 -> away
        tm2_records = tm2[5].find_all('tr')
        self.dico_data['tm2_points_a'].append(tm2_records[2].find_all('td')[4].text.replace('%','')) #home points in %
        self.dico_data['tm2_PPGA_a'].append(tm2_records[5].find_all("td")[1].text)  # Points Per Game away
        self.dico_data['tm2_GS_a'].append(tm2_records[7].find_all('td')[4].text.replace('%','')) # goals score in %
        self.dico_data['tm2_GC_a'].append(tm2_records[8].find_all('td')[4].text.replace('%','')) # goals conceded in %
        self.dico_data['tm0_GS_a'].append(tm2_records[9].find_all('td')[4].text.replace('%',''))#  League average (% goals)

        #------ stats against league average
        #tm1 and tm0 HOME
        tm1_stats = tm1[6].find_all('tr')[1].find('div').find_all('div')[0]
        tm2_stats = tm2[6].find_all('tr')[1].find('div').find_all('div')[0]
        self.dico_data['tm0_PPGH'].append(tm1_stats.find_all('tr')[1].find_all('font')[1].text)
        self.dico_data['tm1_wins'].append(tm1_stats.find_all('tr')[4].find_all('font')[0].text.replace('%','')) # % Wins 
        self.dico_data['tm2_wins'].append(tm2_stats.find_all('tr')[4].find_all('font')[0].text.replace('%',''))
        self.dico_data['tm0_wins'].append(tm1_stats.find_all('tr')[4].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_defeats'].append(tm1_stats.find_all('tr')[5].find_all('font')[0].text.replace('%','')) # % Defeats 
        self.dico_data['tm2_defeats'].append(tm2_stats.find_all('tr')[5].find_all('font')[0].text.replace('%',''))
        self.dico_data['tm0_defeats'].append(tm1_stats.find_all('tr')[5].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_GSG'].append(tm1_stats.find_all('tr')[7].find_all('font')[0].text) # Goals scored per game
        self.dico_data['tm2_GSG'].append(tm2_stats.find_all('tr')[7].find_all('font')[0].text)
        self.dico_data['tm0_GSG'].append(tm1_stats.find_all('tr')[7].find_all('font')[1].text)
        self.dico_data['tm1_GCG'].append(tm1_stats.find_all('tr')[9].find_all('font')[0].text) # Goals conceded per game
        self.dico_data['tm2_GCG'].append(tm2_stats.find_all('tr')[9].find_all('font')[0].text)
        self.dico_data['tm0_GCG'].append(tm1_stats.find_all('tr')[9].find_all('font')[1].text)
        self.dico_data['tm1_D'].append(tm1_stats.find_all('tr')[11].find_all('font')[0].text.replace('%','')) # % Draws
        self.dico_data['tm2_D'].append(tm2_stats.find_all('tr')[11].find_all('font')[0].text.replace('%',''))
        self.dico_data['tm0_D'].append(tm1_stats.find_all('tr')[11].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_TGG'].append(tm1_stats.find_all('tr')[13].find_all('font')[0].text) # Total goals per game
        self.dico_data['tm2_TGG'].append(tm2_stats.find_all('tr')[13].find_all('font')[0].text)
        self.dico_data['tm0_TGG'].append(tm1_stats.find_all('tr')[13].find_all('font')[1].text)
        self.dico_data['tm1_25'].append(tm1_stats.find_all('tr')[15].find_all('font')[0].text.replace('%','')) # % matches over 2.5 goals
        self.dico_data['tm2_25'].append(tm2_stats.find_all('tr')[15].find_all('font')[0].text.replace('%',''))
        self.dico_data['tm0_25'].append(tm1_stats.find_all('tr')[15].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_35'].append(tm1_stats.find_all('tr')[17].find_all('font')[0].text.replace('%','')) # % matches over 3.5 goals
        self.dico_data['tm2_35'].append(tm2_stats.find_all('tr')[17].find_all('font')[0].text.replace('%',''))
        self.dico_data['tm0_35'].append(tm1_stats.find_all('tr')[17].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_BTS'].append(tm1_stats.find_all('tr')[19].find_all('font')[0].text.replace('%','')) # % matches where both teams scored
        self.dico_data['tm2_BTS'].append(tm2_stats.find_all('tr')[19].find_all('font')[0].text.replace('%',''))
        self.dico_data['tm0_BTS'].append(tm1_stats.find_all('tr')[19].find_all('font')[1].text.replace('%',''))
        
        #tm1 and tm0 HOME
        tm1_stats = tm1[6].find_all('tr')[1].find('div').find_all('div')[1]
        # tm1_PPGH'].append(tm1_stats.find_all('tr')[1].find_all('font')[0].text # Points per game
        self.dico_data['tm0_PPGH_h'].append(tm1_stats.find_all('tr')[1].find_all('font')[1].text)
        self.dico_data['tm1_wins_h'].append(tm1_stats.find_all('tr')[4].find_all('font')[0].text.replace('%','')) # % Wins 
        self.dico_data['tm0_wins_h'].append(tm1_stats.find_all('tr')[4].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_defeats_h'].append(tm1_stats.find_all('tr')[5].find_all('font')[0].text.replace('%','')) # % Defeats 
        self.dico_data['tm0_defeats_h'].append(tm1_stats.find_all('tr')[5].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_GSG_h'].append(tm1_stats.find_all('tr')[7].find_all('font')[0].text) # Goals scored per game
        self.dico_data['tm0_GSG_h'].append(tm1_stats.find_all('tr')[7].find_all('font')[1].text)
        self.dico_data['tm1_GCG_h'].append(tm1_stats.find_all('tr')[9].find_all('font')[0].text) # Goals conceded per game
        self.dico_data['tm0_GCG_h'].append(tm1_stats.find_all('tr')[9].find_all('font')[1].text)
        self.dico_data['tm1_D_h'].append(tm1_stats.find_all('tr')[11].find_all('font')[0].text.replace('%','')) # % Draws
        self.dico_data['tm0_D_h'].append(tm1_stats.find_all('tr')[11].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_TGG_h'].append(tm1_stats.find_all('tr')[13].find_all('font')[0].text) # Total goals per game
        self.dico_data['tm0_TGG_h'].append(tm1_stats.find_all('tr')[13].find_all('font')[1].text)
        self.dico_data['tm1_25_h'].append(tm1_stats.find_all('tr')[15].find_all('font')[0].text.replace('%','')) # % matches over 2.5 goals
        self.dico_data['tm0_25_h'].append(tm1_stats.find_all('tr')[15].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_35_h'].append(tm1_stats.find_all('tr')[17].find_all('font')[0].text.replace('%','')) # % matches over 3.5 goals
        self.dico_data['tm0_35_h'].append(tm1_stats.find_all('tr')[17].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm1_BTS_h'].append(tm1_stats.find_all('tr')[19].find_all('font')[0].text.replace('%','')) # % matches where both teams scored
        self.dico_data['tm0_BTS_h'].append(tm1_stats.find_all('tr')[19].find_all('font')[1].text.replace('%',''))
        
        #tm2 and tm0 AWAY
        tm2_stats = tm2[6].find_all('tr')[1].find('div').find_all('div')[2]
        # tm1_PPGH'].append(tm1_stats.find_all('tr')[1].find_all('font')[0].text # Points per game
        self.dico_data['tm0_PPGH_a'].append(tm2_stats.find_all('tr')[1].find_all('font')[1].text)
        self.dico_data['tm2_wins_a'].append(tm2_stats.find_all('tr')[4].find_all('font')[0].text.replace('%','')) # % Wins 
        self.dico_data['tm0_wins_a'].append(tm2_stats.find_all('tr')[4].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm2_defeats_a'].append(tm2_stats.find_all('tr')[5].find_all('font')[0].text.replace('%','')) # % Defeats 
        self.dico_data['tm0_defeats_a'].append(tm2_stats.find_all('tr')[5].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm2_GSG_a'].append(tm2_stats.find_all('tr')[7].find_all('font')[0].text) # Goals scored per game
        self.dico_data['tm0_GSG_a'].append(tm2_stats.find_all('tr')[7].find_all('font')[1].text)
        self.dico_data['tm2_GCG_a'].append(tm2_stats.find_all('tr')[9].find_all('font')[0].text) # Goals conceded per game
        self.dico_data['tm0_GCG_a'].append(tm2_stats.find_all('tr')[9].find_all('font')[1].text)
        self.dico_data['tm2_D_a'].append(tm2_stats.find_all('tr')[11].find_all('font')[0].text.replace('%','')) # % Draws
        self.dico_data['tm0_D_a'].append(tm2_stats.find_all('tr')[11].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm2_TGG_a'].append(tm2_stats.find_all('tr')[13].find_all('font')[0].text) # Total goals per game
        self.dico_data['tm0_TGG_a'].append(tm2_stats.find_all('tr')[13].find_all('font')[1].text)
        self.dico_data['tm2_25_a'].append(tm2_stats.find_all('tr')[15].find_all('font')[0].text.replace('%','')) # % matches over 2.5 goals
        self.dico_data['tm0_25_a'].append(tm2_stats.find_all('tr')[15].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm2_35_a'].append(tm2_stats.find_all('tr')[17].find_all('font')[0].text.replace('%','')) # % matches over 3.5 goals
        self.dico_data['tm0_35_a'].append(tm2_stats.find_all('tr')[17].find_all('font')[1].text.replace('%',''))
        self.dico_data['tm2_BTS_a'].append(tm2_stats.find_all('tr')[19].find_all('font')[0].text.replace('%','')) # % matches where both teams scored
        self.dico_data['tm0_BTS_a'].append(tm2_stats.find_all('tr')[19].find_all('font')[1].text.replace('%',''))
    
    def save_datas(self):
        print('Saving csv file')
        root_folder = path.dirname(path.dirname(__file__))
        data_folder = path.join(root_folder, 'data')
        df = pd.DataFrame(self.dico_data)
        df.to_csv(path.join(data_folder, f'{self.league}.csv'), index=False)
    
    def fetching_datas(self):
        print('Scrapping !')
        for i,url in enumerate(self.urls):
            try:
                self.scrape_data_from_url(url)
            except:
                self.remove_matche(i)
                print(f'!!!pb with url : {url}!!!')
                
    def remove_matche(self, i):
        self.dico_data['url'].pop(i)
        self.dico_data['score'].pop(i)
        self.dico_data['date'].pop(i)
        
    #------------------------------------------------
    # MAIN
    #------------------------------------------------
    def scrape(self):
        # step 1 : initialize dico data
        self.init_dico_data()
        
        # step 2 : get all matches urls
        self.scrape_url_matches_by_year()
        
        # step 3 : fill dico data
        self.fetching_datas()

        # step 4 : saving datas
        self.save_datas()
        
        
if __name__ == '__main__':
    param_set = [
            dict(
                league = 'france_2019',
                months = [f'month{i}' for i in range(1,13)]
                # months = ['month1']
            ),
    ]
    
    for params in param_set : 

        scrapp = scraper(**params)
        scrapp.scrape()
    print('Finito cappuccino!')