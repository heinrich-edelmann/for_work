from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from datetime import datetime


app = FastAPI()
@app.get("/")
def root():
    return {"Wilkommen!": "thats a dedicated server to the fans of japanese content"}


Wikipedia_URL = "https://en.wikipedia.org/wiki/List_of_best-selling_manga"
website = requests.get(Wikipedia_URL)
result = BeautifulSoup(website.content, "html.parser")
manga_table= result.find('table',{'class':"wikitable sortable"})
df=pd.read_html(str(manga_table))
# convert list to dataframe
df0=pd.DataFrame(df[0])

one_piece = df0.loc[0].to_dict()
dragon_ball = df0.loc[1].to_dict()
golgo_13 = df0.loc[2].to_dict()
detective_conan = df0.loc[3].to_dict()
doraemon = df0.loc[4].to_dict()
naruto = df0.loc[5].to_dict()
slam_dunk = df0.loc[6].to_dict()
kochiKame = df0.loc[7].to_dict()
demon_slayer = df0.loc[8].to_dict()
crayon = df0.loc[9].to_dict()
oishinbo = df0.loc[10].to_dict()
bleach = df0.loc[11].to_dict()
jojo = df0.loc[12].to_dict()
attack_on_titan = df0.loc[13].to_dict()
astro_boy = df0.loc[14].to_dict()
fist_of_north_star = df0.loc[15].to_dict()
hajime = df0.loc[16].to_dict()
kindaichi_case_files = df0.loc[17].to_dict()
touch = df0.loc[18].to_dict()

mangas_list = [one_piece,dragon_ball,golgo_13, detective_conan,doraemon, naruto, slam_dunk, kochiKame, demon_slayer, crayon, oishinbo,bleach,
jojo,attack_on_titan,astro_boy, fist_of_north_star, hajime, kindaichi_case_files,touch]

@app.get("/mangas")
async def all_mangas():
    return mangas_list

@app.get("/mangas/{manga_name}")
async def get_manga_informations(manga_name):
    for m in mangas_list:
        if m["Manga series"] == manga_name:
            return m

class Manga(BaseModel):
    Manga_series: str
    Author: str
    Publisher: str
    Demographic: str
    No_of_collected_volumes: int
    Serialized: str
    Approximate_sales: str
    Average_sales_per_volume: str

#put
@app.put("/mangas/{manga_name}")
async def put_manga(Manga_series: str, manga: Manga):
    update_encoded = jsonable_encoder(manga)
    mangas_list = update_encoded
    return mangas_list

#delete
@app.delete("/mangas/{manga_name}", status_code=200)
async def delete_manga(Manga_series: str) -> None:
    mangas_list.remove(mangas_list[Manga_series])
    return mangas_list


#background task
def write_notification(message: str):
    with open("log.txt", mode="w") as message_file:
        content = f"This manga was added: {message} at this time: {datetime.now()}"
        message_file.write(content)
        
#post
@app.post("/mangas", status_code=201)
async def add_newmanga(new_manga: Manga, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, message=new_manga)
    print("Post Logged")
    mangas_list.append(new_manga)
    return(mangas_list)