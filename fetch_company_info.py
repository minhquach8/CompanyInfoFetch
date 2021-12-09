from bs4 import BeautifulSoup
import requests
import csv, os

# Folder CSV to save all company's info csv files
# stock_exchanges includes three main VN stock exchanges
stock_exchanges = ["hose", "hnx", "upcom"]

# Check if CSV folder exists or not
if not os.path.exists(path):
    os.makedirs(path)

# Function: Read stocks from file text
def read_stocks_text_file(namefile):
    """
    Read stocks from a text file, remove end-line breaks, convert them into a list
    """
    file = open(f".\stocktickers\{namefile}.txt", "r")
    content = file.read()
    stocks_list = content.split(", ")
    file.close()
    return stocks_list


# Function: Get company info
def fetch_company_info(ticker):
    url = f"https://www.stockbiz.vn/Stocks/{ticker}/Snapshot.aspx"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # Get category
    category = doc.find("div", {"class": "industry"}).a.text
    # Get company brief info
    info = doc.find("div", {"class": "text_content"}).text
    # Get company address
    addr = doc.find("td", {"valign": "top"}).b.next_sibling
    # Get company link
    link = doc.find_all("td", {"class": "right"})[2].a.text
    return [
        ticker,
        category.strip(),
        info.strip(),
        addr.strip(),
        link.strip(),
    ]


# Function: Create a csv file
def create_company_info_csv(namefile):
    csv_file = open(
        f".\CSV\{namefile}_companies.csv",
        "w",
        encoding="utf-8",
        newline="",
    )
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Ticker", "Category", "Info", "Address", "Link"])

    se_list = read_stocks_text_file(namefile)
    for stock in se_list:
        result = fetch_company_info(stock)
        csv_writer.writerow(result)
    csv_file.close()


# Main function
def main():
    for stock_exchange in stock_exchanges:
        create_company_info_csv(stock_exchange)

main()
