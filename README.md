
## PROBLEM STATEMENT
This project shows historical Airbnb price over the time, allowing travelers plan their trip wisely based on their budget, available time and selected city to visit.
For example you might not care much between visiting London or Paris or also between January or February, and having historical knowledge about average prices in cities and months can help you with your decision making process a lot.

## Data Source
Data is compiled from http://insideairbnb.com/get-the-data.html. More than 2300 csv files; calendar.csv and listings.csv files of 40 European cities  with data capacity of 230 GB are used for this project.

## Demo Link
https://www.datamaster.dev

## Tech Stack
![Tech Stack](https://github.com/tikaj/Best_Deal/blob/master/tech-stack.png)

*Airbnb data source*
http://insideairbnb.com/get-the-data.html

Setting up HTTPS
--- 

On EC2 Box:
---
$ pip3 install pyopenssl
$  openssl genrsa 2048 > private-key.pem
$  openssl req -new -key private-key.pem -out csr.pem

Purchased an SSL Certificate from NameCheap.
   - Used the csr.pem created above as the CSR code
   - Used HTTP DCV method for verification.
   - After verification, downloaded the actual certificate that is used 
     in the app.py 
 