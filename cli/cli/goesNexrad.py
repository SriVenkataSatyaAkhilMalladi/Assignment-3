import typer
import requests
import os


app = typer.Typer()


base_url ='http://localhost:8070/'
@app.command()
def create_user(
        username: str = typer.Option(..., prompt=True),
        email: str = typer.Option(..., prompt=True),
        password: str = typer.Option(..., prompt=True),
        plan: str = typer.Option(..., prompt=True)
):
    """
    Create a new user.
    """
    url = base_url + 'register'
    data = {
        "username" : username,
        "email": email,
        "password": password,
        "plan": plan
    }
    response = requests.post(url, json=data)
    typer.echo(response.text)

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
    response = requests.get(url,params=json_file_name)  
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


    response = requests.get(url,params={"bucket":bucket,"prefix":prefix}).json()
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

    response = requests.get(url,params={"bucket_name":bucket,"prefix":prefix}).json()
    typer.echo(response)


@app.command()
def fetchCoordinates():
    """
    List all coordinates of the nexrad sattelited locations.
    """

    url = base_url + 'coordinatesdata'
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjc3ODA2NzAwfQ.iY_cUl0EbvrFrbCdMiG6jsVKNe_iJznU1-kwagHX47Y'
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url,headers=headers)
    typer.echo(response.text)