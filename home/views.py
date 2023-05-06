from django.shortcuts import render, redirect
from django.http import JsonResponse

from code.astroMatch import MatchMaking, get_person_asthkoot_df, get_asthakoot_base_df

from astromatch.settings import BASE_DIR

# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context=context)

def get_astrology(request):
    response = {}
    if request.POST.get('action') == 'post':
        dob, tob, tz = request.POST.get('dob'), request.POST.get('tob'), request.POST.get('timezone')
        year, month, day = [int(i) for i in dob.split('-')]
        hour, minute = [int(i) for i in tob.split(':')]

        dt_utc = MatchMaking().convert_standard_to_utc_time(year, month, day, hour, minute, second=0, timeZone=tz)
        moon = MatchMaking().moon(dt_utc)
        df = get_asthakoot_base_df(filePath=BASE_DIR / 'code/Nakshatras.xlsx')
        moondf = get_person_asthkoot_df(df, moon.position, detailed=True)
        moondf = moondf.to_dict(orient='records')

        response ={ 
            'status' : 200, 
            'dtUTC' : dt_utc, 
            'overview' : moon.overview, 
            'degrees': moon.position,
            'moondf' : moondf[0]
        }

    return JsonResponse(response)