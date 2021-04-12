import sys
from os import path
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from footpred.scrap_func import scrape_data_from_url

BASE_URL = "https://www.soccerstats.com/"

class scraper():

    def __init__(self, **kwargs):
        self.league = kwargs.get("league", 'france_2020')
        self.months = kwargs.get("months", ['month8'])
        self.df = pd.DataFrame()
    #------------------------------------------------
    # Fetching URLS
    #------------------------------------------------
    def scrape_matches_by_month(self, month):
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

        #Infos table of matches
        scores = table.find_all(text=re.compile('\xa0'))
        tm1_names = [name.replace('\xa0','')  for name in scores if name.endswith('\xa0')]
        tm2_names = [name.replace('\xa0','')  for name in scores if name.startswith('\xa0')]
        urls = [matche['href'] for matche in table.find_all('a', class_= "vsmall")]
        scores =  table.find_all(text=re.compile(' - '))
        dates =  [date.text for date in table.find_all('font', color = "green")]
        
        print(f'Found {len(urls)} matches !')
        
        for i,url in enumerate(urls):
            print(f'Scraping {url}')
            dico_data = {}
            
            #try: #try to scrap the datas from the url
            dico_data = scrape_data_from_url(BASE_URL + url) 
            dico_data['scores'] = scores[i]
            dico_data['tm1_names'] = tm1_names[i]
            dico_data['tm2_names'] = tm2_names[i]
            dico_data['urls'] = urls[i]
            dico_data['scores'] = scores[i]
            dico_data['dates'] = dates[i]
            if self.df.empty :
                self.df = pd.DataFrame.from_dict(dico_data,  orient='index').T
                print('coucou')
            else :
                dfm = pd.DataFrame.from_dict(dico_data,  orient='index').T
                self.df = pd.concat([self.df, dfm], ignore_index=True)
            print(self.df)
            # except:
                # print(f'!!!pb with url : {url}!!!')


    def scrape_url_matches_by_year(self):
        print(f"Searching {self.league}")
        self.urls = []
        for month in self.months:
            self.scrape_matches_by_month(month)

    
    def save_datas(self):
        print('Saving csv file')
        root_folder = path.dirname(path.dirname(__file__))
        data_folder = path.join(root_folder, 'data')
        self.df.to_csv(path.join(data_folder, f'{self.league}.csv'), index=False)
        
    #------------------------------------------------
    # MAIN
    #------------------------------------------------
    def scrape(self):

        # step 1 : scrapping all matches urls
        self.scrape_url_matches_by_year()

        # step 2 : saving datas
        self.save_datas()
        
        
if __name__ == '__main__':
    param_set = [
            # dict(
            #     league = 'france_2019',
            #     months = [f'month{i}' for i in range(1,13)]
            # ),
            dict(
                league = 'france',
                # months = [f'month{i}' for i in range(1,4)]
                months = ['month1']
            ),
    ]
    
    for params in param_set : 
        scrapp = scraper(**params)
        scrapp.scrape()
    print('Finito cappuccino!')