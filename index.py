import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import no_update

import pandas as pd
import numpy as np
import sqlite3
import os
from datetime import date

from app import app,server


app.layout = html.Div(dbc.Container(
    [
        # header
        dbc.Row(
            dbc.Col(
                [
                    html.H5('Upper Columbia RV Park')
                ],
            ),
            justify='center',
            style = dict(width='100%',background='lightGrey',height='65px')
        ),

        html.Br(),

        # content
        dbc.Row(
            dbc.Col(
                [
                    dbc.Card(
                        [
                            html.H3('Maintenance Update',className='card-title'),
                            dbc.Alert(
                                'Item(s) submitted successfully!',
                                id='input-success-alert',
                                is_open=False,
                                color='success',
                                dismissable=True
                            ),
                            dbc.Alert(
                                'There was a problem submitting that alert...Try again?',
                                id='input-failure-alert',
                                color='danger',
                                is_open=False,
                                dismissable=True
                            ),
                            dbc.Alert(
                                'There were duplicate entries...',
                                id='input-duplicates-alert',
                                is_open=False,
                                color='warning',
                                dismissable=True
                            ),

                            dbc.ListGroup(
                                [
                                    dbc.ListGroupItem(
                                        dbc.Row(
                                            [
                                                # site number
                                                dbc.Col(
                                                    [
                                                        html.H5('Site Number',className='card-subtitle'),
                                                        dcc.Dropdown(
                                                            id='site-dropdown',
                                                            options = [
                                                                dict(label=i,value=i)
                                                                for i in range(1,25)
                                                            ],
                                                            multi=True,
                                                        )
                                                    ],
                                                    width=3
                                                ),

                                                # date
                                                dbc.Col(
                                                    [
                                                        html.H5('Date',className='card-subtitle'),
                                                        dcc.DatePickerSingle(
                                                            id='date-input',
                                                            initial_visible_month=date.today(),
                                                            date=date.today(),
                                                            display_format='YYYY MMM DD'
                                                        )
                                                    ],
                                                    width=3
                                                ),

                                                # action multi
                                                dbc.Col(
                                                    [
                                                        html.H5('Action',className='card-subtitle'),
                                                        dcc.Dropdown(
                                                            id='action-dropdown',
                                                            options=[
                                                                dict(label=x,value=x)
                                                                for x in ('Cleanup','Mow','Landscape','Other')
                                                            ],
                                                            multi=True,
                                                        ),
                                                        dbc.Input(
                                                            placeholder='Other description',
                                                            style=dict(maxWidth='250px'),
                                                            disabled=True,
                                                            id='other-input'
                                                        )
                                                    ],
                                                    width=3
                                                ),

                                                # person
                                                dbc.Col(
                                                    [
                                                        html.H5('Person',className='card-subtitle'),
                                                        dcc.Dropdown(
                                                            id='person-dropdown',
                                                            options=[
                                                                dict(label=x,value=x)
                                                                for x in ('Ralph', 'Other')
                                                            ]
                                                        )
                                                    ]
                                                )

                                            ]
                                        )
                                    )
                                ]
                            ),
                            dbc.Button(
                                'Submit item',
                                id='submit-input-button',
                                color='primary',
                                block=True,
                                disabled=True,
                                n_clicks=0
                            )
                        ],
                        body=True
                    ), # end of the card

                    html.Br(),

                    # reports?
                    dbc.Card(
                        [
                            # report input
                            html.H3('Reports',className='card-title'),

                            dbc.Alert(
                                'No values matched those values, try again...',
                                id='report-alert',
                                color='danger',
                                is_open=False,
                                dismissable=True
                            ),
                            
                            html.Br(),

                            dbc.ListGroup(
                                [
                                    dbc.ListGroupItem(
                                        dbc.Row(
                                            [
                                                # site number
                                                dbc.Col(
                                                    [
                                                        html.H5('Site Number',className='card-subtitle'),
                                                        dcc.Dropdown(
                                                            id='report-sites',
                                                            options = [
                                                                dict(label=i,value=i)
                                                                for i in range(1,25)
                                                            ],
                                                            multi=True,
                                                        )
                                                    ],
                                                    width=3
                                                ),

                                                # date
                                                dbc.Col(
                                                    [
                                                        html.H5('Date',className='card-subtitle'),
                                                        dcc.DatePickerSingle(
                                                            id='report-date',
                                                            initial_visible_month=date.today(),
                                                            display_format='YYYY MMM DD'
                                                        )
                                                    ],
                                                    width=3
                                                ),

                                                # action multi
                                                dbc.Col(
                                                    [
                                                        html.H5('Action',className='card-subtitle'),
                                                        dcc.Dropdown(
                                                            id='report-actions',
                                                            options=[
                                                                dict(label=x,value=x)
                                                                for x in ('Cleanup','Mow','Landscape','Other')
                                                            ],
                                                            multi=True,
                                                        ),
                                                        dbc.Input(
                                                            placeholder='Other description',
                                                            style=dict(maxWidth='250px'),
                                                            disabled=True,
                                                            id='report-other-input'
                                                        )
                                                    ],
                                                    width=3
                                                ),

                                                # person
                                                dbc.Col(
                                                    [
                                                        html.H5('Person',className='card-subtitle'),
                                                        dcc.Dropdown(
                                                            id='report-person',
                                                            options=[
                                                                dict(label=x,value=x)
                                                                for x in ('Ralph', 'Other')
                                                            ]
                                                        )
                                                    ]
                                                )

                                            ]
                                        )
                                    )
                                ],
                            ),

                            dbc.Button(
                                'Generate Report',
                                id='report-button',
                                n_clicks=0,
                                color='primary',
                                block=True
                            ),

                            html.Br(),

                            dbc.Card(
                                id='report-output',
                                body=True
                            )
                        ],
                        body=True
                    )
                ]
            )
        ),
    ]
))


