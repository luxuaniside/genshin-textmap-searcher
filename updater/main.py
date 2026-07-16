from downloader import update_repository
from data_loader import upload_data
from parse_data import combine_textmap

def main():
    # Update the repository to get the latest data
    update_repository()

    # Load the data from the repository and upload it to Supabase
    data = combine_textmap()  # Implement this function to load your data
    upload_data(data)

if __name__ == "__main__":
    main()