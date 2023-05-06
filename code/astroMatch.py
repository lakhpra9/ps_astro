import datetime
import math

import swisseph as swe
swe.set_sid_mode(swe.SIDM_LAHIRI)

import numpy as np
import pandas as pd

zodiac_signs = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']
nakshatras = ['अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशिरा', 'आर्द्रा', 'पुनर्वसु', 'पुष्य', 'आश्लेषा', 'मघा', 'पूर्वफाल्गुनी', 'उत्तरफाल्गुनी', 'हस्त', 'चित्रा', 'स्वाति', 'विशाखा', 'अनूराधा', 'ज्येष्ठा', 'मूल', 'पूर्वाषाढ़ा', 'उत्तराषाढ़ा', 'श्रवण', 'धनिष्ठा', 'शतभिषा', 'पूर्वभाद्रपद', 'उत्तरभाद्रपद', 'रेवती']
padasList = ['1st Pada', '2nd Pada', '3rd Pada', '4th Pada']

grihaSwami = ['मंगल', 'शुक्र', 'बुध', 'चंद्र', 'सूर्य', 'बुध', 'शुक्र', 'मंगल', 'गुरु', 'शनि', 'शनि', 'गुरु'] #['Mangal', 'Shukra', 'Budh', 'Chandra', 'Surya', 'Budh', 'Shukra', 'Mangal', 'Guru', 'Shani', 'Shani', 'Guru']
varnaList = ['क्षत्रिय', 'वैश्य', 'शूद्र', 'ब्राह्मण'] # ['Kshatriya', 'Vaishya', 'Shudra', 'Brahmin']
vashyaList = ['चतुष्पद', 'द्विपद-नर', 'जलचर', 'वनचर', 'कीट'] # ['Chatushpada', 'Dwipada/Nara', 'Jalachara', 'Vanachara', 'Keet',]
NaadiList = ['आदि', 'मध्य', 'अंत्य'] # ['Aadi', 'Madhya', 'Antya']

def getVashyaDataFrame():
    
    # ref-link = 'https://www.drikpanchang.com/tutorials/jyotisha/kundali-match/ashta-kuta/vashya-kuta.html'
    # more-ref = 'https://aaps.space/blog/vashya-matching/'
    # Read more on 'https://aaps.space/blog/kundali-matching-process/'

    vashyaDict = {
    'चतुष्पद' : ['0-60', '255-285'],
    'द्विपद-नर' : ['60-90', '150-210', '240-255', '300-330'],
    'जलचर' : ['90-120', '285-300', '330-360'],
    'वनचर' : ['120-150'],
    'कीट' : ['210-240']
    }

    # tolerance = 0.00001
    # data = [(int(j.split('-')[0])+tolerance, float(j.split('-')[1]), k) for k, v in vashyaDict.items() for j in v]

    data = [(int(j.split('-')[1]), k) for k, v in vashyaDict.items() for j in v]
    dfVashya = pd.DataFrame(data, columns=['Max Degrees', 'Vashya'])
    dfVashya.sort_values(by='Max Degrees', inplace=True, ignore_index=True)
    return dfVashya

def get_asthakoot_base_df():
    dfYonis = pd.read_excel('Nakshatras.xlsx')
    dfVashya = getVashyaDataFrame()

    # Naadis = NaadiList + NaadiList[::-1]
    # Naadis = Naadis * 4 + NaadiList
    # Naadis = [j for i in Naadis for j in [i]*4]

    stp = 360/(27*4)
    degrees = np.arange(stp, 360 + stp, stp)

    df = pd.DataFrame(data=degrees, columns=['degrees'])
    df['degrees'] = df['degrees'].apply(lambda x: round(x, 4))

    df['rashi'] = [j for i in range(len(zodiac_signs)) for j in [i]*9]
    df['rashiName'] = df.apply(lambda x: zodiac_signs[int(x['rashi'])], axis=1)
    df['nakshatra'] = [j for i in range(len(nakshatras)) for j in [i]*4]
    df['nakshatraName'] = df.apply(lambda x: nakshatras[int(x['nakshatra'])], axis=1)
    df['padas'] = [i for i in range(1, 5)] * 27

    cols = ['degrees', 'rashi', 'nakshatra', 'rashiName', 'nakshatraName', 'padas']
    df = df[cols]

    df['graha maitri'] = [j for i in grihaSwami for j in [i]*9]
    df['varna'] = [j for i in varnaList for j in [i]*9] * 3
    df['vashya'] = df.apply(lambda x: dfVashya.loc[dfVashya['Max Degrees'] >= x['degrees'], 'Vashya'].tolist()[0], axis=1)

    df['yoni'] = df.apply(lambda x: dfYonis[dfYonis['index'] == x['nakshatra']]['Yoni'].tolist()[0], axis=1)
    df['gana'] = df.apply(lambda x: dfYonis[dfYonis['index'] == x['nakshatra']]['Gana'].tolist()[0], axis=1)
    df['naadi'] = df.apply(lambda x: dfYonis[dfYonis['index'] == x['nakshatra']]['Naadi'].tolist()[0], axis=1)

    return df

