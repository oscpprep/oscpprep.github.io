import requests, json, os, inspect
from datetime import datetime
from dateutil import relativedelta
from tqdm.auto import tqdm

tracking_list = []
print('if you want, program can access the token in current folder \n\t if it was saved with this name "zoom_access_token" exactly')
from_date = input("from which date? ...format {YYYY-MM-DD} exact>> ") # subject to change for each month moving behind
to_date = input("to which date? ...format {YYYY-MM-DD} exact>> ")
items_per_page = '300'
s = requests.Session()
access_token = input('input access token, \n or else if "zoom_access_token" file exists \n then press enter to continue\t')
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
def access_token_file(download_dir):
    for i in os.listdir(download_dir):
        if i == 'zoom_access_token':
            with open(os.path.join(currentdir, '')+i,'r') as f:
                access_token = f.readline()
                return access_token
    return False

if access_token == '':
    access_token = access_token_file(currentdir)

if access_token == False:
    print('access token was not set, quitting!')
    quit()

def days_difference(from_date_str,to_date_str):
    from_date = datetime.strptime(from_date_str,"%Y-%m-%d")
    to_date = datetime.strptime(to_date_str,"%Y-%m-%d")
    #difference_ = relativedelta.relativedelta(from_date, to_date)
    difference_in_days = (to_date - from_date).days
    f = lambda a: (abs(a)+a)/2
    difference_in_days = int(f(difference_in_days))
    zero_days_left = None
    if difference_in_days == 0:
        zero_days_left = True
    else:
        zero_days_left = False

    return (difference_in_days,zero_days_left)


def reset_date_to_one_month_behind(str_current_to_date):
    current_to_date = datetime.strptime(str_current_to_date,"%Y-%m-%d")
    new_to_date = current_to_date + relativedelta.relativedelta(months=-1)

    return datetime.strftime(new_to_date,"%Y-%m-%d")

meeting_topic_counter = 1
name = None
while True:

    url = f'https://api.zoom.us/v2/users/me/recordings?trash_type=meeting_recordings&to={to_date}&from={from_date}&mc=false&page_size={items_per_page}?'
    s.params['access_token'] = access_token
    r = s.get(url)
    response_in_dict = json.loads(r.text.encode('utf8'))
    # with open('dir.txt','w') as t:
    # t.write(json.dumps(response_in_dict,sort_keys=True, indent=4)) # to see in a heirchy
    direct_download_links = []

    # next_page_token = response_in_dict['next_page_token'] # next_page_token == "" True if no nextpage

    meeting_dict_list = [a_meeting for a_meeting in response_in_dict['meetings']]

    def downloader(file_name,link,s=s):
        response = s.get(link, stream=True,allow_redirects=True)
        with tqdm.wrapattr(open(file_name, "wb"), "write", miniters=1,total=int(response.headers.get('content-length', 0)),desc=file_name) as fout:
            for chunk in response.iter_content(chunk_size=4096):
                fout.write(chunk)


    for meeting_dict in meeting_dict_list:
        topic = meeting_dict['topic']
        topic = topic.translate(str.maketrans('','', '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'))
        recording_files_list = meeting_dict['recording_files'] # [MP4,M4A,TXT] DICTIONARY
        date_recorded = recording_files_list[0]['recording_start'].translate(str.maketrans('','', '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'))
        currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        name = os.path.join(currentdir, '')+topic+'_'+date_recorded
        tracking_list.append(name)
        print('current meeting/topic number: ',meeting_topic_counter,'ON TOPIC: ',topic)
        for recording in recording_files_list:
            direct_download_links.append(['.'+recording['file_type'].lower(),recording['download_url']])


        # [['.mp4', 'https://us02web.zoom.us/rec/download],....]
        # download_url


        mp4 = downloader(file_name=name+direct_download_links[0][0],link=direct_download_links[0][1])

        try:
            # [,['m4a',url],['txt',url]]
            downloader(file_name=name+direct_download_links[1][0],link=direct_download_links[1][1])
        except:
            pass

        try:
            # chat txt
            downloader(file_name=name+direct_download_links[2][0],link=direct_download_links[2][1])
        except:
            pass

        direct_download_links = []
        meeting_topic_counter += 1

    # calculations for next month
    difference_in_days , zero_days_left = days_difference(from_date,to_date)
    print('still trying get recordings for: days=', difference_in_days)
    # print(from_date == to_date, tracking_list.count(name) >= 4, zero_days_left)
    if from_date == to_date or tracking_list.count(name) >= 4 or zero_days_left:
        print('done download')
        break        

    else:
        new_to_date = reset_date_to_one_month_behind(to_date)
        # set/update from and to dates
        to_date = new_to_date
        print('resetting dates one month back from: ',to_date, 'continue until :',from_date)

