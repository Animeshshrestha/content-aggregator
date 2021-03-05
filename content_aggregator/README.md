# News Content Aggregator
This project aims to scraps the news from three different website and saves the news to the database. The user can get the news per according to his/her selection.


<u>Technologies Used</u>  
- Backend: Python, Django, Scrapy, Postgresql
- Frontend: HTML, Jquery, CSS

<u>Note: </u>
- This project provides API End point. We need to run the vue js server in next terminal. 

# Project Installation:
1. Setup the virtual environment
2. Clone the github repository into your terminal
3. Run the command
```bash
pip install -r requirements.txt
```
4. If you want to use sqlite3 as database then  run the command
```bash
python manage.py loaddata data.json
```
5. Make sure to change the database settings to 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
6. To run the scrapy run the bash file named job.sh with command. This command ensures that the latest news content is scrapped and saved to the database
```
./job.sh
```
7. To run the bash file periodically, we need to setup a cronjob. For e.g: To run the above bash file every 10 minutes:
```
* /5 * * * <path to bash file> >> <path to the file where to output the result> 2>&1
```
8. To 

```
**if you want to use sqlite3 as database**

# Admin Credentials
username: testuser  
password: admin123 \
email: testuser@test.com