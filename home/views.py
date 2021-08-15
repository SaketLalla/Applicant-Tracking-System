from django.shortcuts import render , HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage

import requests
import json
import numpy as np
import pandas as pd
from pandas import json_normalize # easy JSON -> pd.DataFrame



# Create your views here.
def home(request):
    context={'name':'Saket Lalla'}
    return render(request , 'home.html' , context)
def compare(request):
    return render(request, 'compare.html')
def result(request):
    your_skills="C C++  JavaScript python matlab verilog vhdl databses mysql html css os linux windows librararies pandas numpy pyplot"
    
    content=request.GET['jobdescription']
    content_list=content.split()
    job_description=str()
    for i in content_list:
        job_description+=i + ' '

    auth_endpoint = "https://auth.emsicloud.com/connect/token" # auth endpoint

    client_id = "80cx9fihdo8aceqv" # replace 'your_client_id' with your client id from your api invite email
    client_secret = "EEWZrI1i" # replace 'your_client_secret' with your client secret from your api invite email
    scope = "emsi_open" # ok to leave as is, this is the scope we will used

    payload = "client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=client_credentials&scope=" + scope # set credentials and scope
    headers = {'content-type': 'application/x-www-form-urlencoded'} # headers for the response
    access_token = json.loads((requests.request("POST", auth_endpoint, data=payload, headers=headers)).text)['access_token'] 
    def extract_skills_list():
        all_skills_endpoint = "https://emsiservices.com/skills/versions/latest/skills" # List of all skills endpoint
        auth = "Authorization: Bearer " + access_token # Auth string including access token from above
        headers = {'authorization': auth} # headers
        response = requests.request("GET", all_skills_endpoint, headers=headers) # response
        response = response.json()['data'] # the data

        all_skills_df = pd.DataFrame(json_normalize(response)); # Where response is a JSON object drilled down to the level of 'data' key
        return all_skills_df

    #Extract skills from a text
    def extract_skills_from_document(job_description):
        skills_from_doc_endpoint = "https://emsiservices.com/skills/versions/latest/extract"
        text = job_description
        confidence_interval = str(0.5)
        payload = "{ \"text\": \"... " + text + " ...\", \"confidenceThreshold\": " + confidence_interval + " }"

        headers = {
            'authorization': "Bearer " + access_token,
            'content-type': "application/json"
            }

        response = requests.request("POST", skills_from_doc_endpoint, data=payload.encode('utf-8'), headers=headers)

        skills_found_in_document_df = pd.DataFrame(json_normalize(response.json()['data'])); # Where response is a JSON object drilled down to the level of 'data' key
                                                    
        return skills_found_in_document_df['skill.name'].tolist()
    
    jds_list=extract_skills_from_document(job_description) #jds means job description list
    ys_list = extract_skills_from_document(your_skills)
    
    common_skills=list((set(jds_list) & set(ys_list)))
    len_jds=len(jds_list)
    len_ys=len(ys_list)
    if(len_jds>len_ys):
        for i in range(len_jds-len_ys):
            ys_list.append(" ")
    elif(len_jds<len_ys):
        for i in range(len_ys-len_jds):
            jds_list.append(" ")

    df = pd.DataFrame(list(zip(ys_list, jds_list)), columns =['ys_list', 'jds_list'])
    data=[]
    for i in range(df.shape[0]):
        temp=df.loc[i]
        data.append(dict(temp))
    percent_match = (len(common_skills)/len_jds) *100
    match = round(percent_match , 2)


    
    context={'data':data , 'common_skills' : common_skills , 'match':match}
    return render(request , 'result.html', context )

def fullstack(request):
    return render(request , 'fullstack.html')
def developer(request):
    return render(request , 'developer.html')
def frontend(request):
    return render(request , 'frontend.html')
def backend(request):
    return render(request , 'backend.html')