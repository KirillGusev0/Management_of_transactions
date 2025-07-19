from django.shortcuts import render, redirect
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import logging


@main_auth(on_cookies = True)
def add_deal(request):
    logger = logging.getLogger(__name__)  # for debug
    logger.warning(" Зашли в add_deal")
    logger.warning(f" bitrix_user_token: {getattr(request, 'bitrix_user_token', None)}")
    logger.warning(f" bitrix_user: {getattr(request, 'bitrix_user', None)}")
    logger.warning(f" COOKIES: {request.COOKIES}")
    # end debug
    if request.method == 'POST':
        stage_id = request.POST.get('stage_id')
        title= request.POST.get('title')
        opportunity = request.POST.get('opportunity')
        begindate = request.POST.get('begindate')
        closedate= request.POST.get('closedate')
        address = request.POST.get('address')
        fields = {
        'STAGE_ID': stage_id,
        'TITLE': title,
        'OPPORTUNITY': opportunity,
        'BEGINDATE': begindate,
        'CLOSEDATE': closedate,
        'UF_CRM_1752935615': address,
        }
        but = request.bitrix_user_token
        but.call_api_method('crm.deal.add', {'fields': fields})
        return redirect('active_deals')
    return render(request, 'add_mode.html')