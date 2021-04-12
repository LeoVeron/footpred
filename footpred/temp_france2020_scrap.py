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