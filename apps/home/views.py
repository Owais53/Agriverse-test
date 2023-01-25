# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
import os.path
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import scipy.ndimage as ndi
import requests
import pandas as pd
import numpy as np # linear algebra # data processing, CSV file I/O (e.g. pd.read_csv)
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
from django.shortcuts import render
from django.http import JsonResponse
from branca.element import Template, MacroElement
from django.views import View
import folium
from folium import raster_layers
from matplotlib.pyplot import imread
from matplotlib import  cm,colors
from collections import defaultdict
import matplotlib as mpl
import branca
import matplotlib.pyplot as plt
from osgeo import gdal,gdal_array,osr
import rasterio as rio
import re
import json
import js2py
import zipfile
import io
import numpy.ma as ma
import os
from zipfile import ZipFile, is_zipfile
from apps.authentication.models import Company



@login_required(login_url="/login/")
def index(request):
    selected_date = request.POST.get('dates',False)
    context = {'segment': 'index'}
    auth_url = "https://portal.irriwatch.com/oauth/v2/token"
    headers_auth = {
        "content-type": "application/x-www-form-urlencoded"
       
        } 
    body_auth = {"grant_type":"client_credentials","client_id":"ewzvs7nRh0FoiwnMkxd1MjkR8brOQSdz","client_secret":"r2TfYLayZR2F0PcesAVNNSbDrbRXDFknM98d6H2G75o8sec98NyxeBwTUwkTNzf4"}
    response_auth = requests.post(url=auth_url,headers=headers_auth,data=body_auth)
    response_auth_json = response_auth.json()
    token = response_auth_json['access_token']
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    url_company_orders = "https://api.irriwatch.com/api/v1/company/06db5883-48bd-4350-93e7-0e0ae69fe94c/order"
    response_orders = requests.get(url=url_company_orders,headers=headers).json()
    field_list = []
    field_efficiency_avg_10d_list = []
    field_3 =[]
    field_4 = []
    field_5 = []
    date_list = []
    field_data = []
    colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }
    
    if selected_date != False:
         url_field_data_3103 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = selected_date)
         url_field_data_3099 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = selected_date)
         url_field_data_3097 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = selected_date)
    else:
         url_field_data_3103 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = '20221224')
         url_field_data_3099 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = '20221224')
         url_field_data_3097 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = '20221224')
        
    response_field_3103 = requests.get(url=url_field_data_3103,headers=headers)
    response_field_3099 = requests.get(url=url_field_data_3099,headers=headers)
    response_field_3097 = requests.get(url=url_field_data_3097,headers=headers)
    field_3103 = response_field_3103.json()
    field_3099 = response_field_3099.json()
    field_3097 = response_field_3097.json()
    orders_list = ['3103','3103','3099','3097','3097']
    field_actual_crop_production_list = []
    field_actual_evapotranspiration_list = []
    field_soil_water_potential_root_zone_list = []
    precipitation_cumulative_list = []
    field_name_list = []
    soil_moisture_holding_capacity_list = []
    dates_list = []
    vegetation_cover_list = []
    soil_temperature_list = []
    date_list = []
    for i in field_3103:
      field_3103_vals = field_3103[i]
      field_data.append([field_3103_vals['name'],field_3103_vals['date'],field_3103_vals['vegetation_cover'],field_3103_vals['soil_temperature']])
      soil_moisture_holding_capacity_list.append(field_3103_vals['soil_moisture_holding_capacity'])
      dates_list.append(field_3103_vals['date'])
      precipitation_cumulative_list.append(field_3103_vals['precipitation_cumulative'])
      field_actual_crop_production_list.append(field_3103_vals['actual_crop_production'])
      field_actual_evapotranspiration_list.append(field_3103_vals['actual_evapotranspiration'])
      field_soil_water_potential_root_zone_list.append(field_3103_vals['soil_water_potential_root_zone'])
      field_name_list.append(field_3103_vals['name'])
      vegetation_cover_list.append(field_3103_vals['vegetation_cover'])
      soil_temperature_list.append(field_3103_vals['soil_temperature'])
      date_list.append(field_3103_vals['date'])
    for i in field_3099:
       field_3099_vals = field_3099[i]
       field_data.append([field_3099_vals['name'],field_3099_vals['date'],field_3099_vals['vegetation_cover'],field_3099_vals['soil_temperature']])
       field_actual_crop_production_list.append(field_3099_vals['actual_crop_production'])
       soil_moisture_holding_capacity_list.append(field_3099_vals['soil_moisture_holding_capacity'])
       dates_list.append(field_3099_vals['date'])
       field_actual_evapotranspiration_list.append(field_3099_vals['actual_evapotranspiration'])
       field_soil_water_potential_root_zone_list.append(field_3099_vals['soil_water_potential_root_zone'])
       field_name_list.append(field_3099_vals['name'])
       vegetation_cover_list.append(field_3099_vals['vegetation_cover'])
       soil_temperature_list.append(field_3099_vals['soil_temperature'])
       date_list.append(field_3099_vals['date'])
    for i in field_3097:
       field_3097_vals = field_3097[i]
       field_data.append([field_3097_vals['name'],field_3097_vals['date'],field_3097_vals['vegetation_cover'],field_3097_vals['soil_temperature']])
       field_actual_crop_production_list.append(field_3097_vals['actual_crop_production'])
       soil_moisture_holding_capacity_list.append(field_3097_vals['soil_moisture_holding_capacity'])
       dates_list.append(field_3097_vals['date'])
       field_actual_evapotranspiration_list.append(field_3097_vals['actual_evapotranspiration'])
       field_soil_water_potential_root_zone_list.append(field_3097_vals['soil_water_potential_root_zone'])
       field_name_list.append(field_3097_vals['name'])
       vegetation_cover_list.append(field_3097_vals['vegetation_cover'])
       soil_temperature_list.append(field_3097_vals['soil_temperature'])
       date_list.append(field_3097_vals['date'])
    df = pd.DataFrame({
                "fields_name": field_name_list,
                "actual_evapotranspiration": field_actual_evapotranspiration_list
            })
     # replace with your own data source
    fig = px.pie(df, values='actual_evapotranspiration', names='fields_name', hole=.3,height=300)
    fig.update_layout(
                title_text='Actual Evapotranspiration per fields',
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
               )
    
    plotly_plot_obj = plot({'data': fig}, output_type='div')
    fig2 = go.Figure(go.Surface(
                  contours = {
                    "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color":"black"},
                    "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05}
                    },
                  x = [1,2,3,4,5],
                  y = [1,2,3,4,5],
                  z = [
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1],
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1],
                    [0, 1, 0, 1, 0]
                    ]))
    fig2.update_layout(
                 scene = {
                    "xaxis": {"nticks": 28},
                    "zaxis": {"nticks": 2},
                    'camera_eye': {"x": 0, "y": -1, "z": 0.5},
                    "aspectratio": {"x": 1, "y": 1, "z": 0.2}
                    }, 
                               
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                height=300
               )
   
    df3 = pd.DataFrame({'field':field_name_list,'orders':orders_list,'crop_production':field_actual_crop_production_list}) 
    fig4 = px.bar(df3, x="field", y="crop_production", 
                 color="orders", barmode="group")
    fig4.update_layout(title_text='Crop Production per fields',width=1000,height=300,plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'])
    chart = fig4.to_html()
    data= {'Orders':orders_list,
       'Field': field_name_list,
     'Soil Water Potential Root Zone': field_soil_water_potential_root_zone_list      
     }
    df7 = pd.DataFrame(data)
    #df7['dates'] =pd.to_datetime(df7['dates'])
    freq='M'
    #df7=df7[['dates', 'types']].groupby([pd.Grouper(key='dates', freq = freq)]).agg('count').reset_index()
    #df7.loc['2022-12-23':'2022-12-25']
    line_plot = px.area(df7, x='Field', y='Soil Water Potential Root Zone',color='Orders',pattern_shape="Orders", pattern_shape_sequence=[".", "x", "+"],height=300,width=1000)
    line_plot.update_layout(
                title_text='Soil Water Potential Root Zone',
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
               )
    data1=[soil_temperature_list]
    fig9 = px.imshow(data1,
                labels=dict(x="Fields", y="Date", color="Soil Temprature"),
                x=field_name_list,
                y=['2022-12-24']
               )
    fig9.update_xaxes(side="top")
    fig9.update_layout(
                title_text='Soil Temprature',
                width=1000,
                height=300,
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
               )
      
    chart1 = plot({'data':fig9},output_type='div')
    charts = plot({'data':fig4},output_type='div')
    line_plot_obj = plot({'data':fig2},output_type='div')
    #line_plot_obj1 = plot({'data':fig1},output_type='div')
    line = plot({'data':line_plot},output_type='div')
    user_count = 0
    try:
      company = Company.objects.get(user=request.user)
      user_count = Company.objects.filter(user=request.user).count()
    except Company.DoesNotExist:
      company = 'Company'
    if company == 'Company':
      company_name = 'Company'
    else:      
      company_name  = company.company
    context = {'pie_plot': plotly_plot_obj,'line_plot':line_plot_obj,'company_name':company_name,'user_count':user_count,'bar':charts,'line':line,'field_data':field_data,'box':chart1}
    return render(request,'home/index.html',context=context)
    


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

def change_graphs(request):
    selected_date = request.POST.get('dates',False)
    selected_orders = request.POST.get('orders',False)
    token = get_oauth2_token()
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    colors = {
    'background': '#111111',
    'text': '#7FDBFF'
    }
    if selected_date != False and selected_orders == 'all':
         url_field_data_3103 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = selected_date)
         url_field_data_3099 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = selected_date)
         url_field_data_3097 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = selected_date)
    elif selected_orders == '6f32f9ce-5266-4d68-b6f1-b314e31a071f' and selected_date != False:
        url_field_data_3103 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = selected_date)
    elif selected_orders == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f' and selected_date != False:
        url_field_data_3099 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = selected_date)
    elif selected_orders == '6809fe46-5bfc-4c5c-8e90-b267c705be2e' and selected_date != False:
        url_field_data_3097 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = selected_date)
    else:
         url_field_data_3103 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = '20221224')
         url_field_data_3099 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = '20221224')
         url_field_data_3097 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = '20221224')
    orders_list = ['3103','3103','3099','3097','3097']
    field_actual_crop_production_list = []
    field_actual_evapotranspiration_list = []
    field_soil_water_potential_root_zone_list = []
    soil_moisture_holding_capacity_list = []
    soil_temprature_list = []
    field_name_list = []
    dates_list = []
    field_data = []
    field_3103 = False
    field_3099 = False
    field_3097 = False
    if selected_orders == 'all':
      orders_list = ['3103','3103','3099','3097','3097']
      response_field_3103 = requests.get(url=url_field_data_3103,headers=headers)
      response_field_3099 = requests.get(url=url_field_data_3099,headers=headers)
      response_field_3097 = requests.get(url=url_field_data_3097,headers=headers)
      field_3103 = response_field_3103.json()
      field_3099 = response_field_3099.json()
      field_3097 = response_field_3097.json()
    elif selected_orders == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
      orders_list = ['3103','3103']
      response_field_3103 = requests.get(url=url_field_data_3103,headers=headers)
      field_3103 = response_field_3103.json()
    elif selected_orders == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
      orders_list = ['3099']
      response_field_3099 = requests.get(url=url_field_data_3099,headers=headers)
      field_3099 = response_field_3099.json()
    elif selected_orders == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
      orders_list = ['3097','3097']
      response_field_3097 = requests.get(url=url_field_data_3097,headers=headers)
      field_3097 = response_field_3097.json()
    if field_3103 != False:
      for i in field_3103:
        field_3103_vals = field_3103[i]
        soil_temprature_list.append(field_3103_vals['soil_temperature'])
        soil_moisture_holding_capacity_list.append(field_3103_vals['soil_moisture_holding_capacity'])
        dates_list.append(field_3103_vals['date'])
        field_data.append([field_3103_vals['name'],field_3103_vals['date'],field_3103_vals['vegetation_cover'],field_3103_vals['soil_temperature']])
        field_actual_crop_production_list.append(field_3103_vals['actual_crop_production'])
        field_actual_evapotranspiration_list.append(field_3103_vals['actual_evapotranspiration'])
        field_soil_water_potential_root_zone_list.append(field_3103_vals['soil_water_potential_root_zone'])
        field_name_list.append(field_3103_vals['name'])
    if field_3099 != False:
      for i in field_3099:
       field_3099_vals = field_3099[i]
       soil_temprature_list.append(field_3099_vals['soil_temperature'])
       soil_moisture_holding_capacity_list.append(field_3099_vals['soil_moisture_holding_capacity'])
       dates_list.append(field_3099_vals['date'])
       field_data.append([field_3099_vals['name'],field_3099_vals['date'],field_3099_vals['vegetation_cover'],field_3099_vals['soil_temperature']])
       field_actual_crop_production_list.append(field_3099_vals['actual_crop_production'])
       field_actual_evapotranspiration_list.append(field_3099_vals['actual_evapotranspiration'])
      field_soil_water_potential_root_zone_list.append(field_3099_vals['soil_water_potential_root_zone'])
      field_name_list.append(field_3099_vals['name'])
    if field_3097 != False:
      for i in field_3097:
       field_3097_vals = field_3097[i]
       soil_temprature_list.append(field_3097_vals['soil_temperature'])
       soil_moisture_holding_capacity_list.append(field_3097_vals['soil_moisture_holding_capacity'])
       dates_list.append(field_3097_vals['date'])
       field_data.append([field_3097_vals['name'],field_3097_vals['date'],field_3097_vals['vegetation_cover'],field_3097_vals['soil_temperature']])
       field_actual_crop_production_list.append(field_3097_vals['actual_crop_production'])
       field_actual_evapotranspiration_list.append(field_3097_vals['actual_evapotranspiration'])
       field_soil_water_potential_root_zone_list.append(field_3097_vals['soil_water_potential_root_zone'])
       field_name_list.append(field_3097_vals['name'])
    #date_list = ['2022-12-23','2022-12-24','2022-12-25']
    df = pd.DataFrame({
                "fields_name": field_name_list,
                "actual_evapotranspiration": field_actual_evapotranspiration_list
            })
    fig = px.pie(df, values='actual_evapotranspiration', names='fields_name', hole=.3,height=300)
    fig.update_layout(
                title_text='Actual Evapotranspiration per fields',
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
               )
    
    df3 = pd.DataFrame({'field':field_name_list,'orders':orders_list,'crop_production':field_actual_crop_production_list}) 
    fig4 = px.bar(df3, x="field", y="crop_production", 
                 color="orders", barmode="group")
    fig4.update_layout(title_text='Crop Production per fields',width=1000,height=300,plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'])
    data= {'Orders':orders_list,
       'Field': field_name_list,
     'Soil Water Potential Root Zone': field_soil_water_potential_root_zone_list      
     }
    df7 = pd.DataFrame(data)
    line_plot = px.area(df7, x='Field', y='Soil Water Potential Root Zone',color='Orders',pattern_shape="Orders", pattern_shape_sequence=[".", "x", "+"],height=300,width=1000)
    line_plot.update_layout(
                title_text='Soil Water Potential Root Zone',
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
               )
    data1=[soil_temprature_list]
    if selected_date == '20221223':
      fig9 = px.imshow(data1,
                labels=dict(x="Fields", y="Date", color="Soil Temprature"),
                x=field_name_list,
                y=['2022-12-23']
               )
    elif selected_date == '20221224':
       fig9 = px.imshow(data1,
                labels=dict(x="Fields", y="Date", color="Soil Temprature"),
                x=field_name_list,
                y=['2022-12-24']
               )
    else:
      fig9 = px.imshow(data1,
                labels=dict(x="Fields", y="Date", color="Soil Temprature"),
                x=field_name_list,
                y=['2022-12-25']
               )
    fig9.update_xaxes(side="top")
    fig9.update_layout(
                title_text='Soil Temprature',
                width=1000,
                height=300,
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text']
               ) 
    chart1 = plot({'data':fig9},output_type='div')
    area_chart = plot({'data':line_plot},output_type='div')
    charts = plot({'data':fig4},output_type='div')
    pie_chart = plot({'data':fig},output_type='div')
    context = {'bar_graph':charts,'pie_graph':pie_chart,'area_graph':area_chart,'box_graph':chart1,'field_data':field_data}
    return HttpResponse(json.dumps(context),content_type='application/json')

def get_all_dates_data(selected_field):
    token = get_oauth2_token()
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    url_field_data_3103_23 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = '20221223')
    url_field_data_3099_23 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = '20221223')
    url_field_data_3097_23 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = '20221223')
    url_field_data_3103_24 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = '20221224')
    url_field_data_3099_24 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = '20221224')
    url_field_data_3097_24 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = '20221224')
    url_field_data_3103_25 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = '6f32f9ce-5266-4d68-b6f1-b314e31a071f',date = '20221225')
    url_field_data_3099_25 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f',date = '20221225')
    url_field_data_3097_25 ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',date = '20221225')
    response_field_3103_23 = requests.get(url=url_field_data_3103_23,headers=headers)
    response_field_3099_23 = requests.get(url=url_field_data_3099_23,headers=headers)
    response_field_3097_23 = requests.get(url=url_field_data_3097_23,headers=headers)
    response_field_3103_24 = requests.get(url=url_field_data_3103_24,headers=headers)
    response_field_3099_24 = requests.get(url=url_field_data_3099_24,headers=headers)
    response_field_3097_24 = requests.get(url=url_field_data_3097_24,headers=headers)
    response_field_3103_25 = requests.get(url=url_field_data_3103_25,headers=headers)
    response_field_3099_25 = requests.get(url=url_field_data_3099_25,headers=headers)
    response_field_3097_25 = requests.get(url=url_field_data_3097_25,headers=headers)
    field_3103_23 = response_field_3103_23.json()
    field_3099_23 = response_field_3099_23.json()
    field_3097_23 = response_field_3097_23.json()
    field_3103_24 = response_field_3103_24.json()
    field_3099_24 = response_field_3099_24.json()
    field_3097_24 = response_field_3097_24.json()
    field_3103_25 = response_field_3103_25.json()
    field_3099_25 = response_field_3099_25.json()
    field_3097_25 = response_field_3097_25.json()
    data_list = []
    dry_matter_production_cumulative_list = []
    water_unlimited_dry_matter_production_cumulative_list = []
    attainable_production_cumulative_list = []
    vegetation_cover_list = []
    field_name = []
    if field_3103_23 != False:
      for i in field_3103_23:
        field_3103_vals_23 = field_3103_23[i]
        field_name.append(field_3103_vals_23['name'])
        dry_matter_production_cumulative_list.append({'name':field_3103_vals_23['name'],'crop_production_cumulative':field_3103_vals_23['crop_production_cumulative']})
        water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3103_vals_23['name'],'water_unlimited_crop_production':field_3103_vals_23['water_unlimited_crop_production']})
        attainable_production_cumulative_list.append({'name':field_3103_vals_23['name'],'attainable_crop_production':field_3103_vals_23['attainable_crop_production']})
        vegetation_cover_list.append({'name':field_3103_vals_23['name'],'vegetation_cover':field_3103_vals_23['vegetation_cover']})
        data_list.append([field_3103_vals_23['date'],field_3103_vals_23['name'],field_3103_vals_23['soil_moisture_holding_capacity']])
    if field_3099_23 != False:
      for i in field_3099_23:
       field_3099_vals_23 = field_3099_23[i]
       field_name.append(field_3099_vals_23['name'])
       dry_matter_production_cumulative_list.append({'name':field_3099_vals_23['name'],'crop_production_cumulative':field_3099_vals_23['crop_production_cumulative']})
       water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3099_vals_23['name'],'water_unlimited_crop_production':field_3099_vals_23['water_unlimited_crop_production']})
       attainable_production_cumulative_list.append({'name':field_3099_vals_23['name'],'attainable_crop_production':field_3099_vals_23['attainable_crop_production']})
       vegetation_cover_list.append({'name':field_3099_vals_23['name'],'vegetation_cover':field_3099_vals_23['vegetation_cover']})
       data_list.append([field_3099_vals_23['date'], field_3099_vals_23['name'],field_3099_vals_23['soil_moisture_holding_capacity']])
    if field_3097_23 != False:
      for i in field_3097_23:
        field_3097_vals_23 = field_3097_23[i]  
        field_name.append(field_3097_vals_23['name'])
        dry_matter_production_cumulative_list.append({'name':field_3097_vals_23['name'],'crop_production_cumulative':field_3097_vals_23['crop_production_cumulative']})
        water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3097_vals_23['name'],'water_unlimited_crop_production':field_3097_vals_23['water_unlimited_crop_production']})
        attainable_production_cumulative_list.append({'name':field_3097_vals_23['name'],'attainable_crop_production':field_3097_vals_23['attainable_crop_production']})
        vegetation_cover_list.append({'name':field_3097_vals_23['name'],'vegetation_cover':field_3097_vals_23['vegetation_cover']})
        data_list.append([field_3097_vals_23['date'], field_3097_vals_23['name'],field_3097_vals_23['soil_moisture_holding_capacity']])
    if field_3103_24 != False:
      for i in field_3103_24:
        field_3103_vals_24 = field_3103_24[i]
        field_name.append(field_3103_vals_24['name'])
        dry_matter_production_cumulative_list.append({'name':field_3103_vals_24['name'],'crop_production_cumulative':field_3103_vals_24['crop_production_cumulative']})
        water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3103_vals_24['name'],'water_unlimited_crop_production':field_3103_vals_24['water_unlimited_crop_production']})
        attainable_production_cumulative_list.append({'name':field_3103_vals_24['name'],'attainable_crop_production':field_3103_vals_24['attainable_crop_production']})
        vegetation_cover_list.append({'name':field_3103_vals_24['name'],'vegetation_cover':field_3103_vals_24['vegetation_cover']})
        data_list.append([field_3103_vals_24['date'],field_3103_vals_24['name'],field_3103_vals_24['soil_moisture_holding_capacity']])
    if field_3099_24 != False:
      for i in field_3099_24:
       field_3099_vals_24 = field_3099_24[i]
       field_name.append(field_3099_vals_24['name'])
       dry_matter_production_cumulative_list.append({'name':field_3099_vals_24['name'],'crop_production_cumulative':field_3099_vals_24['crop_production_cumulative']})
       water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3099_vals_24['name'],'water_unlimited_crop_production':field_3099_vals_24['water_unlimited_crop_production']})
       attainable_production_cumulative_list.append({'name':field_3099_vals_24['name'],'attainable_crop_production':field_3099_vals_24['attainable_crop_production']})
       vegetation_cover_list.append({'name':field_3099_vals_24['name'],'vegetation_cover':field_3099_vals_24['vegetation_cover']})
       data_list.append([field_3099_vals_24['date'], field_3099_vals_24['name'],field_3099_vals_24['soil_moisture_holding_capacity']])
    if field_3097_24 != False:
      for i in field_3097_24:
        field_3097_vals_24 = field_3097_24[i]  
        field_name.append(field_3097_vals_24['name'])
        dry_matter_production_cumulative_list.append({'name':field_3097_vals_24['name'],'crop_production_cumulative':field_3097_vals_24['crop_production_cumulative']})
        water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3097_vals_24['name'],'water_unlimited_crop_production':field_3097_vals_24['water_unlimited_crop_production']})
        attainable_production_cumulative_list.append({'name':field_3097_vals_24['name'],'attainable_crop_production':field_3097_vals_24['attainable_crop_production']})
        vegetation_cover_list.append({'name':field_3097_vals_24['name'],'vegetation_cover':field_3097_vals_24['vegetation_cover']})
        data_list.append([field_3097_vals_24['date'], field_3097_vals_24['name'],field_3097_vals_24['soil_moisture_holding_capacity']])
    if field_3103_25 != False:
      for i in field_3103_25:
        field_3103_vals_25 = field_3103_25[i]
        field_name.append(field_3103_vals_25['name'])
        dry_matter_production_cumulative_list.append({'name':field_3103_vals_25['name'],'crop_production_cumulative':field_3103_vals_25['crop_production_cumulative']})
        water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3103_vals_25['name'],'water_unlimited_crop_production':field_3103_vals_25['water_unlimited_crop_production']})
        attainable_production_cumulative_list.append({'name':field_3103_vals_25['name'],'attainable_crop_production':field_3103_vals_25['attainable_crop_production']})
        vegetation_cover_list.append({'name':field_3103_vals_25['name'],'vegetation_cover':field_3103_vals_25['vegetation_cover']})
        data_list.append([field_3103_vals_25['date'],field_3103_vals_25['name'],field_3103_vals_25['soil_moisture_holding_capacity']])
    if field_3099_25 != False:
      for i in field_3099_25:
       field_3099_vals_25 = field_3099_25[i]
       field_name.append(field_3099_vals_25['name'])
       dry_matter_production_cumulative_list.append({'name':field_3099_vals_25['name'],'crop_production_cumulative':field_3099_vals_25['crop_production_cumulative']})
       water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3099_vals_25['name'],'water_unlimited_crop_production':field_3099_vals_25['water_unlimited_crop_production']})
       attainable_production_cumulative_list.append({'name':field_3099_vals_25['name'],'attainable_crop_production':field_3099_vals_25['attainable_crop_production']})
       vegetation_cover_list.append({'name':field_3099_vals_25['name'],'vegetation_cover':field_3099_vals_25['vegetation_cover']})
       data_list.append([field_3099_vals_25['date'], field_3099_vals_25['name'],field_3099_vals_25['soil_moisture_holding_capacity']])
    if field_3097_25 != False:
      for i in field_3097_25:
        field_3097_vals_25 = field_3097_25[i]
        field_name.append(field_3097_vals_25['name'])
        dry_matter_production_cumulative_list.append({'name':field_3097_vals_25['name'],'crop_production_cumulative':field_3097_vals_25['crop_production_cumulative']})
        water_unlimited_dry_matter_production_cumulative_list.append({'name':field_3097_vals_25['name'],'water_unlimited_crop_production':field_3097_vals_25['water_unlimited_crop_production']})
        attainable_production_cumulative_list.append({'name':field_3097_vals_25['name'],'attainable_crop_production':field_3097_vals_25['attainable_crop_production']})
        vegetation_cover_list.append({'name':field_3097_vals_25['name'],'vegetation_cover':field_3097_vals_25['vegetation_cover']})  
        data_list.append([field_3097_vals_25['date'], field_3097_vals_25['name'],field_3097_vals_25['soil_moisture_holding_capacity']])
        final_crop_production_cumulative_list = []
        final_water_unlimited_dry_matter_production_list = []
        final_dry_matter_production_cumulative_list = []
        final_vegetation_cover_list = []
        for x in dry_matter_production_cumulative_list:
           if x['name'] == selected_field:
             final_crop_production_cumulative_list.append(x['crop_production_cumulative'])
        for y in water_unlimited_dry_matter_production_cumulative_list:
          if y['name'] == selected_field:
           final_water_unlimited_dry_matter_production_list.append(y['water_unlimited_crop_production'])
        for z in attainable_production_cumulative_list:
           if z['name'] == selected_field:
            final_dry_matter_production_cumulative_list.append(z['attainable_crop_production'])
        for i in vegetation_cover_list:
           if i['name'] == selected_field:
             final_vegetation_cover_list.append(i['vegetation_cover'])


    return data_list,final_crop_production_cumulative_list,final_water_unlimited_dry_matter_production_list,final_dry_matter_production_cumulative_list,final_vegetation_cover_list

