# Bibliometrics Project with MongoDB, Scrapy, and Dash

This project includes a Docker-compose configuration to run a stack comprising MongoDB, a scraping script with Scrapy, and an interactive dashboard with Dash.

The goal of this project is to extract data from a website and display it interactively on a dashboard.

## Data Blocks Displayed on the Dashboard
- Number of books in each category: Displays the total number of books in each category.

- Average rating for each category: Displays a list of books with more than 10 copies available, showing their title, category, price, and rating.

- List of books with more than 10 available :
Affiche une liste des livres pour lesquels plus de 10 exemplaires sont disponibles, avec leur titre, leur catégorie, leur prix et leur note.

- Random Book Generator : Randomly generated book.

- List of books with a 5 stars rating :
Displays a list of books that have received a 5-star rating, showing their title, category, and rating.

- 10 best priced books with 5 stars rating :
Displays the 10 best-priced books with 5 stars.

- Books count per rating :
Percentage of books based on their ratings.

- Search in title :
Search bar for looking up a book by its title.

## Service Configuration

### MongoDB

The MongoDB service is used as a database to store the data extracted by the scraping script.

- Exposed Port : `27017`

### Scrapping

The scraping service uses Scrapy to extract data from the website "https://books.toscrape.com/" and store it in MongoDB.

### Dash

The Dash service hosts an interactive dashboard for visualizing and analyzing the extracted data.

- Exposed Port : `8050`

## Usage

1. Ensure Docker and Docker-compose are installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Run the following command from the project root to start the services:

   ```bash
   docker compose up --build
5. View the application at: "http://localhost:8050/"

