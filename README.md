# charting_the_boom

This repository is a python script that connects to the city of Austin's public, open-source data API and downloads and compiles data to produce a up-to-date chart showing the amount of new housing supply vs demand in PNG format. This script takes advantage of the Socrata API's ability to use simple SQL-like queries in the request to greatly expedite the process, as well as make the downloaded data significantly easier to handle than working with the entire 1.5GB data set. This script was built to go along with my [Austin Housing](https://nathaniel-j.github.io/Austin-Building-Boom/) project, so that I could automate the process of tracking my predictions made in that project. The chart below was produced by this code on 12/21/2021 (winter solstice!).


![chart](chart.png)

The original intent for this project was to build this as an AWS Lambda script to be run in the cloud as an automated process and have the chart saved in an AWS S3 bucket to be statically hosted, however, the libraries I used made the script file too large to be held or used with Lambas. So, for now I am running this script locally, on a weekly basis to generate an updated chart, and then uploading the updated chart to an AWS S3 storage bucket for static hosting. The result is still not ideal, but it gets the tracking started and it can be viewed [here](https://hellositeworld.s3.us-east-2.amazonaws.com/index.html).

Ideally my final product would be an entirely cloud-based set of scripts that automatically run on a scheduled basis and update this chart (and potentially others as well) to serve as a new housing supply gap dashboard. 


requirements for this code:
- pandas
- sodapy
- seaborn
- matplotlib
- python 3.8+ 
