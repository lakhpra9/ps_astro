# dfNakshatra = pd.DataFrame(data=nakshatras, columns=['Nakshatra'])
# dfNakshatra.reset_index(drop=False, inplace=True)
# dfNakshatra.to_excel('Nakshatras.xlsx', index=None)

# dfYonis = pd.read_excel('Nakshatras.xlsx')
# yoniDict = dfYonis[['Yoni', 'Nakshatra']].groupby(by='Yoni')['Nakshatra'].apply(list).to_dict()
# dfYonis['Yoni Hindi'] = dfYonis.apply(lambda x: yoniEngHin[x['Yoni']], axis=1)

# dfYonis[['Yoni', 'index']].groupby(by='Yoni')['index'].apply(list).to_dict()

# dfX['vashya'] = dfX.apply(lambda x: dfYonis[dfYonis['index'] > x['degrees']], axis=1)

# d = [j for i in zodiac_signs for j in [i]*2]
# dfRashi = pd.DataFrame(data=d, columns=['Rashi'])
# dfRashi.insert(0, 'Degrees', range(15, 360+15, 15))

# for i in range(1, 27):
#     val = ((i - 0) % 27) % 9
#     print(i, val)



# dfSelct = pd.read_excel('matching_criterion.xlsx', sheet_name=criterion)
# dfSelct.set_index(dfSelct.columns, inplace=True)
# dfM.loc[criterion, 'Obtained'] = dfSelct.loc[dfM.loc[criterion, 'Female'], dfM.loc[criterion, 'Male']]


# dfRashi = pd.DataFrame(data=zodiac_signs, columns=['Rashi'])
# dfRashi.T.to_excel('test.xlsx')


# import pytz
# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="my_app")

# def get_utc_timezone(country):
#     location = geolocator.geocode(country)
#     timezone = pytz.timezone('UTC')
#     if location is not None:
#         timezone = pytz.timezone(pytz.country_timezones[location.address.split(',')[-1].strip()])
#     return timezone


# const countryInput = document.getElementById("country");

# fetch("https://restcountries.com/v3.1/all")
#     .then((response) => response.json())
#     .then((data) => {
#         const countryNames = data.map((country) => country.name.common);
#         countryInput.setAttribute("list", "countryList");

#         const dataList = document.createElement("datalist");
#         dataList.setAttribute("id", "countryList");

#         countryNames.forEach((countryName) => {
#             const option = document.createElement("option");
#             option.value = countryName;
#             dataList.appendChild(option);
#         });

#         document.body.appendChild(dataList);
#     })
#     .catch((error) => console.error(error));