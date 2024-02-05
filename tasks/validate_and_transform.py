import datetime
import pandas as pd
from typing import List
from csv import DictReader
from models import Bronze, Silver
from pydantic import ValidationError

def get_csv(fname: str) -> List[dict]:
    """
        Read CSV file and return dict
    """
    with open(fname, 'r') as f:
        r = DictReader(f)
        return list(r)

def sanitize_data(data: List[dict]) -> pd.DataFrame:
    """
        Sanitize bronze data to generate silver data
    """
    df = pd.DataFrame(data)

    ## Make sure there are no relative links
    df['url'] = df['url'].map(lambda x: f'https://old.reddit.com{x}' if x[0] == '/' else x)
    df['self_url'] = df['self_url'].map(lambda x: f'https://old.reddit.com{x}' if x[0] == '/' else x)
    df['user_link'] = df['user_link'].map(lambda x: f'https://old.reddit.com{x}' if x[0] == '/' else x)

    ## Trim URL to 500 characters
    df['url'] = df['url'].str.slice(stop=500)

    ## Update timestamp format to '%Y-%m-%d %H:%M:%S'
    df['create_timestamp'] = df['create_date'].map(lambda x: datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S'))
    df['create_date'] = df['create_timestamp'].map(lambda x: x.split(' ')[0])
    df['create_time'] = df['create_timestamp'].map(lambda x: x.split(' ')[1])

    ## Update upvotes for posts younger than 2 hours and convert to int
    df['upvotes'] = df['upvotes'].map(lambda x: x if x[0].isdigit() else '-1')
    df['upvotes'] = df['upvotes'].astype('int')

    ## Add column for 'post_type' (Text, Media, Link)
    df['post_type'] = df['url'].map(lambda x: 'Media' if 'reddit.com/gallery' in x or 'i.redd.it' in x or 'v.redd.it' in x else ('Text' if 'reddit.com' in x else 'Link'))

    ## Add Upvote Classification
    df['upvote_range'] = df['upvotes'].map(lambda x: 'Hidden' if x==-1 else ('High' if x>=700 else ('Medium' if x>=100 else 'Low')))

    ## Add Time Classification
    df['created_at'] = df['create_time'].map(lambda x: 'Night' if int(x.split(':')[0]) >= 22 and int(x.split(':')[0]) < 5 else ('Morning' if int(x.split(':')[0]) >= 5 and int(x.split(':')[0]) < 12 else ('Day' if int(x.split(':')[0]) >= 12 and int(x.split(':')[0]) <= 18 else 'Evening')))

    return df[['title','url','self_url','domain','flair','create_timestamp','user','user_link','comments','upvotes','post_type','create_date','create_time','created_at','upvote_range']]

if __name__ == "__main__":
    ## Read Bronze Data
    bronze_path = '/tmp/bronze.csv'
    bronze_raw_data = get_csv(bronze_path)

    ## Validate schema as defined in the Pydantic model
    _ = [Bronze.model_validate(o) for o in bronze_raw_data]

    ## Create and validate Silver Data
    silver_df = sanitize_data(bronze_raw_data)
    silver_raw_data = silver_df.to_dict('records')
    _ = [Silver.model_validate(o) for o in silver_raw_data]
    silver_df.to_csv('/tmp/silver.csv', index=False)
