import subprocess
import sys

def install_prerequisites():
    """Installs the necessary Python libraries if they are not already installed."""
    required_libraries = ['nba_api', 'pandas']
    installed_libraries = [pkg.split('==')[0] for pkg in subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode().split()]

    for library in required_libraries:
        if library not in installed_libraries:
            print(f"Installing {library}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
                print(f"{library} installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error installing {library}: {e}")
                sys.exit(1)
        else:
            print(f"{library} is already installed.")

def get_nba_standings():
    """Fetches and displays the current NBA standings in alphabetical order."""
    from nba_api.stats.endpoints import leaguestandings
    from nba_api.stats.static import teams
    import pandas as pd

    try:
        # Get the current league standings
        standings = leaguestandings.LeagueStandings()
        standings_data = standings.get_dict()['resultSets'][0]['rowSet']
        standings_columns = standings.get_dict()['resultSets'][0]['headers']
        standings_df = pd.DataFrame(standings_data, columns=standings_columns)

        # Get the list of NBA teams to merge with standings for full names
        nba_teams = teams.get_teams()
        nba_teams_df = pd.DataFrame(nba_teams)

        # Merge the standings data with the team names using the correct column names
        merged_df = pd.merge(standings_df, nba_teams_df, left_on='TeamID', right_on='id')

        # Select and display the team name, wins, and losses
        wins_losses_df = merged_df[['full_name', 'WINS', 'LOSSES']]

        # Sort alphabetically by team name
        alphabetical_wins_losses = wins_losses_df.sort_values(by='full_name')

        print("\nCurrent NBA Standings (Alphabetical Order):")
        for index, row in alphabetical_wins_losses.iterrows():
            print(f"{row['full_name']}: Wins - {row['WINS']}, Losses - {row['LOSSES']}")

    except ImportError as e:
        print(f"Error importing necessary libraries: {e}. Please ensure 'nba_api' and 'pandas' are installed.")
        print("You can try running the script again to install them.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while fetching or processing standings: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Checking and installing prerequisites...")
    install_prerequisites()
    print("\nFetching and displaying NBA standings...")
    get_nba_standings()
    print("\nScript finished.")