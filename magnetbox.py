import get_torrents
import get_watchlist
import qbittorrentapi
from colorama import Fore
import os

SEPARATOR = "─" * 50

### CONFIGURATION ###
LETTERBOXD_USERNAME = "aldinsmajlovic"
MAX_TORRENT_SIZE_GB = 15.0

QBITTORRENT_HOST = "localhost"
QBITTORRENT_PORT = 8080
QBITTORRENT_USERNAME = "admin"
QBITTORRENT_PASSWORD = "password"
AUTHENTICATION_REQUIRED = False
TORRENT_CATEGORY_NAME = "MagnetBox"

TORRENT_SAVE_PATH = "D:/PLEX/MOVIES"
MAGNET_FILE = "saved_magnets.txt"
ALLOW_DUPLICATE_MAGNETS = False  # Set to True to add even if already saved
### END CONFIGURATION ###

def get_color(seeders):
    seeders = int(seeders)  # Ensure seeders is an integer
    if seeders >= 500:
        return Fore.GREEN
    if seeders >= 100:
        return Fore.LIGHTGREEN_EX
    if seeders >= 25:
        return Fore.YELLOW
    if seeders >= 10:
        return Fore.LIGHTRED_EX
    if seeders >= 3:
        return Fore.RED
    return Fore.LIGHTBLACK_EX


def yes_no_prompt(prompt: str) -> bool:
    """Prompts the user for a yes/no answer and returns a boolean value."""
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer.startswith("y"):
            return True
        elif answer.startswith("n"):
            return False

def load_saved_magnets() -> set:
    """Loads the saved magnet links from the file."""
    if not os.path.exists(MAGNET_FILE):
        return set()
    with open(MAGNET_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_magnets(magnets: list) -> None:
    """Saves new magnet links to the file."""
    with open(MAGNET_FILE, "a") as f:
        f.writelines(f"{magnet}\n" for magnet in magnets)

def add_torrents_to_qbit(magnet_links: list, movie_titles: list) -> None:
    """Adds the magnet links to qBittorrent."""
    qbt_client = qbittorrentapi.Client(
        host=QBITTORRENT_HOST, port=QBITTORRENT_PORT,
        username=QBITTORRENT_USERNAME, password=QBITTORRENT_PASSWORD
    )

    try:
        if AUTHENTICATION_REQUIRED:
            qbt_client.auth_log_in()
        print(Fore.GREEN + "Connected to qBittorrent!" + Fore.RESET)

        categories = qbt_client.torrent_categories.categories

        if TORRENT_CATEGORY_NAME not in categories:
            print(Fore.YELLOW + f"Category '{TORRENT_CATEGORY_NAME}' not found. Creating it..." + Fore.RESET)
            qbt_client.torrent_categories.createCategory(name=TORRENT_CATEGORY_NAME, save_path=TORRENT_SAVE_PATH)

        for link, movie in zip(magnet_links, movie_titles):
            response = qbt_client.torrents_add(urls=link, category=TORRENT_CATEGORY_NAME, save_path=TORRENT_SAVE_PATH)
            status_message = (
                f"{Fore.CYAN}Added torrent for {movie}{Fore.RESET}" 
                if response.lower() == "ok." 
                else f"{Fore.RED}Failed to add torrent for {movie}{Fore.RESET}"
            )
            print(status_message)

    except qbittorrentapi.LoginFailed as e:
        print(Fore.RED + f"Failed to connect to qBittorrent: {e}" + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Fore.RESET)

def main() -> None:
    """Main function that coordinates the process."""
    watchlist = get_watchlist.get_watchlist(LETTERBOXD_USERNAME)
    magnet_links, movie_titles, not_found_movies = [], [], []
    
    saved_magnets = load_saved_magnets()
    
    for movie in watchlist:
        torrents = get_torrents.get_torrents(movie, MAX_TORRENT_SIZE_GB)
        if not torrents:
            print(f"{Fore.RED}No torrents found for {movie}.{Fore.RESET}")
            not_found_movies.append(movie)
            continue
        
        first_torrent_info = get_torrents.get_torrent_info(torrents[0])
        print(movie)
        get_torrents.pprint_torrent(first_torrent_info, seeder_color=get_color(first_torrent_info["seeders"]))
        print(SEPARATOR)
        
        magnet_link = first_torrent_info["magnetLink"]
        if not ALLOW_DUPLICATE_MAGNETS and magnet_link in saved_magnets:
            print(f"{Fore.YELLOW}Skipping {movie} (already saved) in {MAGNET_FILE}.{Fore.RESET}")
            continue
        
        magnet_links.append(magnet_link)
        movie_titles.append(movie)
    
    print(f"Found {len(magnet_links)} torrents out of {len(watchlist)} movies.")
    
    if not magnet_links:
        print("No torrents found.")
        return

    if yes_no_prompt("Do you want to download them?"):
        add_torrents_to_qbit(magnet_links, movie_titles)
        save_magnets(magnet_links)
    else:
        print("Aborting.")

if __name__ == "__main__":
    main()
