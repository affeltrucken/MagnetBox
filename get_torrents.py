from py1337x import py1337x
from colorama import Fore

# Seed threshold values
PERFECT_SEEDS = 500
HIGH_SEEDS = 100
MEDIUM_SEEDS = 25
LOW_SEEDS = 10
BAD_SEEDS = 3
DEAD_SEEDS = 0

# Initialize py1337x client
PY1337X = py1337x(proxy='1337x.to', cache='py1337xCache', cacheTime=500)

def get_torrents(search_term, max_size_gb):
    """Fetch torrents for a search term and filter by size."""
    search_results = PY1337X.search(search_term, page=1, sortBy='seeders', category="Movies")
    torrents = search_results["items"]
    return [torrent for torrent in torrents if filter_torrent_by_size(torrent, max_size_gb)]

def filter_torrent_by_size(torrent, max_size_gb):
    """Filter torrents by size."""
    size, prefix = torrent["size"].split()
    size = float(size.replace(",", ""))

    return prefix == "GB" and size <= max_size_gb

def pprint_torrent(torrent, seeder_color, index=""):
    """Pretty print torrent details."""
    seeders = int(torrent["seeders"])
    size = torrent["size"]
    name = format_name(torrent["name"])

    print(Fore.RESET)
    print(f"{Fore.WHITE}{index} {name}")
    print(f" {seeder_color} ↪ {seeders} seeders")
    print(f" {Fore.BLUE} ↪ {torrent['language']}")
    print(f" {Fore.CYAN} ↪ {size}") 
    print(Fore.RESET)
    print(torrent["magnetLink"])

def format_name(name):
    """Format torrent name with color coding and splitting if needed."""
    middle = len(name) // 2
    if len(name) > 40:
        name = f"{name[:middle]}\n {name[middle:].strip()}"
    
    # Color code resolution labels
    if "1080p" in name:
        name = f"{Fore.MAGENTA}1080p{Fore.WHITE} {name}"
    elif "720p" in name:
        name = f"{Fore.LIGHTMAGENTA_EX}720p{Fore.WHITE} {name}"
    elif "480p" in name:
        name = f"{Fore.LIGHTCYAN_EX}480p{Fore.WHITE} {name}"
    
    return name

def get_torrent_info(torrent):
    """Fetch detailed info of a torrent."""
    return PY1337X.info(torrentId=torrent["torrentId"])
