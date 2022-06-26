from operator import ge
import pandas as pd

ETHANOL_SPECIFIC_GRAV = 0.787

def abv2unit(data):
    return data['volume'] * (data['abv'] / 100) / 10

def get_ethanol_in_weight(data):
    return data['volume'] * (data['abv'] / 100) * ETHANOL_SPECIFIC_GRAV

def get_bac(volume, abv, weight, gender='a'):
    if gender == 'm':
        return get_ethanol_in_weight({'volume': volume, 'abv': abv}) / (weight * 1000 * 0.68)
    elif gender == 'f':
        return get_ethanol_in_weight({'volume': volume, 'abv': abv}) / (weight * 1000 * 0.55)
    elif gender == 'a':
        return get_ethanol_in_weight({'volume': volume, 'abv': abv}) / (weight * 1000 * 0.615)
    else:
        return None

# show BAC chart
BAC_NOTE = [
    [0.01, 'mild intoxication'], 
    [0.04, 'impaired judgement'], 
    [0.07, 'legally drunk'], 
    [0.10, 'obvious physical impairment, loss of judgment'], 
    [0.13, 'blurred vision, loss of coordination and balance'], 
    [0.16, 'difficulty walking'], 
    [0.20, 'possible blackouts'], 
    [0.30, 'likelihood of unconsciousness'], 
    [0.40, 'possible death'], 
]

WEIGHT = 75 # in kg
GENDER = 'a'

print(f'at the weight of {WEIGHT} kg...')
sep = '-' * 5
prebac = 0.0
for i in range(1, 26):
    bac = get_bac(10 * i, 100, WEIGHT, gender=GENDER)

    for n in BAC_NOTE:
        if ((prebac * 100) < n[0]) & ((bac * 100) >= n[0]):
            print(f'{sep} >= {n[0]:>3.2f}% {sep} {n[1]}')

    print(f'{i:>2d} unit = BAC: {bac * 100:>5.3f}%')

    prebac = bac

print('-' * 40)

# load beverage data
df_alc = pd.read_csv('alcdata.csv', encoding='utf-8', 
    header=0, parse_dates=True)

df_alc['units'] = abv2unit(df_alc)
df_alc['price_per_unit'] = df_alc['price'] / df_alc['units']

# sort by lowest unit price and show top 3
df_alc_sroted = df_alc.sort_values('price_per_unit', ascending=True)
print(df_alc_sroted[['name', 'abv', 'units', 'price', 'price_per_unit']].head(3))