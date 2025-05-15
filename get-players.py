from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import players
import pandas as pd

def get_top_scoring_players(max_results=50):
    """
    Retrieves the top scoring NBA players for the current season and displays them
    alphabetically, along with their points per game.

    Args:
        max_results (int, optional): The maximum number of players to retrieve.
            Defaults to 50.
    """
    try:
        # Get the league leaders in points
        leaders = leagueleaders.LeagueLeaders(stat_category_abbreviation='PTS', season='2024-25')
        leaders_data = leaders.get_dict()['resultSets'][0]['rowSet']
        leaders_columns = leaders.get_dict()['resultSets'][0]['headers']
        leaders_df = pd.DataFrame(leaders_data, columns=leaders_columns)

        # Print the columns of the DataFrame to inspect available data
        print("Columns in leaders_df:", leaders_df.columns)

        # Get the player information (including full names)
        nba_players = players.get_players()
        nba_players_df = pd.DataFrame(nba_players)

        # Create a dictionary to map player IDs to full names for efficient lookup
        player_id_to_name = {player['id']: player['full_name'] for player in nba_players}

        # Add player names to the leaders DataFrame
        leaders_df['Player_Name'] = leaders_df['PLAYER_ID'].map(player_id_to_name)

        # Select relevant columns and calculate PPG
        if 'PTS' in leaders_df.columns and 'GP' in leaders_df.columns:
            leaders_df['PPG'] = leaders_df['PTS'] / leaders_df['GP']
            top_scorers_df = leaders_df[['Player_Name', 'PPG']]
            top_scorers_df = top_scorers_df.rename(columns={'PPG': 'Points Per Game'})
            sort_column = 'Points Per Game'
        elif 'PTS' in leaders_df.columns:
            top_scorers_df = leaders_df[['Player_Name', 'PTS']]
            top_scorers_df = top_scorers_df.rename(columns={'PTS': 'Total Points'})
            sort_column = 'Total Points'
        else:
            print("Could not find 'PTS' or 'GP' columns in the leaders data.")
            return

        # Sort the DataFrame alphabetically by player name
        alphabetical_scorers = top_scorers_df.sort_values(by='Player_Name')

        # Limit the number of results
        alphabetical_scorers = alphabetical_scorers.head(max_results)

        # Print the results
        print(f"\nTop Scoring NBA Players (Alphabetical Order - {sort_column}):")
        for index, row in alphabetical_scorers.iterrows():
            print(f"{row['Player_Name']}: {sort_column} - {row[sort_column]:.1f}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_top_scoring_players()