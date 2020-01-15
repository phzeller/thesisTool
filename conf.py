from csv import writer
from io import StringIO

#   Configure the DMCA dataset directory below
######################################################
main_directory = "/Users/philippzeller/GitHub/dmca"  #
######################################################

# Do not touch those variables
no_of_notices = 0
output_csv = StringIO()
output_fileName = "output_final.csv"
output_file = None
csv_writer = writer(output_csv)


def create_csv_file():
    global output_csv
    # Define header of output file
    header_data = ["notice_id", "file_link", "year", "month", "day", "header", "notice", "description", "github_url", "no_of_github_URLs", "other_urls", "no_of_other_URLs", "github_user"]

    csv_writer.writerow(header_data)

def write_to_csv_file(noticeObj):
    global no_of_notices
    new_mined_list = noticeObj.mined_list
    new_mined_list.insert(0, no_of_notices)
    csv_writer.writerow(new_mined_list)
    no_of_notices += 1


def save_csv_file():
    output_file.write(output_csv.getvalue())