from dash_canvas import DashCanvas
import datetime
import base64
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dropbox
import cv2
from matplotlib import pyplot as plt
from urllib.request import urlopen
import numpy as np
import pandas as pd
import dash_table
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
from dash_extensions import Download
import dash_bootstrap_components as dbc
col=['Grade1','Grade2','Grade3']
dbx = dropbox.Dropbox('5uSdWA0gd2UAAAAAAAAAAauPVaO_t_nlwRgP3YzwZ8-2HlxYFWRLUrmTAgk4F4b7')
for entry in dbx.files_list_folder('/Diabetci Foot').entries:
            aa=entry.name
            if aa=='TestResult.csv':
                dbx.files_delete_v2('/Diabetci Foot/TestResult.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': 'LightSalmon',
    'text': '#7FDBFF'
}
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
                    html.H1("XYZ Diabetic Foot Screening System",style={'font-size': '50px','font-family':'Times New Roman','color':'black'}),
                         ], 
                    style = {'padding' : '50px',
                             'textAlign': 'center'}),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '99%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'color':'white',
            'backgroundColor': '#00308F',
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div(id='output-image-upload'),
         html.Div([
    html.Button('Start Process', id='btn-nclicks-1', style={'backgroundColor': '#00308F',
                                                             'color':'white','width':'15%', 'border':'1px black solid',
                                                             'height': '40px','textalign':'center', 'marginLeft': '2px', 'marginTop': 0,
                                                             'font-size': '15px','font-family':'Courier New','borderStyle': 'groove'},n_clicks=0),
    html.Button('Show Process Data', id='btn-nclicks-2',style={'backgroundColor': '#00308F',
                                                             'color':'white','width':'15%', 'border':'1px black solid',
                                                             'height': '40px','textalign':'center', 'marginLeft': '2px', 'marginTop':0,
                                                             'font-size': '15px','font-family':'Courier New','borderStyle': 'groove'},n_clicks=0)]),
    html.Div(id='container-button-timestamp'),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in col],
    style_header={'backgroundColor': '#8C4500'},
                           style_cell={
                               'backgroundColor': '#DC143C',
                                'color': 'Black',
                                 'textAlign': 'center'}),
    html.Div([
    html.Div([dcc.Graph(
        id='plot',style={'backgroundColor': '#00308F'})],className='six columns'),
    html.Hr(),
    html.Div([html.H2('Biological Vision Result and Doctor Validation',style={'font-size': '20px','font-family':'Times New Roman','color':'black'}),
              html.H3('Note : Select Result (only for Doctors)',style={'font-size': '18px','font-family':'Times New Roman','color':'black'}),
        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Grade1', 'value': 'Grade1'},
            {'label': 'Grade2', 'value': 'Garde1'},
            {'label': 'Grade3', 'value': 'Grade1'},                       
        ],
        placeholder="Select Answer",
                            style = dict(
                            width = '80%',
                            display = 'inline-block',
                            verticalAlign = "middle"
                            ))],
    className='six columns'),
    html.Div([html.Div(id='dd-output-container')],className='six columns'),
     html.Div([html.P("This Part Is only for dotor's",
            style={'font-size': '18px','font-family':'Times New Roman','color':'black','text-align':'justify'})])],
    className='row'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2('For Download Report fill this informtion'),
    html.Div([html.Div([html.P('Note : Name , Mobile and All Red filled Requied',style={'font-size': '50x','font-family':'Times New Roman','color':'red','font-weight': 'bold','font-style': 'italic'}),
    html.Div('Patinet Name       : ',style={'display': 'inline-block'}),
               dcc.Input(id="user", type="text", placeholder="Enter Name",className="inputbox1",required=True,
                           style={'display': 'inline-block','margin-left':'80px','width':'49%',
                                'font-size':'16px','border-width':'3px','border-color':'black'}),
    html.Br(),
    html.Br(),
    html.Div('Mobile Number       : ',style={'display': 'inline-block'}),
               dcc.Input(id="user1", type="text", placeholder="Enter Mobile Number",className="inputbox1",required=True,
                           style={'display': 'inline-block','margin-left':'71px','width':'49%',
                                'font-size':'16px','border-width':'3px','border-color':'black'}),
    html.Br(),
    html.Br(),
    html.Div('Patient Gender      : ',style={'display': 'inline-block'}),
               dcc.Input(id="user2", type="text", placeholder="Enter Gender",className="inputbox1",required=True,
                           style={'display': 'inline-block','margin-left':'73px','width':'49%',
                                'font-size':'16px','border-width':'3px','border-color':'black'}),
    html.Br(),
    html.Br(),
    html.Div('Patient Age      : ',style={'display': 'inline-block'}),
               dcc.Input(id="user3", type="number", placeholder="Enter Age",className="inputbox1",required=True,
                           style={'display': 'inline-block','margin-left':'95px','width':'49%',
                                'font-size':'16px','border-width':'3px','border-color':'black'}),
    html.Br(),
    html.Br(),
        html.Div("Test Date      : ",style={'display': 'inline-block'}),
               dcc.Input(id="user4", type="date", placeholder="Enter Date",className="inputbox1",required=True,
                           style={'display': 'inline-block','margin-left':'107px','width':'49%',
                                'font-size':'16px','border-width':'3px','border-color':'black'}),
    html.Br(),
    html.Br(),
        html.Div("Doctor 's Name      : ",style={'display': 'inline-block'}),
               dcc.Input(id="user5", type="text", placeholder="Enter Doctor's Name",className="inputbox1",required=True,
                           style={'display': 'inline-block','margin-left':'70px','width':'49%',
                                'font-size':'16px','border-width':'3px','border-color':'black'}), 
    html.H1('        '),
         html.Button('Submit', id='btn-nclicks-3',style={'backgroundColor': '#00308F',
                                                             'color':'white','width':'99%', 'border':'1px black solid',
                                                             'height': '40px','textalign':'center', 'marginLeft': '2px', 'marginTop': 0,
                                                             'font-size': '15px','font-family':'Courier New','borderStyle': 'groove'}, n_clicks=0),
         ],style={"border":"3px black solid"},
               className='six columns'),
html.Div([html.P('Diabetic Foot System',style={'font-size': '30x','font-family':'Times New Roman','color':'black'}),
                html.Div(id='textareaoutput', style={'whiteSpace': 'pre-line'})],className='four columns'),],style={"border":"3px black solid"},className='row'),
    html.Br(),
    html.Br(),
    html.Button('Process', id='btn-nclicks-4',style={'backgroundColor': '#00308F',
                                                             'color':'white','width':'99%', 'border':'1px black solid',
                                                             'height': '40px','textalign':'center', 'marginLeft': '2px', 'marginTop': 0,
                                                             'font-size': '15px','font-family':'Courier New','borderStyle': 'groove'}, n_clicks=0),
    html.Div("After Click On Process Click On Download"),
    html.Button('Download', id='btn-nclicks-5',style={'backgroundColor': '#00308F',
                                                             'color':'white','width':'99%', 'border':'1px black solid',
                                                             'height': '40px','textalign':'center', 'marginLeft': '2px', 'marginTop': 0,
                                                             'font-size': '15px','font-family':'Courier New','borderStyle': 'groove'}, n_clicks=0),
    html.Div(id='containers-button-timestamp'),
    html.Div(id='containers-buttons-timestamp'),
    html.Footer(html.P('XYZ Diabetic Foot Testing System',style={'font-size': '30px','font-family':'Times New Roman','color':'black','textAlign':'center'})),
    
    
])
def parse_contents(contents, filename, date):
    dbx.files_delete_v2('/Diabetci Foot/IMAGE.png')
    content_type, content_string = contents.split(',')
    base64_img_bytes = content_string.encode('utf-8')
