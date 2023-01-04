import requests
#requests를 다운받고 불러옴
from bs4 import BeautifulSoup
#beautifulsoup4를 다운받고 불러옴

LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():

  result = requests.get(INDEED_URL)
  #requests라는 package를 이용해서 해당 url의 html을 가져옴
  #result는 해당 url의 html을 불러온 것
  #print(result.text)로 html의 text를 불러올 수 있음

  soup = BeautifulSoup(result.text, "html.parser")
  #beautifulsoup4라는 package안의 BeautifulSoup라는 함수를 이용해서 해당 url의 html의 text를 추출할 수 있음
  #soup는 해당 url의 html data를 추출한 것임

  pagination = soup.find("div", {"class":"pagination"})
  #해당 사이트의 코드를 통해서 페이지 관련 코드 찾을 수 있고 find라는 함수를 통해 해당 <div>를 추출해낼 수 있음
  #pagination은 페이지 관련 <div>를 추출해낸 변수임

  links = pagination.find_all("a")
  #find_all 함수는 리스트로 값을 내보냄 
  #links는 각 <div> 안에 있는 <a>(anchor)를 추출한 리스트가 있는 변수임
  #links는 list로 되어있음


  pages = []
  for link in links[:-1]:
  #spans의 마지막 부분(next page)을 없애줌
    pages.append(int(link.find("span").string))
    #links라는 리스트에 있는 각 <a>(링크) span을 찾아 pages라는 새로운 리스트에 넣어줌
    #string만 골라오고(= text만 가져옴) 이를 integer로 바꿈


  max_page = pages[-1]
  return max_page


def extract_job(html):
  jobtitle = html.find("h2", {"class":"jobTitle"})
  real_job = jobtitle.find("span",title=True).string
  # real_job = jobtitle.find("span")["title"]을 쓰지 못함. class=jobTitle 하위에 span이라는 tag가 두개 존재하기 때문임. 따라서 두 span 중 title이라는 이름을 가진 tag를 추출해야함.

  company = html.find("span", {"class":"companyName"}).string

  location = html.find("div",{"class":"companyLocation"}).get_text()
  # pre라는 tag 하위항목에 span과 div가 존재하는데 여기서는 div를 추출해야 하므로 html.select_one("pre>div")를 사용함

  job_id = html.parent["data-jk"]
  # 여기서 html 상에 'data-jk'의 data가 없기 때문에 부모tag에서 찾아줘야함

  
  return {"title": real_job, "company": company, "location": location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}
  #return구문 사용시 두가지 이상 출력 시 dictionary 처럼 {}와 :을 사용함


def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed page: {page}")
    result = requests.get(f"{INDEED_URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"slider_container"})
    # 여기서 results 값을 가장 큰 범위로 해놓는 것이 좋음.
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs
    
