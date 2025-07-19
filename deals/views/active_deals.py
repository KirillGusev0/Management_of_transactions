from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from datetime import datetime
from dateutil import tz

def iso_transform(date):
    date = datetime.fromisoformat(date.replace('Z', '+00:00'))
    dete_moscow = date.astimezone(tz.gettz('Europe/Moscow'))
    return dete_moscow.strftime('%d/%m/%Y')

@main_auth(on_cookies = True)
def active_deals(request):
    but = request.bitrix_user_token
    recent_active = but.call_api_method("crm.deal.list",{
        'filter':{
            'ASSIGNED_BY_ID':request.bitrix_user.id,
            "!@STAGE_ID":["WON","LOSE","APOLOGY"]
        },
        'order':{'BEGINDATE':'Desk'},
        'select':['ID','STAGE_ID','TITLE','OPPORTUNITY','BEGINDATE','CLOSEDATE','UF_CRM_1752935615']
    })['result'][:10]
    for deal in recent_active:
        deal['BEGINDATE'] = iso_transform(deal['BEGINDATE'])
        deal['CLOSEDATE'] = iso_transform(deal['CLOSEDATE'])
    return render(request,'active_mode.html',locals())