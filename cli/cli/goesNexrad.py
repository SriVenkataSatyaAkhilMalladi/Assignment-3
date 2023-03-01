import typer
import requests
import os


app = typer.Typer()


base_url =' http://ec2-44-211-9-40.compute-1.amazonaws.com:8070/'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyX2ZyZWUiLCJleHAiOjE2Nzg4Nzg5NzF9.nf3xgoIkWBEvega60fBa88IzWNIKUHtI7f6mC5aDMi0'
headers = {"Authorization": f"Bearer {token}"}
@app.command()
def create_user(
        username: str = typer.Option(..., prompt=True),
        password: str = typer.Option(..., prompt=True),
        plan: str = typer.Option(..., prompt=True)
):
    """
    Create a new user.
    """
    url = base_url + 'register'
    data = {
        "username" : username,
        "password": password,
        "plan": plan
    }
    response = requests.post(url, json=data)
    typer.echo("Successfully registered")

@app.command()
def downloadByFileName(filename: str):
    """
    Download a file by name.
    """
    json_file_name = {"filename":filename}

    if filename.endswith('.nc'):
        url = base_url + 'filename_url_gen_goes'
    else:
        url = base_url + 'filename_url_gen_nexrad'
    response = requests.get(url,params=json_file_name,headers=headers)  
    data = response.json()
  
    typer.echo(data['url'])

@app.command()
def fetchGoes(bucket: str = typer.Option(..., prompt=True),
    year_geos: int = typer.Option(..., prompt=True),
    day_of_year_geos: int = typer.Option(..., prompt=True),
    hour_of_day: str = typer.Option(..., prompt=True),):
    """
    List all files in a bucket with the given prefix.
    """
   

   
    url = base_url + 'list_goes_files_as_dropdown'
    prefix = 'ABI-L1b-RadC/{}/{}/{}/'.format(year_geos,day_of_year_geos,hour_of_day)


    response = requests.get(url,params={"bucket":bucket,"prefix":prefix},headers=headers).json()
    typer.echo(response)


@app.command()
def fetchNexrad(bucket: str = typer.Option(..., prompt=True),
    year_nexrad: int = typer.Option(..., prompt=True),
    month_of_year_nexrad: str = typer.Option(..., prompt=True),
    day_of_month_nexrad: str = typer.Option(..., prompt=True),
    selected_stationcode:str = typer.Option(..., prompt=True),):
    """
    List all files in a bucket with the given prefix.
    """
   


    url = base_url +'list_nexrad_files_as_dropdown'
    prefix = '{}/{}/{}/{}/'.format(year_nexrad,month_of_year_nexrad,day_of_month_nexrad,selected_stationcode)

    response = requests.get(url,params={"bucket_name":bucket,"prefix":prefix},headers=headers).json()
    typer.echo(response)


@app.command()
def fetchCoordinates():
    """
    List all coordinates of the nexrad sattelited locations.
    """

    url = base_url + 'coordinatesdata'
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url,headers=headers)
    typer.echo(response.text)
