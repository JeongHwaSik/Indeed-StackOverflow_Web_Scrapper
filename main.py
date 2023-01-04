from indeed import extract_indeed_pages, extract_indeed_jobs
from Stackoverflow import sof_last_page, sof_extract_jobs 
from save import save_to_file

last_sof_page = sof_last_page()
last_indeed_page = extract_indeed_pages()

indeed_jobs = extract_indeed_jobs(last_indeed_page)
extract_jobs = sof_extract_jobs(last_sof_page)

jobs = indeed_jobs + extract_jobs

save_to_file(jobs)
    























