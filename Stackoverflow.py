import requests
from bs4 import BeautifulSoup


def sof_last_page():
  result = requests.get("https://stackoverflow.com/jobs?q=python&sort=i")
  soup = BeautifulSoup(result.text,"html.parser")
  pagination = soup.find("div", {"class":"s-pagination"}) 

  links = pagination.find_all("a")

  pages=[]
  for link in links[:-1]:
    pages.append(int(link.find("span").string))

  last_page = pages[-1] + 1
  
  return last_page


def extract_jobs(html):

  title = html.find("a",{"class":"s-link"})
  real_title = title["title"]

  company, location = html.find("h3",{"class":"mb4"}).find_all("span",recursive=False)
  # recursive=False는 tag안에 있는 모든 tag를 가져오지 않고 바로 하위 tag들(직계자손들)만 추출함
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)

  # name_loc = html.find("h3",{"class":"fc-black-700 fs-body1 mb4"})
  # if name_loc:
  # # name_loc이 None일 수도 있기 때문에 if에 name_loc이라는 조건 붙이기 가능함
  #   real_name_loc = name_loc.get_text(strip=True)
  #   # soup.get_text(strip=True) 구문 쓸 수 있음
  # else:
  #   real_name_loc = None

  link = html["data-preview-url"]
  
  return {"title":real_title, "company":company, "location":location, "links": f"https://stackoverflow.com{link}"}



def sof_extract_jobs(last_page):
  jobs = []
  for page in range(1,last_page):
    print(f"Scrapping StackOverflow page: {page}")
    result = requests.get(f"https://stackoverflow.com/jobs?q=python&sort=i&pg={page}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div", {"class":"-job"})
    for result in results:
      job = extract_jobs(result)
      jobs.append(job)
  return jobs
  