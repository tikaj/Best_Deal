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

TODO:
---
1- Table show correct caption (London, 2, 2).
2- months show as number
3- 0 defaults are stupid.
 