##    with open('decoded_image.png', 'wb') as file_to_save:
    decoded_image_data = base64.decodebytes(base64_img_bytes)
        #file_to_save.write(decoded_image_data,format="PNG")
    dbx.files_upload(
                decoded_image_data,'/Diabetci Foot/IMAGE.png', dropbox.files.WriteMode.overwrite,
                mute=True)
    return html.Div([
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents,width="200",height="200"),
        html.H5("Test Image"),
        html.Hr(),
        #html.Div('Raw Content'),
        ])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
@app.callback(Output('container-button-timestamp', 'children'),
              Input('btn-nclicks-1', 'n_clicks'))
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        msg='Process is Going on'
        for entry in dbx.files_list_folder('/Diabetci Foot').entries:
            aa=entry.name
            if aa=='IMAGE.png':
                bb=entry.id
                resultresult =dbx.files_get_temporary_link(bb)
                cc=resultresult.link
        print(cc)
        url_response = urlopen(cc)
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
        h,w,c=img.shape
        center_coordinates = (int(w/2),int(h/2))
        radius = int(w*15/100)
        x=int(center_coordinates[0]-radius)
        y=int(center_coordinates[1]-radius)
        print(x)
        rop_image = img[int(y):int(y+1.5*radius),int(x):int(x+2*radius)]
        grayimg = cv2.cvtColor(rop_image, cv2.COLOR_BGR2GRAY)
        Gaussian_Iamge = cv2.GaussianBlur(grayimg,(5,5),0)
        edges = cv2.Canny(Gaussian_Iamge,30,30)
        df = pd.DataFrame(edges/255)
        Descibe_Data=df.describe()
        df1=Descibe_Data.mean(axis=1)
        med1=df1.iloc[1:len(df1)].mean(axis=0)
        df2=Descibe_Data.median(axis=1)
        med2=df2.iloc[1:len(df2)].mean(axis=0)
        df3=Descibe_Data.std(axis=1)
        med3=df3.iloc[1:len(df3)].mean(axis=0)
        _, res = dbx.files_download("/Diabetci Foot/Grade1.csv")
        with io.BytesIO(res.content) as stream:
            df4Grade1 = pd.read_csv(stream)
        _, res = dbx.files_download("/Diabetci Foot/Grade2.csv")
        with io.BytesIO(res.content) as stream:
            df5Grade2 = pd.read_csv(stream)
        _, res = dbx.files_download("/Diabetci Foot/Grade3.csv")
        with io.BytesIO(res.content) as stream:
            df6Grade3 = pd.read_csv(stream)
        data_point_Grade1=np.array([df4Grade1['Mean'],df4Grade1['Median']])
        data_point_Grade2=np.array([df5Grade2['Mean'],df5Grade2['Median']])
        data_point_Grade3=np.array([df6Grade3['Mean'],df6Grade3['Median']])
        print(data_point_Grade3)
        daat_point_test_image=np.array([round(med1,4),round(med2,4)])
        Euclidean_distance_Grade1 = round(np.linalg.norm(data_point_Grade1 - daat_point_test_image),4)
        Euclidean_distance_Grade2 = round(np.linalg.norm(data_point_Grade2 - daat_point_test_image),4)
        Euclidean_distance_Grade3 = round(np.linalg.norm(data_point_Grade3- daat_point_test_image),4)
        list9=[str("Grade1"),str("Grade2"),str("Grade3")]
        list8=[Euclidean_distance_Grade1, Euclidean_distance_Grade2,Euclidean_distance_Grade3]
        percent_1=(list8[0])/(sum(list8))
        percent_2= (list8[1])/(sum(list8))
        percent_3 =(list8[2])/(sum(list8))
        list10=[round(100-(percent_1*100),2),round(100-(percent_2*100),2),round(100-(percent_3*100),2)]
        new_data=pd.DataFrame({'Grade1' : [list10[0]],
                                   'Grade2' : [list10[1]],
                                         "Grade3" : [list10[2]]}, 
                                  columns=['Grade1', 'Grade2','Grade3'])
        data = new_data.to_csv(index=False) # The index parameter is optional
        with io.BytesIO(data.encode()) as stream:
            stream.seek(0)
            dbx.files_upload(stream.read(), "/Diabetci Foot/TestResult.csv", mode=dropbox.files.WriteMode.overwrite)
        msg="Process IS Complete"
    else:
        msg = 'Button has not been yet Clicked'
    return html.Div(msg)
