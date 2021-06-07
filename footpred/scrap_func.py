import re
import pandas as pd
from requests import get
from bs4 import BeautifulSoup

def scrape_data_from_url(url):
    #Init dico data
    dico_data = {}

    #request + soup
    soup = BeautifulSoup(get(url).text, "html.parser")

    #---------- Home and away records
    scores = soup.find_all(text=re.compile('Home and away records'))
    divs = [score.parent.parent.parent.parent for score in scores]

    tm1_records = divs[0].find_all('tr')
    dico_data['tm1_points_h'] = tm1_records[2].find_all('td')[2].text.replace('%','') #home points in %
    dico_data['tm1_PPGH_h'] = tm1_records[4].find_all("td")[1].text #  Points Per Game at Home
    dico_data['tm1_GS_h'] = tm1_records[7].find_all('td')[2].text.replace('%','') # goals score in %
    dico_data['tm1_GC_h'] = tm1_records[8].find_all('td')[2].text.replace('%','') # goals conceded in %
    dico_data['tm0_GS_h'] = tm1_records[9].find_all('td')[2].text.replace('%','')#  League average (% goals)

    tm2_records = divs[1].find_all('tr')
    dico_data['tm2_points_a'] = tm2_records[2].find_all('td')[4].text.replace('%','') #home points in %
    dico_data['tm2_PPGA_a'] = tm2_records[5].find_all("td")[1].text  # Points Per Game away
    dico_data['tm2_GS_a'] = tm2_records[7].find_all('td')[4].text.replace('%','') # goals score in %
    dico_data['tm2_GC_a'] = tm2_records[8].find_all('td')[4].text.replace('%','') # goals conceded in %
    dico_data['tm0_GS_a'] = tm2_records[9].find_all('td')[4].text.replace('%','')#  League average (% goals)

    #---------- stats against league average
    scores = soup.find_all(text=re.compile('stats against league average'))
    divs = [score.parent.parent.parent.parent for score in scores]

    tm1_stats = divs[0].find_all('tr')[1].find('div').find_all('div')[0]
    tm2_stats = divs[1].find_all('tr')[1].find('div').find_all('div')[0]

    dico_data['tm0_PPGH'] = tm1_stats.find_all('tr')[1].find_all('font')[1].text
    dico_data['tm1_wins'] = tm1_stats.find_all('tr')[4].find_all('font')[0].text.replace('%','') # % Wins 
    dico_data['tm2_wins'] = tm2_stats.find_all('tr')[4].find_all('font')[0].text.replace('%','')
    dico_data['tm0_wins'] = tm1_stats.find_all('tr')[4].find_all('font')[1].text.replace('%','')
    dico_data['tm1_defeats'] = tm1_stats.find_all('tr')[5].find_all('font')[0].text.replace('%','') # % Defeats 
    dico_data['tm2_defeats'] = tm2_stats.find_all('tr')[5].find_all('font')[0].text.replace('%','')
    dico_data['tm0_defeats'] = tm1_stats.find_all('tr')[5].find_all('font')[1].text.replace('%','')
    dico_data['tm1_GSG'] = tm1_stats.find_all('tr')[7].find_all('font')[0].text # Goals scored per game
    dico_data['tm2_GSG'] = tm2_stats.find_all('tr')[7].find_all('font')[0].text
    dico_data['tm0_GSG'] = tm1_stats.find_all('tr')[7].find_all('font')[1].text
    dico_data['tm1_GCG'] = tm1_stats.find_all('tr')[9].find_all('font')[0].text # Goals conceded per game
    dico_data['tm2_GCG'] = tm2_stats.find_all('tr')[9].find_all('font')[0].text
    dico_data['tm0_GCG'] = tm1_stats.find_all('tr')[9].find_all('font')[1].text
    dico_data['tm1_D'] = tm1_stats.find_all('tr')[11].find_all('font')[0].text.replace('%','') # % Draws
    dico_data['tm2_D'] = tm2_stats.find_all('tr')[11].find_all('font')[0].text.replace('%','')
    dico_data['tm0_D'] = tm1_stats.find_all('tr')[11].find_all('font')[1].text.replace('%','')
    dico_data['tm1_TGG'] = tm1_stats.find_all('tr')[13].find_all('font')[0].text # Total goals per game
    dico_data['tm2_TGG'] = tm2_stats.find_all('tr')[13].find_all('font')[0].text
    dico_data['tm0_TGG'] = tm1_stats.find_all('tr')[13].find_all('font')[1].text
    dico_data['tm1_25'] = tm1_stats.find_all('tr')[15].find_all('font')[0].text.replace('%','') # % matches over 2.5 goals
    dico_data['tm2_25'] = tm2_stats.find_all('tr')[15].find_all('font')[0].text.replace('%','')
    dico_data['tm0_25'] = tm1_stats.find_all('tr')[15].find_all('font')[1].text.replace('%','')
    dico_data['tm1_35'] = tm1_stats.find_all('tr')[17].find_all('font')[0].text.replace('%','') # % matches over 3.5 goals
    dico_data['tm2_35'] = tm2_stats.find_all('tr')[17].find_all('font')[0].text.replace('%','')
    dico_data['tm0_35'] = tm1_stats.find_all('tr')[17].find_all('font')[1].text.replace('%','')
    dico_data['tm1_BTS'] = tm1_stats.find_all('tr')[19].find_all('font')[0].text.replace('%','') # % matches where both teams scored
    dico_data['tm2_BTS'] = tm2_stats.find_all('tr')[19].find_all('font')[0].text.replace('%','')
    dico_data['tm0_BTS'] = tm1_stats.find_all('tr')[19].find_all('font')[1].text.replace('%','')

    #tm1 and tm0 HOME
    tm1_stats = divs[0].find_all('tr')[1].find('div').find_all('div')[1]
    # tm1_PPGH'] = tm1_stats.find_all('tr')[1].find_all('font')[0].text # Points per game
    dico_data['tm0_PPGH_h'] = tm1_stats.find_all('tr')[1].find_all('font')[1].text
    dico_data['tm1_wins_h'] = tm1_stats.find_all('tr')[4].find_all('font')[0].text.replace('%','') # % Wins 
    dico_data['tm0_wins_h'] = tm1_stats.find_all('tr')[4].find_all('font')[1].text.replace('%','')
    dico_data['tm1_defeats_h'] = tm1_stats.find_all('tr')[5].find_all('font')[0].text.replace('%','') # % Defeats 
    dico_data['tm0_defeats_h'] = tm1_stats.find_all('tr')[5].find_all('font')[1].text.replace('%','')
    dico_data['tm1_GSG_h'] = tm1_stats.find_all('tr')[7].find_all('font')[0].text # Goals scored per game
    dico_data['tm0_GSG_h'] = tm1_stats.find_all('tr')[7].find_all('font')[1].text
    dico_data['tm1_GCG_h'] = tm1_stats.find_all('tr')[9].find_all('font')[0].text # Goals conceded per game
    dico_data['tm0_GCG_h'] = tm1_stats.find_all('tr')[9].find_all('font')[1].text
    dico_data['tm1_D_h'] = tm1_stats.find_all('tr')[11].find_all('font')[0].text.replace('%','') # % Draws
    dico_data['tm0_D_h'] = tm1_stats.find_all('tr')[11].find_all('font')[1].text.replace('%','')
    dico_data['tm1_TGG_h'] = tm1_stats.find_all('tr')[13].find_all('font')[0].text # Total goals per game
    dico_data['tm0_TGG_h'] = tm1_stats.find_all('tr')[13].find_all('font')[1].text
    dico_data['tm1_25_h'] = tm1_stats.find_all('tr')[15].find_all('font')[0].text.replace('%','') # % matches over 2.5 goals
    dico_data['tm0_25_h'] = tm1_stats.find_all('tr')[15].find_all('font')[1].text.replace('%','')
    dico_data['tm1_35_h'] = tm1_stats.find_all('tr')[17].find_all('font')[0].text.replace('%','') # % matches over 3.5 goals
    dico_data['tm0_35_h'] = tm1_stats.find_all('tr')[17].find_all('font')[1].text.replace('%','')
    dico_data['tm1_BTS_h'] = tm1_stats.find_all('tr')[19].find_all('font')[0].text.replace('%','') # % matches where both teams scored
    dico_data['tm0_BTS_h'] = tm1_stats.find_all('tr')[19].find_all('font')[1].text.replace('%','')

    #tm2 and tm0 AWAY
    tm2_stats = divs[1].find_all('tr')[1].find('div').find_all('div')[2]
    # tm1_PPGH'] = tm1_stats.find_all('tr')[1].find_all('font')[0].text # Points per game
    dico_data['tm0_PPGH_a'] = tm2_stats.find_all('tr')[1].find_all('font')[1].text
    dico_data['tm2_wins_a'] = tm2_stats.find_all('tr')[4].find_all('font')[0].text.replace('%','') # % Wins 
    dico_data['tm0_wins_a'] = tm2_stats.find_all('tr')[4].find_all('font')[1].text.replace('%','')
    dico_data['tm2_defeats_a'] = tm2_stats.find_all('tr')[5].find_all('font')[0].text.replace('%','') # % Defeats 
    dico_data['tm0_defeats_a'] = tm2_stats.find_all('tr')[5].find_all('font')[1].text.replace('%','')
    dico_data['tm2_GSG_a'] = tm2_stats.find_all('tr')[7].find_all('font')[0].text # Goals scored per game
    dico_data['tm0_GSG_a'] = tm2_stats.find_all('tr')[7].find_all('font')[1].text
    dico_data['tm2_GCG_a'] = tm2_stats.find_all('tr')[9].find_all('font')[0].text # Goals conceded per game
    dico_data['tm0_GCG_a'] = tm2_stats.find_all('tr')[9].find_all('font')[1].text
    dico_data['tm2_D_a'] = tm2_stats.find_all('tr')[11].find_all('font')[0].text.replace('%','') # % Draws
    dico_data['tm0_D_a'] = tm2_stats.find_all('tr')[11].find_all('font')[1].text.replace('%','')
    dico_data['tm2_TGG_a'] = tm2_stats.find_all('tr')[13].find_all('font')[0].text # Total goals per game
    dico_data['tm0_TGG_a'] = tm2_stats.find_all('tr')[13].find_all('font')[1].text
    dico_data['tm2_25_a'] = tm2_stats.find_all('tr')[15].find_all('font')[0].text.replace('%','') # % matches over 2.5 goals
    dico_data['tm0_25_a'] = tm2_stats.find_all('tr')[15].find_all('font')[1].text.replace('%','')
    dico_data['tm2_35_a'] = tm2_stats.find_all('tr')[17].find_all('font')[0].text.replace('%','') # % matches over 3.5 goals
    dico_data['tm0_35_a'] = tm2_stats.find_all('tr')[17].find_all('font')[1].text.replace('%','')
    dico_data['tm2_BTS_a'] = tm2_stats.find_all('tr')[19].find_all('font')[0].text.replace('%','') # % matches where both teams scored
    dico_data['tm0_BTS_a'] = tm2_stats.find_all('tr')[19].find_all('font')[1].text.replace('%','')

    #------------ Scoring patterns
    scores = soup.find_all(text=re.compile('Scoring patterns'))
    divs = [score.parent.parent.parent.parent for score in scores]

    tm1_patterns = divs[0].find_all('tr')
    dico_data['tm1_ClS_h'] = tm1_patterns[2].find_all('td')[1].text.replace('%','') # Clean sheets
    dico_data['tm1_WtN_h'] = tm1_patterns[3].find_all('td')[1].text.replace('%','') # Won-to-nil
    dico_data['tm1_SiBH_h'] = tm1_patterns[4].find_all('td')[1].text.replace('%','') # Scored in both halves
    dico_data['tm1_BoTS_h'] = tm1_patterns[5].find_all('td')[1].text.replace('%','') # Both teams scored
    dico_data['tm1_FtS_h'] = tm1_patterns[6].find_all('td')[1].text.replace('%','') # Failed to score
    dico_data['tm1_LtN_h'] = tm1_patterns[7].find_all('td')[1].text.replace('%','') # Lost-to-nil
    dico_data['tm1_CiBH_h'] = tm1_patterns[8].find_all('td')[1].text.replace('%','') # Conceded in both halves

    tm2_patterns = divs[1].find_all('tr')
    dico_data['tm2_ClS_a'] = tm2_patterns[2].find_all('td')[2].text.replace('%','') # Clean sheets
    dico_data['tm2_WtN_a'] = tm2_patterns[3].find_all('td')[2].text.replace('%','') # Won-to-nil
    dico_data['tm2_SiBH_a'] = tm2_patterns[4].find_all('td')[2].text.replace('%','') # Scored in both halves
    dico_data['tm2_BoTS_a'] = tm2_patterns[5].find_all('td')[2].text.replace('%','') # Both teams scored
    dico_data['tm2_FtS_a'] = tm2_patterns[6].find_all('td')[2].text.replace('%','') # Failed to score
    dico_data['tm2_LtN_a'] = tm2_patterns[7].find_all('td')[2].text.replace('%','') # Lost-to-nil
    dico_data['tm2_CiBH_a'] = tm2_patterns[8].find_all('td')[2].text.replace('%','') # Conceded in both halves

    return dico_data