# Stevens Institute of Technology | Hanlon Lab
## Daily Stock Summary: Generating Daily Digest of Previous Day's Stock Performance

The aim of this project is to develop an automated script to send daily summary of previous day's stock performance over email.
This is intended for passive investors who would wan't to receive a daily digest of all the stocks they's invested in and their net profit.
There is a sentiment analysis component, which fetches trending news related to each stock, analyses weather it is positive or negative providing insights on how might the stock perform in future.

## APIs used:
1. Yahoo Finance
2. NewsAPI

## Modules Used:
1. json
2. pandas
3. time
4. datetime
5. newsapi
6. nltk

## Files
1. source.py: Primary Python3 script with all core functionality.
2. portfolio.json: JSON format file with details of all the stocks with purchase price.
3. meta_mail.txt: A meta file containing details of the recepient of the email, subject line and sendor.
4. send_mail.sh: A shell script to execute the source.py script.

## Cronjob
The following line is to be added in crontab to schedule daily execution at 7:00AM (12:00PM UTC).

0 12 * * * /usr/bin/sh /home/ubuntu/hanlon_project/send_mail.sh
