from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PriceToUSDPipeline:

    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## check is price present
        if adapter.get('price'):

            #converting the price to a float
            floatPrice = float(adapter['price'])

            #converting the price from gbp to usd using our hard coded exchange rate
            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item

        else:
            # drop item if no price
            raise DropItem(f"Missing price in {item}")

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item
        
import mysql.connector

import mysql.connector

class SavingToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='0619248',
            database='chocolate_scraping'
        )
        self.curr = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Check if the table exists, and if not, create it
        self.curr.execute("""
        CREATE TABLE IF NOT EXISTS chocolate_products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            price VARCHAR(50),
            url VARCHAR(2083)
        )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            print(f"Processing item: {item}")
            self.curr.execute("""INSERT INTO chocolate_products (name, price, url) VALUES (%s, %s, %s)""", (
                item['name'],
                item['price'],
                item['url']
            ))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error saving item: {e}")
        return item

    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()