def area_graph_date(data_list,crop_production,field_name_list,soil_moisture_holding_capacity_list):
     dates_list = ['2022-12-23','2022-12-24','2022-12-25','2022-12-24','2022-12-23']
     df = pd.DataFrame(data_list,columns={
                "Date",
                "field_name",
                "Holding_Capacity"
                
            })             
     fig = px.line(df, x='Holding_Capacity', y='Date',color='field_name')
     fig.update_xaxes(fixedrange=True)
     fig.update_xaxes(tickformat="%b %d\n%Y")
     fig.update_xaxes(dtick='M1')
     return fig

def add_categorical_legend(folium_map, title, colors, labels):
    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """
    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map


def add_modal(folium_map):
  
    
    legend_html = f"""
    <div id="myModalgraph" class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Modal title</h5>
          <button type="button" class="btn-close" data-bs-target="#myModal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>Modal body text goes here.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>
    """
    script = f"""
         <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
         <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
      """
   

    css = """
   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <style type='text/css'>
      .modal:before {
            content: '';
            display: inline-block;
            height: 100%;
            margin-left:-300px;
            vertical-align: middle;
        }
          
        .modal-dialog {
            display: inline-block;
            vertical-align: middle;
        }
          
        .modal .modal-content {
            padding: 20px 20px 20px 20px;
            -webkit-animation-name: modal-animation;
            -webkit-animation-duration: 0.5s;
            animation-name: modal-animation;
            animation-duration: 0.5s;
        }
          
        @-webkit-keyframes modal-animation {
            from {
                top: -100px;
                opacity: 0;
            }
            to {
                top: 0px;
                opacity: 1;
            }
        }
          
        @keyframes modal-animation {
            from {
                top: -100px;
                opacity: 0;
            }
            to {
                top: 0px;
                opacity: 1;
            }
        }
    </style>
    """
    folium_map.get_root().header.add_child(folium.Element(legend_html + css))

    return folium_map


def get_oauth2_token():
    auth_url = "https://portal.irriwatch.com/oauth/v2/token"
    headers_auth = {
        "content-type": "application/x-www-form-urlencoded"
       
        } 
    body_auth = {"grant_type":"client_credentials","client_id":"ewzvs7nRh0FoiwnMkxd1MjkR8brOQSdz","client_secret":"r2TfYLayZR2F0PcesAVNNSbDrbRXDFknM98d6H2G75o8sec98NyxeBwTUwkTNzf4"}
    response_auth = requests.post(url=auth_url,headers=headers_auth,data=body_auth)
    response_auth_json = response_auth.json()
    token = response_auth_json['access_token']
    return token

def pixel_level_api():
    token = get_oauth2_token()
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    url_result_uuids ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result'.format(
    company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',
    order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e'
     )
    result_uuid_result = []
    result_uuids_response = requests.get(url = url_result_uuids,headers = headers)
    list_result_uuids = json.loads(result_uuids_response.content)
    #credentials = Credentials.from_service_account_file(
     #        'google-cloud-storage_auth.json'
     #   )
    #c = {
  #"type": "service_account",
  #"private_key_id": "b52b31579f903c3dfe4007069e3bb45d6f832c5b",
  #"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQClx+I4FwixlLdw\nJDwu5kLy3B6Vvj5To0bObbFfkNG16W1Dol6Ep9ncICqYTGhoqI8jk7DWBwlDlFju\nnoA/ZxQzwgdTKti8GS1uk5XuuShWZyNMUUfoiUZKHYf8MaiFrTtuIkL+JMu735Gs\nD2T879c3k1vG1jayQRuF0HveRoqO8d93EM/ZMZQ10C44wET3jt6KzG0NrJArFFgp\nodXATzdRa0FiOEt6PSFJYy/T1dzwRVSVQwZk15/tOVmAJl+lmT9Rh9iB/oaCUBwc\nhnGeoDPy3UH1hBzPg4T94AOYtDrkm7Cuc22gOOx2td5kcjtY72lTGa3kzI7Krawx\nZpJSct+dAgMBAAECggEAHN8OPTF5wJ+DQOL2nj5Yu33tT6vVo/BEFRBSey+37gPs\nlQJSjqzCyszJTkPETTHJ1+rRObz49o1/3XK6KBCWGpt4dhn4q+2AlYjbbDtP1Jha\ns+BV8x/xH1g8RgYJ8NnmBzytSSB0YNBDSOFXd5t3ckTWD29gEDQ5jFjuMZw8Zj9e\nIZw9vYL3crLlxIAHSmEzbyJ9yMxjmnGDdH+OoWuzRH3Te7Ayh2PIKbF1NPVHRZhc\nWjgJiMqUxEsRSw8pjsK59x22WyhLKBVizUiSHX0MYm9Ii31oFQmh444PTRBlpCYH\n2iGsPfTrakNPizwnss+GJiiJoPv5MZICrXvvIJSfiwKBgQDocgZTrUQ0u64CVDol\nmFPJvz6oEPmg7l7v+zt7SLCCxZzZddkVz0I87asOj+WwUSL/igF8Juc5paZs5Nq6\n67B4pnvWxisHlotTI4kTlX2BhL1bPtCdbG4hAOTmwmkBXgBls6ul1e7MZBa8QBXS\nLUZ4BbCihKLzt695eM7qzNCU/wKBgQC2lHshNsdMtgYfv9VtURyPCj8ChCLWgEZt\nfE8GE5OcD1eqEV2OYtnLxqkpEqCIbcCecWcddluq7Zn0N/eTJKUwzvbBX/whkmLI\nFTV/5yxpbvkh1PiRYHc4BaPPCY1dbF8Rx9HgZ1w6lJWx4YcP6a2nWRSrTEyAj7sB\nOBdA9mG/YwKBgQDZCcbgkNMzzd4/bHfSrLXnlbuiYB9F5e0ddN7oUUoHAQ9geUpW\ns+xsSZrEARZ9mHTuV+TlEMosKIEKAnI9wF5JeWH+e5CoCChVW8PdVmMW8WOBdFiD\n9T+rb1NMKFC1pxkF3UqzkNrlW7ti0Q/O7Nl0rhNs3B3vJR8ic+v4j39e7wKBgFUu\nkQO9+t3fTpwhdAG8hgZ2UU9rNpW84x7RkEzVdViqD8xYrb1wgQyBcwqmlh8QlX1W\nizVDsyDcGafHNMqBnlBXPuiZT5iaI1wWCQ/TWvUVwUX3hsDMsNKCTxqY6ktb9D7n\naxO3JWBvUifbgJf7/fjFps8EmeyhIi4/bRnx2UjhAoGAJ/924kiCYiPdhnvQQexQ\nAJXnHgQFQTbX01kARsLrC60/rqdWhIHC5WK2iein5ftJJwbhGNnHe/5MnNCr4VJN\nuozl4qrcEvanl+CrwzyJvT6F0jOheRyAoWme+ojSCllbR3vWAi4ysBHnIA++SGPN\nXLPO2LF/GGNASqThtcMGPWw=\n-----END PRIVATE KEY-----\n",
  #"client_email": "owais-703@proj-344411.iam.gserviceaccount.com",
  #"client_id": "113541826885100726004",
 
#}

    #credentials1 = ServiceAccountCredentials.from_json_keyfile_dict(
     #        c
      #  )
    #client = s.Client(credentials=credentials, project='Project Management')
    #client1 = gs.Client(credentials=credentials1, project='Project Management')
    #blobs = client.list_blobs('filebucket_map')
    #bucket = client1.get_bucket('filebucket_map') 
    #bucket.delete_blobs(blobs=list(blobs))
   
    url_tiff_data ='https://portal.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{result_uuid}'.format(
         company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',
         order_uuid = '6809fe46-5bfc-4c5c-8e90-b267c705be2e',
         result_uuid = 'dc748211-d3db-f575-996b-5d8e26d6e35f'
         )
    tiff_data_response = requests.get(
         url = url_tiff_data,
         headers = headers
         )
    zipfile_data = zipfile.ZipFile(io.BytesIO(tiff_data_response.content)) 
    path_to_save = 'C:/Users/CC/Desktop/irriwatch api doc/zip/3097 2022-12-25'
          # extract all zipped data to given path
    zipfile_data.extractall(path_to_save)   
         #blob = bucket.blob(zipfile_data)
         #blob.upload_from_string('this is test content!')
         #zipextract(zipfile_data,credentials,tiff_data_response.content)
        

def zipextract(zipfile,cred,data):
    client1 = s.Client(credentials=cred, project='Project Management')
    bucket = client1.get_bucket('filebucket_map') 
    zipfilename_with_path = 'gs://filebucket_map/'+str(zipfile)+''
    blob = bucket.blob(zipfilename_with_path)
    zipbytes = io.BytesIO(data)
    if is_zipfile(zipbytes):
       with ZipFile(zipbytes, 'r') as myzip:
            for contentfilename in myzip.namelist():
                contentfile = myzip.read(contentfilename)
                blob = bucket.blob(zipfilename_with_path + "/" + contentfilename)
                blob.upload_from_string(contentfile)



def get_pixel_data_from_tif(selected_order_val,selected_date,selected_pixel_level_val,order_results):
    driver=gdal.GetDriverByName('GTiFF')
    driver.Register() 
    SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    ds1 = None
    if selected_order_val == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
      if selected_pixel_level_val == 'moisture_status':
        if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3103 ms.tif')
          ds1 = gdal.Open('2022-12-23 3103 ms2.tif') 
        elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3103 ms.tif') 
          ds1 = gdal.Open('2022-12-24 3103 ms2.tif')
        else:
          ds = gdal.Open('2022-12-25 3103 ms.tif')
          ds1 = gdal.Open('2022-12-25 3103 ms2.tif') 
      elif selected_pixel_level_val == 'vegetation_cover':
        if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3103 vc.tif') 
          ds1 = gdal.Open('2022-12-23 3103 vc2.tif') 
        elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3103 vc.tif') 
          ds1 = gdal.Open('2022-12-24 3103 vc2.tif') 
        else:
          ds = gdal.Open('2022-12-25 3103 vc.tif') 
          ds1 = gdal.Open('2022-12-25 3103 vc2.tif') 
      else:
        if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3103 ae.tif') 
          ds1 = gdal.Open('Geotiff/2022-12-23 3103 ae2.tif') 
        elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3103 ae.tif') 
          ds1 = gdal.Open('2022-12-24 3103 ae2.tif') 
        else:
          ds = gdal.Open('2022-12-25 3103 ae.tif') 
          ds1 = gdal.Open('2022-12-25 3103 ae2.tif')
    elif selected_order_val == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
       if selected_pixel_level_val == 'moisture_status':
        if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3099 ms.tif')
        elif selected_date == '20221224':
           ds = gdal.Open('2022-12-24 3099 ms.tif')
        else:
          ds = gdal.Open('2022-12-25 3099 ms.tif')
       elif selected_pixel_level_val == 'vegetation_cover':
        if selected_date == '20221223':
           ds = gdal.Open('2022-12-23 3099 vc.tif')
        elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3099 vc.tif')
        else:
          ds = gdal.Open('2022-12-25 3099 vc.tif')
       else:
         if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3099 ae.tif')
         elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3099 ae.tif')
         else:  
          ds = gdal.Open('2022-12-25 3099 ae.tif')
    else:
       if selected_pixel_level_val == 'moisture_status':
        if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3097 ms.tif')
          ds1 = gdal.Open('2022-12-23 3097 ms2.tif')
        elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3097 ms.tif')
          ds1 = gdal.Open('2022-12-24 3097 ms2.tif')
        else:
          ds = gdal.Open('2022-12-25 3097 ms.tif')
          ds1 = gdal.Open('2022-12-25 3097 ms2.tif')
       elif selected_pixel_level_val == 'vegetation_cover':
        if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3097 vc.tif')
          ds1 = gdal.Open('2022-12-23 3097 vc2.tif')
        elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3097 vc.tif')
          ds1 = gdal.Open('2022-12-24 3097 vc2.tif')
        else:
          ds = gdal.Open('2022-12-25 3097 vc.tif')
          ds1 = gdal.Open('2022-12-25 3097 vc2.tif')
       else:
        if selected_date == '20221223':
          ds = gdal.Open('2022-12-23 3097 ae.tif')
          ds1 = gdal.Open('2022-12-23 3097 ae2.tif')
        elif selected_date == '20221224':
          ds = gdal.Open('2022-12-24 3097 ae.tif')
          ds1 = gdal.Open('2022-12-24 3097 ae2.tif')
        else:
          ds = gdal.Open('2022-12-25 3097 ae.tif')
          ds1 = gdal.Open('2022-12-25 3097 ae2.tif')
    #band1[0:10,0:10] = 0
    
      
    if ds is not None:
      geotransform = ds.GetGeoTransform()
      cols = ds.RasterXSize 
      rows = ds.RasterYSize 
      xmin=geotransform[0]
      ymax=geotransform[3]
      xmax=xmin+cols*geotransform[1]
      ymin=ymax+rows*geotransform[5]
      centerx=(xmin+xmax)/2
      centery=(ymin+ymax)/2
      bands = ds.RasterCount
      r = ds.GetRasterBand(1).ReadAsArray()
      g = ds.GetRasterBand(2).ReadAsArray()
      b = ds.GetRasterBand(3).ReadAsArray()
      a = ds.GetRasterBand(4).ReadAsArray()
      rgb =np.dstack((r,g,b,a))
    if ds1 is not None:
      geotransform1 = ds1.GetGeoTransform()
      cols1 = ds1.RasterXSize 
      rows1 = ds1.RasterYSize 
      xmin1=geotransform1[0]
      ymax1=geotransform1[3]
      xmax1=xmin1+cols1*geotransform1[1]
      ymin1=ymax1+rows1*geotransform1[5]
      centerx1=(xmin1+xmax1)/2
      centery1=(ymin1+ymax1)/2
      bands1 = ds1.RasterCount
      r1 = ds1.GetRasterBand(1).ReadAsArray()
      g1 = ds1.GetRasterBand(2).ReadAsArray()
      b1 = ds1.GetRasterBand(3).ReadAsArray()
      a1 = ds1.GetRasterBand(4).ReadAsArray()
     
      rgb1 =np.dstack((r1,g1,b1,a1))
     
    count = 0
    map= folium.Map(location=[centery, centerx], zoom_start=7,tiles='openstreetmap')
    for i in order_results[0]['fields']['features']:
        fields_geojson = order_results[0]['fields']['features'][count]['geometry']
        folium.GeoJson(fields_geojson,style_function=lambda x:{'fillOpacity': 0}).add_to(map)
        count += 1
    image = folium.raster_layers.ImageOverlay(
          rgb,opacity=3, bounds=[[ymin,xmin],[ymax,xmax]]
      )
    image.add_to(map) 
    map.fit_bounds(map.get_bounds(), padding=(10, 10)) 
    if ds1 is not None:           
      image = folium.raster_layers.ImageOverlay(
      rgb1,opacity=3, bounds=[[ymin1,xmin1],[ymax1,xmax1]]
       )
      image.add_to(map)
     
    return map

def scaleMinMax(x):
  return((x - np.nanmin(x))/(np.nanmax(x)- np.nanmin(x)))
   
def get_color(x):
    decimals = 2
    x = np.around(x, decimals=decimals)
    ls = np.linspace(0,1,10**decimals+1)
    if 0 <= x <= 1:
        return cm.get_cmap('viridis')(ls)[np.argwhere(ls==x)]
  
    

def field_level_api(headers,field_level,companyid,orderid,date):
    token = get_oauth2_token()
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    url_field_data ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = companyid,order_uuid = orderid,date = date)
    response_field_levels = requests.get(url=url_field_data,headers=headers)
    field_level_res = eval(response_field_levels.content)
    vegetation_cover_list = []
    field_uuid_list = []
    actual_evapotranspiration_list = []
    applied_water_cumulative_list = []
    for i in field_level_res:
        field_uuid = i     
        field_level_vals = field_level_res[field_uuid]         
        field_uuid_list.append(field_uuid)
        vegetation_cover_list.append(field_level_vals['vegetation_cover'])
        actual_evapotranspiration_list.append(field_level_vals['actual_evapotranspiration'])
        applied_water_cumulative_list.append(field_level_vals['irrigation_amount_cumulative']) 
    if field_level=='vegetation_cover':
      return field_uuid_list,vegetation_cover_list
    elif field_level == 'irrigation_amount_cumulative':
      return field_uuid_list,applied_water_cumulative_list
    else:
      return field_uuid_list,actual_evapotranspiration_list


def map(request):
    selected_field_level_val = request.POST.get('selected_field_level',False)
    selected_pixel_level_val = request.POST.get('pixel_level_ddl',False)
    selected_order_val = request.POST.get('selected_order',False)
    selected_date = request.POST.get('selected_date',False)
    token = get_oauth2_token()
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    if selected_order_val == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
     url_company_orders = "https://api.irriwatch.com/api/v1/company/06db5883-48bd-4350-93e7-0e0ae69fe94c/order"
    elif selected_order_val == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
      url_company_orders = "https://api.irriwatch.com/api/v1/company/ac082ccd-4605-4a51-b272-fc4856cade6c/order"  
    else:
      url_company_orders = "https://api.irriwatch.com/api/v1/company/06db5883-48bd-4350-93e7-0e0ae69fe94c/order"  
    response_orders = requests.get(url=url_company_orders,headers=headers)
    list_result_uuids = json.loads(response_orders.content)
    list_result = list_result_uuids
   
    m = folium.Map(tiles="openstreetmap",zoom_start=10)
    count = 0
    #api_pixel_level = pixel_level_api()
    if selected_field_level_val != False or selected_field_level_val!='none':
     if selected_order_val == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
        if selected_date != False:
            if selected_date != 'none':
              api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,selected_date)
            else:
             api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,'20221224')
        else:
           api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,'20221224')
     elif selected_order_val == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
         if selected_date != False:
            if selected_date != 'none' and selected_order_val != 'none':
             api_field_level_data = field_level_api(headers,selected_field_level_val,'ac082ccd-4605-4a51-b272-fc4856cade6c',selected_order_val,selected_date)
            else:
               api_field_level_data = field_level_api(headers,selected_field_level_val,'ac082ccd-4605-4a51-b272-fc4856cade6c','30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f','20221224') 
         else:
            api_field_level_data = field_level_api(headers,selected_field_level_val,'ac082ccd-4605-4a51-b272-fc4856cade6c',selected_order_val,'20221224')
     else:
        if selected_date != False:
         if selected_date != 'none' and selected_order_val != 'none':
           api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,selected_date)
         else:
            api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c','6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
        else:
           api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c','6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
    if selected_pixel_level_val == False or selected_pixel_level_val == 'none':
     for i in list_result[0]['fields']['features']:  
         fields_geojson = list_result[0]['fields']['features'][count]['geometry']
         field_uuid = list_result[0]['fields']['features'][count]['properties']['uuid'] 
         field_name = list_result[0]['fields']['features'][count]['properties']['name'] 
         style_function =  {
             "fillColor": "#D3D3D3",
            }
         if selected_order_val != False and selected_date != False:
            if selected_order_val!='none' and selected_date!='none':
                style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,selected_order_val,selected_date)
            elif selected_order_val!='none':
             style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,selected_order_val,'20221224')
            elif selected_date!= 'none':
                style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,'6f32f9ce-5266-4d68-b6f1-b314e31a071f',selected_date)
            else:
                 style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,'6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
         else:
            style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,'6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
         if selected_field_level_val == False:  
          style_function =  {
             "fillColor": "#D3D3D3",
            }
         count += 1
         if selected_field_level_val != False:
          geo_json = folium.GeoJson(fields_geojson,style_function=lambda x, fillColor=style_function['fillColor']:{
                "fillColor": fillColor,
                'fillOpacity': 2 
             }).add_to(m)     
          geo_json.add_child(folium.Popup('<button id="btnopengraphs" type="button" class="btn btn-primary">'+field_name+'</button>'))
         else:
          #m = add_modal(m)
          geo_json = folium.GeoJson(fields_geojson,style_function=lambda x, fillColor=style_function['fillColor']:{
                "fillColor": fillColor,
                'fillOpacity': 0
                }).add_to(m)
          html="""
           <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
           <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>   
           <script type="text/javascript">
            function opengraphsmodal(id){ 
              window.top.postMessage(id, '*');
               
            }
           </script>
      
           <button id="""+field_uuid+""" onclick="opengraphsmodal(this.id)"  type="button"  class="btn btn-primary">"""+field_name+"""</button>
          """          
          iframe = folium.IFrame(html=html, width=100, height=70)
          geo_json.add_child(folium.Popup(iframe,max_width=100))
         m.fit_bounds(m.get_bounds(), padding=(10, 10))
         
     if selected_field_level_val != False:
        if selected_field_level_val != 'none' and selected_order_val != 'none' and selected_date != 'none':
            m = set_range_legend(m,selected_field_level_val,selected_order_val,selected_date)
        else:
          if selected_order_val == 'none' and selected_date == 'none':
           m = set_range_legend(m,selected_field_level_val,'6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
          elif selected_order_val!='none' and selected_date == 'none':
             m = set_range_legend(m,selected_field_level_val,selected_order_val,'20221224')
          elif selected_order_val == 'none' and selected_date != 'none':
            m = set_range_legend(m,selected_field_level_val,'6f32f9ce-5266-4d68-b6f1-b314e31a071f',selected_date)
          else:
             m = set_range_legend(m,selected_field_level_val,selected_order_val,selected_date)

    else:
       m = get_pixel_data_from_tif()
  
    m = m._repr_html_()
    try:
      company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
      company = 'Company'
    if company == 'Company':
      company_name = 'Company'
    else:      
      company_name  = company.company
    context = {
            'm':m,
            'company_name': company_name
        }
    
  
    return render(request,'home/ui-maps.html',context)

def show_graphs(request):
   field_uuid_data = request.POST.get('field_uid',False)
   #val = id
   token = get_oauth2_token()
   headers = {"accept":"application/json","authorization":"Bearer "+token+""}
   selected_order_val = request.POST.get('selected_order',False)
   selected_date = request.POST.get('selected_date',False)
   if selected_order_val == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
    url_field_data ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = selected_order_val,date = selected_date)
   elif selected_order_val == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
      url_field_data ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ac082ccd-4605-4a51-b272-fc4856cade6c',order_uuid = selected_order_val,date = selected_date)
   elif selected_order_val == "6809fe46-5bfc-4c5c-8e90-b267c705be2e":
      url_field_data ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = 'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',order_uuid = selected_order_val,date = selected_date)
   else:
       url_field_data ='https://api.irriwatch.com/api/v1/company/{company_uuid}/order/{order_uuid}/result/{date}/field_level'.format(company_uuid = '06db5883-48bd-4350-93e7-0e0ae69fe94c',order_uuid = selected_order_val,date = selected_date) 
   response_orders = requests.get(url=url_field_data,headers=headers)
   count = 0
   field_name = ''
   field_level_res = eval(response_orders.content)
   field_actual_evapotranspiration_list = []
   field_name_list = []
   data_list = ''
   for i in field_level_res:
         field_uuid = i
         field_level_vals = field_level_res[field_uuid]
         if field_uuid_data == field_uuid:
            field_name = field_level_vals['name']
            field_name_list.append(field_level_vals['name'])
            field_actual_evapotranspiration_list.append(field_level_vals['actual_evapotranspiration'])
            data_list = get_all_dates_data(field_name)
            break
         count += 1
   df = pd.DataFrame({
                "fields_name": field_name_list,
                "actual_evapotranspiration": field_actual_evapotranspiration_list
            })
   fig = px.pie(df, values='actual_evapotranspiration', names='fields_name', hole=.3,height=300)
   fig.update_layout(
                title_text='Actual Evapotranspiration per fields'
                
               )
   pie_chart = plot({'data':fig},output_type='div')
   
   context = {'field_name': field_name,'pie_graph_modal':pie_chart,'crop_production_cumulative':data_list[1],'water_unlimited_crop_production':data_list[2],'attainable_crop_production':data_list[3],'vegetation_cover':data_list[4]}
   return JsonResponse(context)

def map_change(request):
  if request.method == "POST":
    selected_field_level_val = request.POST.get('selected_field_level',False)
    selected_pixel_level_val = request.POST.get('pixel_level_ddl',False)
    selected_order_val = request.POST.get('selected_order',False)
    selected_date = request.POST.get('selected_date',False)
    #api_pixel_level = pixel_level_api()
    token = get_oauth2_token()
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    if selected_order_val == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
     url_company_orders = "https://api.irriwatch.com/api/v1/company/06db5883-48bd-4350-93e7-0e0ae69fe94c/order"
    elif selected_order_val == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
      url_company_orders = "https://api.irriwatch.com/api/v1/company/ac082ccd-4605-4a51-b272-fc4856cade6c/order"  
    elif selected_order_val == "6809fe46-5bfc-4c5c-8e90-b267c705be2e":
      url_company_orders = "https://api.irriwatch.com/api/v1/company/ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28/order"
    else:
      url_company_orders = "https://api.irriwatch.com/api/v1/company/06db5883-48bd-4350-93e7-0e0ae69fe94c/order"  
    response_orders = requests.get(url=url_company_orders,headers=headers)
    list_result_uuids = json.loads(response_orders.content)
    list_result = list_result_uuids
   
    m = folium.Map(tiles="openstreetmap",zoom_start=10)
    count = 0
    if selected_order_val != 'none':
      if selected_order_val != False:
        if selected_field_level_val != False:
          if selected_order_val == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
            if selected_date != False:
              if selected_date != 'none':
                api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,selected_date)
              else:
                api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,'20221224')
            else:
               api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,'20221224')
          elif selected_order_val == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
             if selected_date != False:
                if selected_date != 'none' and selected_order_val != 'none':
                 api_field_level_data = field_level_api(headers,selected_field_level_val,'ac082ccd-4605-4a51-b272-fc4856cade6c',selected_order_val,selected_date)
                else:
                  api_field_level_data = field_level_api(headers,selected_field_level_val,'ac082ccd-4605-4a51-b272-fc4856cade6c','30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f','20221224') 
             else:
               api_field_level_data = field_level_api(headers,selected_field_level_val,'ac082ccd-4605-4a51-b272-fc4856cade6c',selected_order_val,'20221224')
          elif selected_order_val == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
              if selected_date != False:
                if selected_date != 'none' and selected_order_val != 'none':
                 api_field_level_data = field_level_api(headers,selected_field_level_val,'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',selected_order_val,selected_date)
                else:
                  api_field_level_data = field_level_api(headers,selected_field_level_val,'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28','6809fe46-5bfc-4c5c-8e90-b267c705be2e','20221224') 
              else:
               api_field_level_data = field_level_api(headers,selected_field_level_val,'ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28',selected_order_val,'20221224')
          else:
              if selected_date != False:
                if selected_date != 'none' and selected_order_val != 'none':
                  api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c',selected_order_val,selected_date)
              else:
                api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c','6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
      else:
         api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c','6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
    else:
           api_field_level_data = field_level_api(headers,selected_field_level_val,'06db5883-48bd-4350-93e7-0e0ae69fe94c','6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
   
    for i in list_result[0]['fields']['features']:  
         fields_geojson = list_result[0]['fields']['features'][count]['geometry']
         field_uuid = list_result[0]['fields']['features'][count]['properties']['uuid'] 
         field_name = list_result[0]['fields']['features'][count]['properties']['name']
         style_function =  {
             "fillColor": "#D3D3D3",
            }
         if selected_order_val != False and selected_date != False:
            if selected_order_val!='none' and selected_date!='none':
                style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,selected_order_val,selected_date)
            elif selected_order_val!='none':
             style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,selected_order_val,'20221224')
            elif selected_date!= 'none':
                style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,'6f32f9ce-5266-4d68-b6f1-b314e31a071f',selected_date)
            else:
                 style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,'6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
         else:
            style_function = change_field_level_color(selected_field_level_val,field_uuid,api_field_level_data,'6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224')
         if selected_field_level_val == False:  
          style_function =  {
             "fillColor": "#D3D3D3",
            }
         count += 1
         if selected_field_level_val != False:
          geo_json = folium.GeoJson(fields_geojson,style_function=lambda x, fillColor=style_function['fillColor']:{
                "fillColor": fillColor,
                'fillOpacity': 2 
           }).add_to(m)
          html="""
           <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
           <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>   
           <script type="text/javascript">
            function opengraphsmodal(id){ 
              window.top.postMessage(id, '*');
            }
           </script>
      
           <button id="""+field_uuid+""" onclick="opengraphsmodal(this.id)"  type="button"  class="btn btn-primary">"""+field_name+"""</button>
          """          
          iframe = folium.IFrame(html=html, width=100, height=70)
          geo_json.add_child(folium.Popup(iframe,max_width=100))
         else:
          geo_json = folium.GeoJson(fields_geojson,style_function=lambda x, fillColor=style_function['fillColor']:{
                "fillColor": fillColor,
                'fillOpacity': 0
             }).add_to(m)
          html="""
           <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
           <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>   
           <script type="text/javascript">
            function opengraphsmodal(id){ 
              window.top.postMessage(id, '*');
               
            }
           </script>
      
           <button id="""+field_uuid+""" onclick="opengraphsmodal(this.id)"  type="button"  class="btn btn-primary">"""+field_name+"""</button>
          """          
          iframe = folium.IFrame(html=html, width=100, height=70)
          geo_json.add_child(folium.Popup(iframe,max_width=100)) 
         m.fit_bounds(m.get_bounds(), padding=(10, 10))
    if selected_field_level_val != False:
        if selected_field_level_val != 'none' and selected_order_val != 'none' and selected_date != 'none':
            m = set_range_legend(m,selected_field_level_val,selected_order_val,selected_date,False)
        else:
          if selected_order_val == 'none' and selected_date == 'none':
           m = set_range_legend(m,selected_field_level_val,'6f32f9ce-5266-4d68-b6f1-b314e31a071f','20221224',False)
          elif selected_order_val!='none' and selected_date == 'none':
             m = set_range_legend(m,selected_field_level_val,selected_order_val,'20221224',False)
          elif selected_order_val == 'none' and selected_date != 'none':
            m = set_range_legend(m,selected_field_level_val,'6f32f9ce-5266-4d68-b6f1-b314e31a071f',selected_date,False)
          else:
             m = set_range_legend(m,selected_field_level_val,selected_order_val,selected_date,False)

    if selected_field_level_val == 'none': 
      if selected_pixel_level_val != 'none':
        m = get_pixel_data_from_tif(selected_order_val,selected_date,selected_pixel_level_val,list_result)
        m = set_range_legend(m,False,selected_order_val,selected_date,selected_pixel_level_val)

    m = m._repr_html_()
       

    return HttpResponse(m)

def pixel_map(request):
    selected_field_level_val = request.POST.get('selected_field_level',False)
    selected_pixel_level_val = request.POST.get('pixel_level_ddl',False)
    selected_order_val = request.POST.get('selected_order',False)
    selected_date = request.POST.get('selected_date',False)
    token = get_oauth2_token()
    headers = {"accept":"application/json","authorization":"Bearer "+token+""}
    if selected_order_val == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
        url_company_orders = "https://api.irriwatch.com/api/v1/company/06db5883-48bd-4350-93e7-0e0ae69fe94c/order"
    elif selected_order_val == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
        url_company_orders = "https://api.irriwatch.com/api/v1/company/ac082ccd-4605-4a51-b272-fc4856cade6c/order"  
    elif selected_order_val == "6809fe46-5bfc-4c5c-8e90-b267c705be2e":
        url_company_orders = "https://api.irriwatch.com/api/v1/company/ef9ff8a0-e81a-43c1-af24-0ecdc4d87b28/order"
    else:
        url_company_orders = "https://api.irriwatch.com/api/v1/company/06db5883-48bd-4350-93e7-0e0ae69fe94c/order"  
    response_orders = requests.get(url=url_company_orders,headers=headers)
    list_result_uuids = json.loads(response_orders.content)
    list_result = list_result_uuids
    
    if selected_field_level_val == 'none' and selected_pixel_level_val == 'none':
        count = 0
        for i in list_result[0]['fields']['features']:
          fields_geojson = list_result[0]['fields']['features'][count]['geometry']
          field_uuid = list_result[0]['fields']['features'][count]['properties']['uuid'] 
          field_name = list_result[0]['fields']['features'][count]['properties']['name']
          geo_json = folium.GeoJson(fields_geojson,style_function=lambda x:{'fillOpacity': 0}).add_to(map)
          html="""
           <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
           <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.1/jquery.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>   
           <script type="text/javascript">
            function opengraphsmodal(id){ 
              window.top.postMessage(id, '*');
            }
           </script>
      
           <button id="""+field_uuid+""" onclick="opengraphsmodal(this.id)"  type="button"  class="btn btn-primary">"""+field_name+"""</button>
          """          
          iframe = folium.IFrame(html=html, width=100, height=70)
          geo_json.add_child(folium.Popup(iframe,max_width=100))
          count += 1
    if selected_field_level_val == False or selected_field_level_val == 'none':
      if selected_pixel_level_val != 'none':
        m = get_pixel_data_from_tif(selected_order_val,selected_date,selected_pixel_level_val,list_result)
        m = set_range_legend(m,False,selected_order_val,selected_date,selected_pixel_level_val)

    m = m._repr_html_()
       
    return HttpResponse(m)
    
  

def set_range_legend(m,field_level,order,date,pixel_level):
    if field_level:
        if field_level =='vegetation_cover':
            if order == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
              if date == '20221225':
                 m = add_categorical_legend(m, 'Field: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['90.90', '92.50','94.10','95.70','97.30','98.90'])
                        
                 return m
              else:
                 m = add_categorical_legend(m, 'Field: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['87.40', '89.64','91.88','94.12','96.36','98.60'])
                        
                 return m
            elif order == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
                  m = add_categorical_legend(m, 'Field: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['65.00', '65.74','66.48','67.22','67.96','68.70'])
                        
                  return m
            else:
                if date == '20221224' or date == '20221225':
                  m = add_categorical_legend(m, 'Field: Vegetation Cover (%)',
                             colors = ['#800000'],
                             labels = ['25.30'])
                else:
                  m = add_categorical_legend(m, 'Field: Vegetation Cover (%)',
                             colors = ['#800000'],
                             labels = ['27.30'])
                        
                return m
        elif field_level == 'actual_evapotranspiration':
            if order == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
              if date == '20221224':
                 m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['1.00','1.04','1.08','1.12','1.16','1.20'])
                 return m
              elif date == '20221225':
                 m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['1.00','1.04','1.08','1.12','1.16','1.20'])
                 return m
              else:
                 m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#C70039'],
                             labels = ['0.90'])
                 return m
            elif order == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
               if date == '20221223':
                  m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['2.90','2.96','3.02','3.08','3.14','3.20'])
                  return m
               elif date == '20221224':
                  m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['2.80','2.96','3.12','3.28','3.44','3.60'])
                  return m
               else:
                   m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['3.40','3.46','3.52','3.58','3.64','3.70'])
                   return m

            else:
                 if date == '20221224':
                   m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000'],
                             labels = ['2.90'])
                 else:
                    m = add_categorical_legend(m, 'Field: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000'],
                             labels = ['3.10'])
                 return m
        elif field_level == 'irrigation_amount_cumulative':
             if order == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
                if date == '20221223' or date == '20221224':
                    m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['71.06','71.60','72.14','72.69','73.23','73.77'])
                    return m 
                else:
                      m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['77.96','78.52','79.08','79.63','80.19','80.75'])
                      return m 
             elif order == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
                if date == '20221223':
                     m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000'],
                             labels = ['112.46'])
                     return m 
                elif date == '20221224':
                      m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000'],
                             labels = ['113.35'])
                      return m 
                else:
                   m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000'],
                             labels = ['117.35'])
                   return m 
             else:
               if date == '20221223':
                   m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['64.82','65.96','67.10','68.23','69.37','70.51'])
                   return m 
               elif date == '20221224':
                    m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['65.82','67.24','68.66','70.09','71.51','72.93'])
                    return m 
               else:
                  m = add_categorical_legend(m, 'Field: Applied Water Cumulative (mm)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['76.87','78.34','79.81','81.27','82.74','84.21'])
                  return m 
        else:
            return m
    if pixel_level or pixel_level != 'none':
      if pixel_level == 'moisture_status': 
        if order == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
             m = add_categorical_legend(m, 'Pixel: Moisture status',
                             colors = ['#d22e05','#f5ab21','#208528','#30129f','#c5b221'],
                             labels = ['Dry','Stressed','Adequate','Wet','Sparse vegetation'])
             return m 
        elif order == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
           m = add_categorical_legend(m, 'Pixel: Moisture status',
                             colors = ['#d22e05','#f5ab21','#208528','#30129f','#c5b221'],
                             labels = ['Dry','Stressed','Adequate','Wet','Sparse vegetation'])
           return m 
        else:
           m = add_categorical_legend(m, 'Pixel: Moisture status',
                             colors = ['#d22e05','#f5ab21','#208528','#30129f','#c5b221'],
                             labels = ['Dry','Stressed','Adequate','Wet','Sparse vegetation'])
           return m 
      elif pixel_level == 'vegetation_cover': 
        if order == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
          if date == '20221223' or date == '20221224':
             m = add_categorical_legend(m, 'Pixel: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['34.70','47.56','60.42','73.28','86.14','99.00'])
             return m 
          else:
            m = add_categorical_legend(m, 'Pixel: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['45.30','56.04','66.78','77.52','88.26','99.00'])
            return m 
        elif order == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
             m = add_categorical_legend(m, 'Pixel: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['32.90','45.72','58.54','71.36','84.18','97.00'])
             return m 
        else:
          if date == '20221223':
             m = add_categorical_legend(m, 'Pixel: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['16.20','21.74','27.28','32.82','38.36','43.90'])
             return m 
          elif date == '20221224':
              m = add_categorical_legend(m, 'Pixel: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['12.30','20.06','27.82','35.58','43.34','51.10'])
              return m 
          else:
             m = add_categorical_legend(m, 'Pixel: Vegetation Cover (%)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['12.30','20.06','27.82','35.58','43.34','51.10'])
             return m   
      else:
        if order == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
          if date == '20221223':
             m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['0.40','0.60','0.80','1.00','1.20','1.40'])
             return m  
          elif date == '20221224':
             m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['0.50','0.74','0.98','1.22','1.46','1.70'])
             return m  
          else:
             m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['0.60','0.86','1.12','1.38','1.64','1.90'])
             return m  
        elif order == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
          if date == '20221223':
            m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['1.80','2.28','2.76','3.24','3.72','4.20'])
            return m  
          elif date == '20221224':
             m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['2.00','2.52','3.04','3.56','4.08','4.60'])
             return m 
          else:
              m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['2.20','2.64','3.08','3.52','3.96','4.40'])
              return m 
        else:
          if date == '20221223':
             m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['1.80','2.34','2.88','3.42','3.96','4.50'])
             return m 
          elif date == '20221224':
             m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['1.00','1.92','2.84','3.76','4.68','5.60'])
             return m
          else:
             m = add_categorical_legend(m, 'Pixel: Actual Evapotranspiration (mm/d)',
                             colors = ['#800000','#FFA500','#FFE5B4','#E2E6A9','#B4D9EC','#9D5BB5'],
                             labels = ['1.40','2.38','3.36','4.34','5.32','6.30'])
             return m


def change_field_level_color(field_level,field_uuid,api_field_level_data,selected_order_value,date):
    if field_level:
       
       field_dict = {api_field_level_data[0][i]: api_field_level_data[1][i] for i in range(len(api_field_level_data[0]))}
       value_data = field_dict.get(field_uuid)           
       if field_level=='vegetation_cover':
          if selected_order_value == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
            if date == '20221225':
              if value_data == 90.90:
                 style_function =  {
                "fillColor": "#800000",
                'fillOpacity': 3
               }
              elif value_data == 98.90:
                 style_function =  {
                "fillColor": "#9D5BB5",
                'fillOpacity': 3
                }
            else:
              if value_data >= 98.60:
               style_function =  {
                "fillColor": "#9D5BB5",
                'fillOpacity': 3
               }
              elif value_data >= 96.36 and value_data < 98.60:
                style_function =  {
                "fillColor": "#B4D9EC",
                'fillOpacity': 3
                }
              elif value_data >= 94.12 and value_data < 96.36:
               style_function =  {
               "fillColor": "#E2E6A9",
               'fillOpacity': 3
              }
              elif value_data >= 91.88 and value_data < 94.12:
               style_function =  {
               "fillColor": "#FFE5B4",
               'fillOpacity': 3
              }
              elif value_data >= 89.64 and value_data < 91.88:
               style_function =  {
               "fillColor": "#FFA500",
               'fillOpacity': 3
              }
              elif value_data >= 87.40 and value_data < 89.64:
               style_function =  {
               "fillColor": "#800000",
               'fillOpacity': 3
              }
          elif selected_order_value == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
            if value_data == 65.00:
                style_function =  {
               "fillColor": "#800000",
               'fillOpacity': 3
                 } 
            else:
               style_function =  {
               "fillColor": "#9D5BB5",
               'fillOpacity': 3
                 } 
          else:
            if value_data == 25.30:
                  style_function =  {
               "fillColor": "#800000",
               'fillOpacity': 3
                 } 
            else:
                style_function =  {
               "fillColor": "#800000",
               'fillOpacity': 3
               } 
       elif field_level=='actual_evapotranspiration':
         if selected_order_value == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
            if date == '20221224':
                if value_data == 1.00:
                    style_function =  {
                        "fillColor": "#800000",
                         'fillOpacity': 3
                    }
                elif value_data == 1.04:
                     style_function =  {
                        "fillColor": "#FFA500",
                         'fillOpacity': 3
                    }
                elif value_data == 1.08:
                     style_function =  {
                        "fillColor": "#FFE5B4",
                         'fillOpacity': 3
                    }
                elif value_data == 1.12:
                    style_function =  {
                        "fillColor": "#E2E6A9",
                         'fillOpacity': 3
                    }
                elif value_data == 1.16:
                     style_function =  {
                        "fillColor": "#B4D9EC",
                         'fillOpacity': 3
                    }
                elif value_data == 1.20:
                      style_function =  {
                        "fillColor": "#9D5BB5",
                         'fillOpacity': 3
                    }
            elif date == '20221225':
                if value_data == 1.00:
                    style_function =  {
                        "fillColor": "#800000",
                         'fillOpacity': 3
                    }
                elif value_data == 1.04:
                     style_function =  {
                        "fillColor": "#FFA500",
                         'fillOpacity': 3
                    }
                elif value_data == 1.08:
                     style_function =  {
                        "fillColor": "#FFE5B4",
                         'fillOpacity': 3
                    }
                elif value_data == 1.12:
                    style_function =  {
                        "fillColor": "#E2E6A9",
                         'fillOpacity': 3
                    }
                elif value_data == 1.16:
                     style_function =  {
                        "fillColor": "#B4D9EC",
                         'fillOpacity': 3
                    }
                elif value_data == 1.20:
                      style_function =  {
                        "fillColor": "#9D5BB5",
                         'fillOpacity': 3
                    }
            else:
                 style_function =  {
                 "fillColor": "#C70039",
                 'fillOpacity': 3
              }
         elif selected_order_value == '6809fe46-5bfc-4c5c-8e90-b267c705be2e':
           if date == '20221223':
                if value_data == 2.90:
                     style_function =  {
                       "fillColor": "#800000",
                        'fillOpacity': 3
                     } 
                else:
                     style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
           elif date == '20221224':
                if value_data == 2.80:
                  style_function =  {
                       "fillColor": "#800000",
                        'fillOpacity': 3
                     } 
                else:
                  style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
           else:
              if value_data == 3.40:
                 style_function =  {
                       "fillColor": "#800000",
                        'fillOpacity': 3
                     } 
              else:
                 style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
         else:
            style_function =  {
               "fillColor": "#800000",
               'fillOpacity': 3
              } 
       elif field_level == 'irrigation_amount_cumulative':
          if selected_order_value == '6f32f9ce-5266-4d68-b6f1-b314e31a071f':
            if date == '20221223' or date == '20221224':
              if value_data == 71.06:
                 style_function =  {
                       "fillColor": "#800000",
                        'fillOpacity': 3
                     } 
              else:
                 style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
            else:
              if value_data == 77.96:
                style_function =  {
                       "fillColor": "#800000",
                        'fillOpacity': 3
                     } 
              else:
                 style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
          elif selected_order_value == '30fc75c3-a68e-4ba3-95a0-a9bf3e6d2c4f':
                  style_function =  {
                        "fillColor": "#800000",
                         'fillOpacity': 3
                    }
          else:
            if date == '20221223':
              if value_data == 64.82:
                 style_function =  {
                        "fillColor": "#800000",
                         'fillOpacity': 3
                    }
              else:
                 style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
            elif date == '20221224':
              if value_data == 65.82:
                 style_function =  {
                        "fillColor": "#800000",
                         'fillOpacity': 3
                    }
              else:
                 style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
            else:
              if value_data == 76.87:
                style_function =  {
                        "fillColor": "#800000",
                         'fillOpacity': 3
                    }
              else:
                 style_function =  {
                       "fillColor": "#9D5BB5",
                        'fillOpacity': 3
                     } 
       else:
            style_function =  {
             "fillColor": "#D3D3D3",
            }
       return style_function