def get_person_asthkoot_df(df, moonPosition):
    # df :  this is the base df desrived in the function get_asthakoot_base_df
    # moonPosition : In degrees in the sky (converted to UTC)
    
    # if moonPosition < 0:
    #     idx = df['degrees'].sub(360 + moonPosition).abs().idxmin()
    # else:
    #     idx = df['degrees'].sub(moonPosition).abs().idxmin() #+ 1

    moonPosition = moonPosition % 360
    idx = df[df['degrees'] >= moonPosition].index[0]

    dfFin = df.loc[[idx]]
    dfFin.reset_index(drop=True, inplace=True)
    dfFin['Tara'] = ''

    cols = ['nakshatra', 'varna', 'vashya', 'Tara', 'yoni', 'graha maitri', 'gana', 'rashiName', 'naadi']
    dfFin = dfFin[cols]
    dfFin.rename(columns={'rashiName':'bhakut'}, inplace=True)

    return dfFin


def get_matchmaking_df(maledf, femaledf):
    dfM = maledf.T.rename(columns={0:'Male'})
    dfM = dfM.join(femaledf.T.rename(columns={0:'Female'}))

    maleNakshatra = dfM.loc['nakshatra', 'Male']
    femaleNakshatra = dfM.loc['nakshatra', 'Female']
    dfM.loc['Tara', 'Male'] =  ((femaleNakshatra - maleNakshatra) % 27) % 9 +1
    dfM.loc['Tara', 'Female'] =  ((maleNakshatra - femaleNakshatra) % 27) % 9 +1
    dfM.drop(index=['nakshatra'], inplace=True)
    dfM['Obtained'] = ''
    dfM['Max Points'] = range(1, 9)

    criterionList = ['varna', 'vashya', 'Tara', 'yoni', 'graha maitri', 'gana', 'bhakut', 'naadi']

    for criterion in criterionList:
        dfSelct = pd.read_excel('asthkoot_criterion.xlsx', sheet_name=criterion)
        dfSelct.set_index(dfSelct.columns, inplace=True)
        dfM.loc[criterion, 'Obtained'] = dfSelct.loc[dfM.loc[criterion, 'Female'], dfM.loc[criterion, 'Male']]
        
    dfM['Obtained'] = dfM['Obtained'].astype('float64')
        
    # total_points = sum(dfM[~dfM['Obtained'].eq('')]['Obtained'].tolist())

    return dfM


class MatchMaking():
    def __init__(self):
        pass

    def convert_standard_to_utc_time(self, year, month, day, hour, minute, second, timeZone='+00:00'):
        # year = 1995
        # month = 5
        # day = 27
        # hour = 22
        # minute = 35
        # second = 0
        # timeZone = '+05:30'

        month = f'0{month}' if month < 10 else month
        day = f'0{day}' if day < 10 else day
        hour = f'0{hour}' if hour < 10 else hour
        minute = f'0{minute}' if minute < 10 else minute
        second = f'0{second}' if second < 10 else second

        # input datetime in string format
        dt_str = f'{year}-{month}-{day} {hour}:{minute}:{second}{timeZone}'
        dt = datetime.datetime.fromisoformat(dt_str)
        dt_utc = dt.astimezone(datetime.timezone.utc)

        return dt_utc

    def moon(self, dt_utc):
        jd = swe.utc_to_jd(dt_utc.year , dt_utc.month, dt_utc.day, dt_utc.hour, dt_utc.minute, dt_utc.second)
        jd = float(jd[1])
        ayanamsha = swe.get_ayanamsa_ut(jd)
        moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
        moon_pos = moon_pos - ayanamsha
        # moon_pos = moon_pos % 360

        moon_sign = math.floor(moon_pos / 30.0) % 12

        nakshatra_num = math.floor(moon_pos / (360/27)) + 1
        nakshatra_num = (nakshatra_num - 1) % 27

        nakshatra_pada = math.floor(moon_pos / (360/(27*4)))
        nakshatra_pada = (nakshatra_pada) % 4

        base_vikalas = ((moon_pos % 30) * 60 * 60 )
        vikala = base_vikalas % 60
        kala = (base_vikalas - vikala)/60 % 60
        ansh = ((base_vikalas - vikala)/60 - kala) / 60 % 30

        self.position = moon_pos
        self.vikala = math.floor(vikala)
        self.kala = math.floor(kala)
        self.ansh = math.floor(ansh)
        self.rashi = moon_sign
        self.rashiName = zodiac_signs[moon_sign]

        self.nakshatra = nakshatra_num
        self.nakshatraName = nakshatras[nakshatra_num]

        self.pada = nakshatra_pada
        self.padaName = padasList[nakshatra_pada]

        self.overview = f'{self.rashi} [{self.rashiName}] {self.ansh}:{self.kala}:{self.vikala} | {self.nakshatraName} & {self.padaName}'

        return self
    


# ------- Extras --------
# d = [j for i in zodiac_signs for j in [i]*2]
# dfRashi = pd.DataFrame(data=d, columns=['Rashi'])
# dfRashi.insert(0, 'Degrees', range(15, 360+15, 15))