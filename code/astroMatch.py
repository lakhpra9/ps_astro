import datetime
import math
import swisseph as swe
swe.set_sid_mode(swe.SIDM_LAHIRI)
import pandas as pd

zodiac_signs = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']
nakshatras = ['अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशीर्ष', 'आर्द्रा', 'पुनर्वसु', 'पुष्य', 'आश्लेषा', 'मघा', 'पूर्वफाल्गुनी', 'उत्तरफाल्गुनी', 'हस्त', 'चित्रा', 'स्वाति', 'विशाखा', 'अनूराधा', 'ज्येष्ठा', 'मूल', 'पूर्वाषाढ़ा', 'उत्तराषाढ़ा', 'श्रवण', 'श्रविष्ठा', 'शतभिषा', 'पूर्वभाद्रपद', 'उत्तरभाद्रपद', 'रेवती']
padasList = ['1st Pada', '2nd Pada', '3rd Pada', '4th Pada']

grihaSwami = ['मंगल', 'शुक्र', 'बुध', 'चंद्र', 'सूर्य', 'बुध', 'शुक्र', 'मंगल', 'गुरु', 'शनि', 'शनि', 'गुरु'] #['Mangal', 'Shukra', 'Budh', 'Chandra', 'Surya', 'Budh', 'Shukra', 'Mangal', 'Guru', 'Shani', 'Shani', 'Guru']
varnaList = ['क्षत्रिय', 'वैश्य', 'शूद्र', 'ब्राह्मण'] # ['Kshatriya', 'Vaishya', 'Shudra', 'Brahmin']
vashyaList = ['चतुष्पद', 'द्विपद-नर', 'जलचर', 'वनचर', 'कीट'] # ['Chatushpada', 'Dwipada/Nara', 'Jalachara', 'Vanachara', 'Keet',]

def getVashyaDataFrame():
    
    # ref-link = 'https://www.drikpanchang.com/tutorials/jyotisha/kundali-match/ashta-kuta/vashya-kuta.html'
    # more-ref = 'https://aaps.space/blog/vashya-matching/'

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