@app.callback(Output('table', 'data'),
              Input('btn-nclicks-2', 'n_clicks')
)
def displayClick(btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-2' in changed_id:
        for entry in dbx.files_list_folder('/Diabetci Foot').entries:
            aa=entry.name
            if aa=='TestResult.csv':
                bb=entry.id
                resultresult =dbx.files_get_temporary_link(bb)
                cc=resultresult.link
        df=pd.read_csv(cc)
        data=df.to_dict('records')
        return data
@app.callback(Output('plot', 'figure'),
              Input('btn-nclicks-2', 'n_clicks')
)
def updates_charts(btn2):
    for entry in dbx.files_list_folder('/Diabetci Foot').entries:
            aa=entry.name
            if aa=='TestResult.csv':
                bb=entry.id
                resultresult =dbx.files_get_temporary_link(bb)
                cc=resultresult.link
    df=pd.read_csv(cc)
    y1=df['Grade1'].to_list()
    y2=df['Grade2'].to_list()
    y3=df['Grade3'].to_list()
    x1=['Grade1','Grade2','Grade3']
    y4=[*y1,*y2,*y3]
    fig = go.Figure([go.Bar(x=x1, y=y4,text=y4,marker=dict(color= "rgb(255, 127, 14)"),textposition='auto')])
    fig.layout.plot_bgcolor = '#0A061C'
    fig.layout.paper_bgcolor = '#0A061C '
    fig.update_geos(
    projection_type="orthographic",
    landcolor="white",
    oceancolor="MidnightBlue",
    showocean=True,
    lakecolor="LightBlue"
    )
    fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[
        dict(
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
    )
    fig.update_layout(title_text="Result Data Diabetic Foot")
    return fig


@app.callback(
    Output('textareaoutput', 'children'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('user', 'value'),
    Input('user1','value'),
    Input('user2','value'),
    Input('user3','value'),
    Input('user4','value'),
    Input('user5','value'),
)
def update_output(btn3,user,user1,user2,user3,user4,user5):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-3' in changed_id:
        if user==None:
            return 'Enter Name In Filled'
        elif user1==None:
            return 'Enter Mobile In Filled'
        elif user2==None:
            return 'Enter Gender In Filled'
        elif user3==None:
            return 'Enetr Age in Filled'
        elif user4==None:
            return "Enter Doctor's Detail In Filled"
        elif user5==None:
            return "Enter Test Date In Filled"
        else:
            res=[]
            list1=["Name","Mobile Number","Gender","Age","Test Date","Doctor's Name"]
            list2=[user,user1,user2,user3,user4,user5]
            res1 = dict(zip(list2,list1))
            df=pd.DataFrame([list2],columns=list1)
            data = df.to_csv(index=False)
            for j in range(0,len(list1)):
                res.append(list1[j]+str("  ")+str(":")+str('  ')+str(list2[j]))
            text1 = str(res[0])+str('\n')+str(res[1])+str('\n')+str(res[2])+str('\n')+str(res[3])+str('\n')+str(res[4])+str('\n')+str(res[5])+str("\n")
            with io.BytesIO(data.encode()) as stream:
                stream.seek(0)
                dbx.files_upload(stream.read(), "/Diabetci Foot/Pdfdata.csv", mode=dropbox.files.WriteMode.overwrite)
            return 'You have entered: \n{}'.format(text1)
@app.callback(Output('containers-button-timestamp', 'children'),
              Input('btn-nclicks-4', 'n_clicks'))
def displayClick(btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-4' in changed_id:
        cc=[]
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()
        pdf.rect(10,5,190,287,'D')
        pdf.set_font('times', 'B', 20)
        pdf.set_text_color(0,0,0)
        pdf.image('screen-0.jpg', x = 15, y = 10, w = 100, h = 80,type = '')
        pdf.cell(0,50, 'XYZ Diabetic Foot Medical Report', 0, 0,'R')
        pdf.set_font('times', '', 12)
        pdf.ln(50)
        pdf.cell(5)
        pdf.cell(180,0,'',1,0,'C')
        for entry in dbx.files_list_folder('/Diabetci Foot').entries:
            aa=entry.name
            if aa=='Pdfdata.csv':
                bb=entry.id
                resultresult =dbx.files_get_temporary_link(bb)
                cc=resultresult.link
        if cc!=[]:
            df=pd.read_csv(cc)
            namelist=[]
            valuelist=[];
            total=[]
            totallist=[]
            kk=1;
            for j in df:
                list1=df[j].astype(str).tolist()
                namelist.append(j)
                valuelist.append(*list1)
                total=[j,*list1]
                totallist.append(total)
            epw = pdf.w - 2*pdf.l_margin
            col_width = epw/4
            data = totallist[0:5]
            pdf.ln(5)
            pdf.set_font('Times','B',14.0) 
            pdf.cell(epw, 0.0, 'Basic Information', align='C')
            pdf.set_font('Times','',10.0) 
            pdf.ln(0.5)
            th = pdf.font_size
            pdf.ln(2*th)
            for row in data:
                pdf.cell(5)
                for datum in row:
                         pdf.set_font('Times','B',10.0)
                         pdf.cell(col_width+42, 2*th, str(datum), border=1,align='C')
             
                pdf.ln(2*th)
            pdf.ln(5)
            pdf.cell(5)
            pdf.cell(180,0,'',1,0,'C')
            for entry in dbx.files_list_folder('/Diabetci Foot').entries:
                aa=entry.name
                if aa=='IMAGE.png':
                    bb=entry.id
                    resultresult =dbx.files_get_temporary_link(bb)
                    ccc=resultresult.link
            url_response = urlopen(ccc)
            img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
            pdf.image(ccc,50,120,100,80,'PNG')
            pdf.ln(60)
            pdf.cell(5)
            for entry in dbx.files_list_folder('/Diabetci Foot').entries:
                aa=entry.name
                if aa=='TestResult.csv':
                    bb=entry.id
                    resultresult =dbx.files_get_temporary_link(bb)
                    ccd=resultresult.link
            df=pd.read_csv(ccd)
            a=[df['Grade1'][0],df['Grade2'][0],df['Grade3'][0]]
            b=max(a)
            c=a.index(b)
            print(c)
            if c==0:
                stri1=[str('Grade1'),str(b)]
            if c==1:
                stri1=[str('Grade2'),str(b)]
            if c==2:
                stri1=[str('Grade1'),str(b)]
            pdf.ln(50)
            epw = pdf.w - 2*pdf.l_margin
            col_width = epw/4
            data = [stri1]
            pdf.ln(5)
            pdf.set_font('Times','B',14.0) 
            pdf.cell(epw, 0.0, 'Diabetic Foot Issue', align='C')
            pdf.set_font('Times','',10.0) 
            pdf.ln(0.5)
            th = pdf.font_size
            pdf.ln(2*th)
            for row in data:
                pdf.cell(5)
                for datum in row:
                         pdf.set_font('Times','B',10.0)
                         pdf.cell(col_width+42, 2*th, str(datum), border=1,align='C')
             
                pdf.ln(2*th)
            pdf.ln(5)
            pdf.cell(0,10,str(valuelist[5]),0,0,'R')
            pdf.ln(3)
            pdf.cell(0,10,'contact Information',0,0,'R')
            pdf.cell(5)
            pdf.cell(180,0,'',1,0,'C')
            pname= str('/')+str('Diabetci Foot')+str('/')+str(valuelist[0])+str(' ')+str('Medical Report')+str(' ')+str(valuelist[4])+str('.pdf')
            dbx.files_upload(
                        pdf.output(dest='S').encode('latin-1'),pname,mode=dropbox.files.WriteMode.overwrite)
            return dbc.Alert('Click on Download Download',style={'font-size': '30px','font-family':'Arial Black','color':'black'},duration=4000)
        else:
            return 'Try Again'
@app.callback(Output('containers-buttons-timestamp', 'children'),
              Input('btn-nclicks-5', 'n_clicks'))
def displayClick(btn5):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-5' in changed_id:
        cc=[]
        for entry in dbx.files_list_folder('/Diabetci Foot').entries:
            aa=entry.name
            if aa=='Pdfdata.csv':
                bb=entry.id
                resultresult =dbx.files_get_temporary_link(bb)
                cc=resultresult.link
        if cc!=[]:
            df=pd.read_csv(cc)
            valuelist=[]
            for j in df:
                list1=df[j].astype(str).tolist()
                valuelist.append(*list1)
            
            for entry in dbx.files_list_folder('').entries:
                aae=entry.name
                if aae=='Diabetci Foot':
                    bbe=entry.id
                    resultresulte =dbx.files_get_temporary_link('/Diabetci Foot/'+str(valuelist[0])+str(' ')+str('Medical Report')+str(' ')+str(valuelist[4])+str('.pdf'))
                    cce=resultresulte.link
            return dbc.Alert(html.A('Go to Download',style={'font-size': '30px','font-family':'Arial Black','color':'black'},href=cce,target="_blank"),duration=4000)
        else:
            return 'Try Again'
                    

if __name__ == '__main__':
    app.run_server(debug=False)
    
    
