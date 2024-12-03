
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/generate-file")
async def generate_and_return_file():

    ###################################### ----------- A.P.I ----------- ######################################

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": -20.8255,
        "longitude": -40.6207,
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation",
                "surface_pressure", "cloud_cover", "wind_speed_10m", 
                "wind_direction_10m", "shortwave_radiation"
                ] ,
        "wind_speed_unit": "ms",
        "timezone": "America/Sao_Paulo",
        "models": "best_match"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(3).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(6).ValuesAsNumpy()
    hourly_shortwave_radiation = hourly.Variables(7).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
    	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True).tz_convert("America/Sao_Paulo"),
    	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True).tz_convert("America/Sao_Paulo"),
    	freq = pd.Timedelta(seconds = hourly.Interval()),
    	inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["shortwave_radiation"] = hourly_shortwave_radiation

    hourly_dataframe = pd.DataFrame(data = hourly_data)

    ###################################### ----------- C.O.N.V.E.R.S.O.R ----------- ######################################

    def xlsx_to_sam(xlsx_file, sam_file):
        # Ler o arquivo XLSX (assumindo que as colunas são Data, Hora, Temperatura, Umidade, Pressão, etc.)
        df = pd.read_excel(xlsx_file)
        df.columns = df.columns.str.strip()
        df['date'] = df['date'].astype(str)


        # Cria novas 3 colunas para de ano, Mês e Dia (separa a coluna "time" em 3)
        df['YR'] = df['date'].str.slice(2, 4)    # Últimos dois dígitos do ano
        df['MO'] = df['date'].str.slice(5, 7)    # Mês
        df['DA'] = df['date'].str.slice(8, 10)   # Dia
        df['HR'] = df['date'].str.slice(11, 13)  # Hora
        df = df.drop(columns=['date'])

        # Abrir o arquivo SAM para escrita
        with open(sam_file, 'w') as sam:

            sam.write("~    1 ANCHIETA               ES  -3  S20 48  W040 36    10\n")
            sam.write(f"{'~'}{'YR':<2} {'MO':<2} {'DA':<2} {'HR':<2} {'I':<4} {'1':<4} {'2':<2} {'3':<7} {'4':<7} {'5':<7} {'6':<4} {'7':<3} {'8':<4} {'9':<5} {'10':<2} {'11':<6} {'12':<5} {'13':<5} {'14':<6} {'15':<6} {'16':<9} {'17':<4} {'18':<6} {'19':<4} {'20':<8} {'21'}\n")
            
            for index, row in df.iterrows():

                sam.write(f"{''} {row['YR']:<2} {row['MO']:<2} {row['DA']:<2} {row['HR']:<2} {'0 9999 9999':<12} {row['shortwave_radiation']:<4} {'?0 9999 ?0 9999 ?0'} {row['cloud_cover']:<4} {row['cloud_cover']:<3} {row['temperature_2m']} {'9999.'} {row['relative_humidity_2m']} {row['surface_pressure']} {row['wind_direction_10m']:<5} {row['wind_speed_10m']:<5} 99999. 999999 999999999 9999 99999. 9999 999      0\n")

    # Salvar o DataFrame como arquivo Excel
    hourly_dataframe['date'] = hourly_dataframe['date'].dt.tz_localize(None)
    excel_file = 'arquivo.xlsx'
    hourly_dataframe.to_excel(excel_file, index=False, engine='openpyxl',float_format='%.1f')


    # Criar a pasta de saída, se não existir
    output_folder = 'arquivos'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Definir o nome do arquivo SAM
    sam_file = os.path.join(output_folder, 'dados_meteorologicos.sam')

    # Chamar a função de conversão
    xlsx_to_sam(excel_file, sam_file)

    return FileResponse(
        sam_file,           
        media_type= "application/octet-stream",
        filename= "dados_meteorologicos.sam"
    )

