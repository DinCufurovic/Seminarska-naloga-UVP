import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

results = []
ratings_arr = []
dosezki_arr = []

def find_opponents_and_results(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Poišče vse igre
    games = soup.find_all('a', class_='master-games-clickable-link master-games-td-user')

    for game in games:
        # Informacije o nasprotniku
        nasprotnik_tagline = game.find_all('div', class_='master-games-user-tagline')[1]
        nasprotnik_ime = nasprotnik_tagline.find('span', class_='master-games-username').text.strip()
        nasprotnik_rating = nasprotnik_tagline.find('span', class_='master-games-user-rating').text.strip().strip('()')

        # Ekstrahiran rezultat iz <td>, ki vsebuje povezavo rezultata
        result_td = game.find_next('td', class_='master-games-text-center')
        if result_td:
            result_value = result_td.find('a', class_='master-games-clickable-link master-games-text-middle')
            if result_value:
                # Izvleči rezultat iz atributa naslova in besedilne vsebine
                result = result_value.get('title', '').strip() or result_value.text.strip()
            else:
                result = "/"
        else:
            result = "/"
        
        # Ugotovi, ali je Hikaru zmagal, izgubil ali izenačil
        if result == "1-0":
            izid = "Hikaru won"
        elif result == "0-1":
            izid = "Hikaru lost"
        elif result == "1/2-1/2":
            izid = "Draw"
        else:
            izid = "/"

        moves_td = game.find_next('td', class_='master-games-text-right')
        if moves_td:
            moves_value = moves_td.find('a', class_='master-games-clickable-link master-games-text-middle')
            if moves_value:
                moves = moves_value.get('title', '').strip() or moves_value.text.strip()
            else:
                moves = "/"
        else:
            moves = "/"

        opening_a = game.find_next('a', class_='master-games-content-stats master-games-opening')
        if opening_a:
            opening_moves = opening_a.get('title', '').strip()
            if opening_moves:
                opening_name = opening_a.find_all('span')[1].text.strip()
            else:
                opening_name = "/"
        else: opening_moves = "/"

        game_link_value = game.find_next('a', class_='master-games-date master-games-clickable-link master-games-text-middle')
        if game_link_value:
            game_link = game_link_value.get('href', '')
        else:
            game_link = "/"

        #print(f"Opponent: {nasprotnik_ime} - Moves: {moves} - Opening: {opening_name} ({opening_moves}) - (Rating: {nasprotnik_rating}) - Link = {game_link} - Result: {izid}")
        ratings_arr.append(int(nasprotnik_rating))

        results.append({
            'Nasprotnik': nasprotnik_ime,
            'Moves': moves,
            'Rating': nasprotnik_rating,
            'Rezultat': result,
            'Izid': izid,
            'Povezava':game_link
        })
        

# Tukaj gremo skozi prvih i strani
def Get_Data():
    for i in range(1, 6):
        # Ustrezen URL
        url = f"https://www.chess.com/games/search?fromSearchShort=1&p1=Hikaru%20Nakamura&playerId=291573"

        if i > 1:
            url += f"&page={i}"

        # Pošlji req
        response = requests.get(url)
        
        # In še preveri req
        if response.status_code == 200:
            find_opponents_and_results(response)


def Grafična_predstavitev(podatki):
    plt.figure(figsize=(12, 6))
    x = np.arange(len(podatki))
    plt.plot(x, podatki, marker='o', linestyle='-', color='royalblue', label='Opponent Ratings', markersize=8)

    plt.axhline(y=3213, color='crimson', linestyle='--', linewidth=2, label=f'Hikarujev Rating ({3213})')

    plt.xlabel('Game Number', fontsize=14, fontweight='bold')
    plt.ylabel('Rating', fontsize=14, fontweight='bold')
    plt.title('Ratingi nasprotnikov', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.tight_layout()
    plt.show()


def Table(data):
    df = pd.DataFrame(results, columns=['Nasprotnik', 'Povezava'])
    print(df)


def Dosezki():
    url = "https://www.chessfocus.com/tournament-history/hikaru-nakamura"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    gold_rows = soup.find_all('tr', class_='goldrow')

    for row in gold_rows:
        tournament_data = row.find('a')
        
        tournament_name = tournament_data.text.strip()
        
        dosezki_arr.append(tournament_name)
        

#Get_Data()
#Table(results)
#Grafična_predstavitev(ratings_arr)

