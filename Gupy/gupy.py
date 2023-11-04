import requests
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass
import pandas as pd
from time import sleep


@dataclass
class Infos:
    job_name: str
    company_name: str
    job_url: str
    date: str

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"}
job_names = ['estagio', 'c#', '.net', 'pessoa', 'software', 'estagiario']
#job_names = ['estagio']

search_date = '04/10/2023'


def get_infos(job) -> Infos:
    date = job.get("publishedDate").split("T")[0].split("-")
    date = f"{date[2]}/{date[1]}/{date[0]}"
    return Infos(
        job_name=job.get("name"),
        company_name=job.get("careerPageName"),
        job_url=job.get("jobUrl"),
        date=date,
    )


def search_jobs_infos(job_name: str):
    max_pages = 1
    limit = 50
    offset = 0
    for i in range(0, max_pages):
        dic_jobs = {'job_name': [], 'company_name': [], 'job_url': [], 'date': []}
        print(i)
        url = 'https://portal.api.gupy.io/api/v1/jobs?jobName={' + job_name + '}&limit=' + str(
            limit) + '&offset=' + str(
            offset) + '&workplaceType=remote'
        print(url)
        sleep(5)
        site = requests.get(url, headers=headers)
        soup = BeautifulSoup(site.content, 'html.parser')
        site_json = json.loads(soup.text)

        jobs = site_json.get('data')

        for job in jobs:
            info = get_infos(job)
            # if info.date == search_date:
            dic_jobs['job_name'].append(info.job_name)
            dic_jobs['company_name'].append(info.company_name)
            dic_jobs['job_url'].append(info.job_url)
            dic_jobs['date'].append(info.date)

            df = pd.DataFrame(dic_jobs)
            df.to_csv(f'{job_name}.csv', encoding='utf-8', sep=';')
        offset += limit


for i in range(0, len(job_names)):
    search_jobs_infos(job_names[i])
