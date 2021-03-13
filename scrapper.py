import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    main_page = requests.get(url)
    soup = BeautifulSoup(main_page.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    pages = pagination.find_all("a")
    last_page = pages[-2].find("span").string
    return int(last_page)


def extract_job(html):
    title = html.find("h2").find("a").string
    company, location = html.find("h3").find_all(
        "span", recursive=False)  # recursive span속 span을 가져오지 않음
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    link = html["data-jobid"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://stackoverflow.com/jobs/{link}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping so page {page+1}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "js-result"})
        for result in results:
            jobs.append(extract_job(result))

    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
