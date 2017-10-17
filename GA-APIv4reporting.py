
# coding: utf-8

# In[2]:


from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import csv, time
import datetime

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
#Create a new Google Analytics API Project: https://console.developers.google.com/flows/enableapi?apiid=analytics
#Create a new Google Analytics API Project: https://www.youtube.com/watch?v=o50lrTq9DjQ
KEY_FILE_LOCATION = 'YOUR JSON CREDENTIALS FILE'
VIEW_ID = 'YOUR VIEW ID'

START_DATE = 'yesterday'
END_DATE = 'yesterday'
USERS = {
                        'reportRequests': [
                        {
                          'viewId': VIEW_ID,
                          'dateRanges': [{'startDate': START_DATE, 'endDate': END_DATE}],
                          'metrics': [{'expression': 'ga:sessions'},{'expression':'ga:users'}],
                          'dimensions': [{'name': 'ga:dateHourMinute'},{'name': 'ga:userType'},{'name': 'ga:userAgeBracket'},{'name': 'ga:userGender'}]
                        }]
                      }


# In[3]:


def initialize_analyticsreporting():
  """Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


# In[7]:


def get_report(analytics, report_config):
  """Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(body = report_config).execute()

def arrangedict(response):
  #Esta función toma el JSON devuelto por la API ya parseado a diccionario y lo loopea para reconstruirlo
  #con el formato adecuado para ser tomado por la librería que importamos para convertir diccionarios en csv.
  okarray = []
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dimensions = row.get('dimensions', [])
      metrics = row.get('metrics', [])[0].get('values',[])
      rowdict = {}
      for header, dimension in zip(dimensionHeaders, dimensions):
            rowdict[header] = dimension
      for header, metric in zip(metricHeaders, metrics):
            rowdict[header['name']] = metric
      okarray.append(rowdict)
  return okarray

def convert_to_csv(array, nombre):
    #crear y abrir cs nombre = report.name ()v
    #to do: cambiarle el nombre por la fecha + el nombre del reporte. El nombre del reporte no lo tenemos, hay que traerlo.
    nombre = report_config.name ()
    timestr = time.strftime("%Y%m%d_%H%M%S")
    nombreok = nombre + "_" + timestr  
    csv_file = open(nombreok, 'w+', encoding='utf-8')
    
    # crear objeto de escritura en el csv creado. método importado
    csvwriter = csv.writer(csv_file)
    
    count = 0
    for row in array:

          if count == 0:

                 header = row.keys()

                 csvwriter.writerow(header)

                 count += 1

          csvwriter.writerow(row.values())

    csv_file.close()

def main():

    analytics = initialize_analyticsreporting()
    
    #generar csv de usuarios
    user_data = get_report(analytics, USERS)
    convert_to_csv(arrangedict(user_data),'USERDATA')


# In[8]:


if __name__ == '__main__':
  main()