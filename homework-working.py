import requests
from datetime import datetime
import argparse
import csv

argParser = argparse.ArgumentParser()
argParser.add_argument("--user", help="Username", required=True)
argParser.add_argument("--password", help="Password", required=True)
argParser.add_argument("--job", help="Jenkins job", required=True)
argParser.add_argument("--start_date", type=lambda d: datetime.strptime(d, '%d.%m.%Y %H:%M'), help="Start Date in the format ddmmyyyy hh:mm")
argParser.add_argument("--end_date", type=lambda d: datetime.strptime(d, '%d.%m.%Y %H:%M'), help="End Date in the format ddmmyyyy hh:mm")
args = argParser.parse_args()



username = args.user
password = args.password
jenkins_host = "https://build.pyrsoftware.ca"
jenkins_job = args.job
end_date = args.end_date
start_date = args.start_date

request_url = "{0:s}/job/{1:s}/api/json{2:s}".format(
    jenkins_host,
    jenkins_job,
    "?tree=builds[fullDisplayName,number,timestamp,result,duration]"
)

job_data = requests.get(request_url , auth=(username, password)).json()

builds = []

for build in job_data["builds"]:
    build_date = datetime.fromtimestamp(build["timestamp"]/1000)
    if build_date > start_date and build_date < end_date:
        builds.append(build)


today = datetime.today()
d1 = today.strftime("%d.%m.%Y")
with open("jenkins-job-report-" + d1 + ".csv", 'w', newline = '') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(["Job name", "Build Number", "Status", "Duration(sec.)", "Date"])

    for build in builds:
        build_name = (build["fullDisplayName"])
        build_number = (build["number"])
        build_status = (build["result"])
        build_duration = (build["duration"]/60)

        writer.writerow([build_name, build_number, build_status, build_duration, build_date])

print("Report generated!")