# disable the other input
@app.callback(
    Output('other-input','disabled'),
    [Input('action-dropdown','value')]
)
def disable_other(value):
    '''
    if Other is selected in Action, enable the input
    '''
    if not type(value)==list:
        value = [value]
    if 'Other' in value:
        return False
    return True

# disable the other input
@app.callback(
    Output('report-other-input','disabled'),
    [Input('action-dropdown','value')]
)
def disable_report_other(value):
    '''
    if Other is selected in Action, enable the input
    '''
    if not type(value)==list:
        value = [value]
    if 'Other' in value:
        return False
    return True




# enter an item into the database
@app.callback(
    [Output('input-success-alert','is_open'),
     Output('input-failure-alert','is_open'),
     Output('input-failure-alert','children'),
     Output('input-duplicates-alert','is_open'),
     Output('input-duplicates-alert','children')],
    [Input('submit-input-button','n_clicks')],
    [State('site-dropdown','value'),
     State('date-input','date'),
     State('action-dropdown','value'),
     State('person-dropdown','value'),
     State('other-input','value')]
)
def submit_item(n,sites,this_date,actions,person,other_input):
    '''
    when the user pushes the submit button, send some thing to the database
    '''
    if n==0:
        return [no_update for i in range(5)]

    # transform values to lists
    if not type(sites)==list:
        sites = [sites]
    if not type(actions)==list:
        actions = [actions]
    if 'Other' in actions:
        actions[ np.argmax(np.array(actions)=='Other') ] = other_input

    conn = sqlite3.connect('uc.db')

    # track which ones have been done
    all_ = []
    for s,a in zip(sites,actions):
        all_.append([s,this_date,a,person])

    # submit the next
    try:
        # check for duplicate things
        duplicates = []
        done = []
        df = pd.read_sql('select * from uc',conn)
        print('sites',sites)
        for s in sites:
            for a in actions:
                # check for duplicate
                if df[(df.date==this_date) & (df.site==s) & (df.action==a) & (df.person==person)].shape[0]>0:
                    duplicates.append([s,this_date,a,person])
                    all_ = all_[1:]

                # if no duplicate, send to database
                else:
                    
                    conn.cursor().execute('insert into uc (site,date,action,person) values ({},"{}","{}","{}");'.format(s,this_date,a,person))
                    conn.commit()
                    done.append([s,this_date,a,person])
                    all_ = all_[1:]
        show_failure = False
    # error?
    except BaseException as e:
        print(e)
        show_failure = True

    input_success,show_dupe = False, False
    duplicate_children, failure_children = None, None

    # duplicates
    if len(duplicates)>0:
        show_dupe = True
        duplicates = pd.DataFrame(duplicates,columns=['site','date','action','person'])
        duplicates = dbc.Table.from_dataframe(duplicates,striped=True,bordered=True,hover=True)
        duplicate_children = dbc.Card(
            [
                html.H6('Duplicate entries error - everything was submitted except:',className='card-subtitle'),
                html.Br(),
                duplicates,
            ],
            body=True
        )
    if len(all_)>0:
        not_done = pd.DataFrame(all_,columns=['site','date','action','person'])
        not_done = dbc.Table.from_dataframe(not_done,striped=True,bordered=True,hover=True)
        failure_children = dbc.Card(
            [
                html.H6('Something went wrong - these were not submitted',className='card-subtitle'),
                html.Br(),
                not_done
            ]
        )
    if not show_failure:
        input_success = True
    
    conn.close()

    return (
        input_success,
        show_failure,
        failure_children,
        show_dupe,
        duplicate_children
    )

    


# disable item submit button if the reports are all true
@app.callback(
    Output('submit-input-button','disabled'),
    [Input('date-input','date'),
     Input('action-dropdown','value'),
     Input('person-dropdown','value'),
     Input('site-dropdown','value')]
)
def disabled_input_button(this_date,actions,person,sites):
    '''
    if the inputs aren't all ready, don't let them submit yet
    '''
    if this_date==None or actions==None or person==None or sites==None:
        return True
    return False
    




# get a report for an item
@app.callback(
    [Output('report-output','children'),
     Output('report-alert','is_open')],
    [Input('report-button','n_clicks')],
    [State(thing,'value') for thing in ('report-sites','report-person','report-actions')]+\
    [State('report-date','date'),
     State('report-other-input','value')]
)
def reports(n,sites,person,actions,this_date,other_input):
    '''
    get the data
    filter the data
    send the data to the output section
    '''

    if n==0:
        return no_update,no_update

    # transform values to lists
    if not type(sites)==list:
        sites = [sites]
    if not type(actions)==list:
        actions = [actions]
        if type(actions[0])==list:
            actions = actions[0]

    if 'Other' in actions:
        actions[ np.argmax(np.array(actions)=='Other') ] = other_input
    
    conn = sqlite3.connect('uc.db')

    df = pd.read_sql('select * from uc',conn)

    for col,values in zip(['site','date','action','person'],[sites,[this_date],actions,[person]]):
        if None in values or len(values)==0:
            continue
        if df.empty:
            continue
        print(col,values)
        df = df[[x in values for x in df[col]]]

    if df.shape[0]==0:
        return None, True

    table = dbc.Table.from_dataframe(df,striped=True,bordered=True,hover=True)
        
    return table,False





if __name__ == "__main__":
    app.run_server(
        debug=True,
        port=8050
    )