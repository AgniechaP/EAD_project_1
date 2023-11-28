import os
import pandas as pd
import matplotlib.pyplot as plt

# Zadanie 1: Wczytanie danych do jednego pandas DataFrame. Dane .txt umieszczone są bezpośrednio w folderze ./data
data_path = './data'
dataframes = []

for filename in os.listdir(data_path):
    if filename.endswith(".txt"):
        year = int(filename[3:7])
        file_path = os.path.join(data_path, filename)

        df = pd.read_csv(file_path, header=None, names=["Name", "Sex", "Count"])
        df['Year'] = year
        dataframes.append(df)
all_data = pd.concat(dataframes, ignore_index=True)
print(f"Zadanie 1. Wczytanie danych do jednego DataFrame: \n {all_data} \n")

# Zadanie 2: Liczba unikalnych imion w całym zbiorze 
unique_names_count = all_data['Name'].nunique()
print(f"Zadanie 2. Liczba unikalnych imion w calym zbiorze: {unique_names_count} \n")

# Zadanie 3: Liczba unikalnych imion w całym zbiorze rozróżniając imiona męskie i imiona żeńskie
unique_names_by_sex = all_data.groupby(['Sex', 'Name'])['Name'].nunique()
unique_names_by_sex_count = unique_names_by_sex.groupby('Sex').sum()
print(f"Zadanie 3. \n Liczba unikalnych imion  F: {unique_names_by_sex_count['F']}, Liczba unikalnych imion M: {unique_names_by_sex_count['M']} \n")

# Zadanie 4: Popularność imion w danym każdym roku poprzez podzielenie liczby razy kiedy zostało nadane przez całkowitą liczbę urodzeń dla danej płci
# Suma urodzeń dla każdego roku i płci 
all_data['Total_birth'] = all_data.groupby(['Year', 'Sex'])['Count'].transform('sum')
all_data['Frequency_appearance'] = all_data['Count']/all_data['Total_birth']

result_data = all_data.pivot(index=['Year', 'Name'], columns='Sex', values='Frequency_appearance').fillna(0).reset_index()
result_data.rename(columns={"F" : "frequency_female", "M" : "frequency_male"}, inplace=True)
print(f"Zadanie 4. Popularność imion w danym każdym roku: \n {result_data} \n")

# Zadanie 5: wykres na górze - liczbę urodzin w danym roku, wykres na dole - stosunek liczby narodzin dziewczynek do liczby narodzin chłopców w każdym roku. 
# W którym roku zanotowano najmniejszą, a w którym największą różnicę w liczbie urodzeń między chłopcami a dziewczynkami? 

all_data['Total_birth_fm'] = all_data.groupby(['Year'])['Count'].transform('sum')
total_births_per_year = all_data[['Year', 'Total_birth_fm']].groupby(['Year'], as_index=False).mean()

# Stosunek liczby narodzin dziewczynek do liczby narodzin chłopców w każdym roku (wykres na dole)
births_per_year_female_male = all_data.pivot(index=['Year', 'Name'], columns='Sex', values='Count').fillna(0).reset_index()
births_per_year_female_male_sum = births_per_year_female_male[['Year', 'F', 'M']].groupby(['Year'], as_index=False).sum()
births_per_year_female_male_sum['Ratio'] = births_per_year_female_male_sum['F']/births_per_year_female_male_sum['M']

# Najmniejsza i największa różnica między chłopcami a dziewczynkami - odpowiedź pisemna 
min_diff_year = births_per_year_female_male_sum.loc[births_per_year_female_male_sum['Ratio'].idxmin()]['Year']
max_diff_year = births_per_year_female_male_sum.loc[births_per_year_female_male_sum['Ratio'].idxmax()]['Year']
print(f"Zadanie 5. Rok z min różnicą w urodzeniach: {min_diff_year}, rok z max różnicą: {max_diff_year} \n")

fig, axes = plt.subplots(nrows=2, ncols=1, sharex=False, sharey = False, figsize=(11, 10))

axes[0].bar(total_births_per_year['Year'], total_births_per_year['Total_birth_fm'])
axes[0].set_ylabel('Number of births')
axes[0].set_xlabel('Year')
axes[0].legend(['Total nr births per year'], loc='upper left')
axes[0].set_title('Total births per year')

axes[1].plot(births_per_year_female_male_sum['Year'], births_per_year_female_male_sum['Ratio'])
axes[1].set_ylabel('Ratio')
axes[1].set_xlabel('Year')
axes[1].set_title('Girls - boys birth ratio')

# Zaznaczenie min_diff i max_diff
axes[1].scatter(min_diff_year, births_per_year_female_male_sum.loc[births_per_year_female_male_sum['Year'] == min_diff_year]['Ratio'].values[0],
               color='red', marker='o', label=f'Min Diff Year: {min_diff_year}')
axes[1].scatter(max_diff_year, births_per_year_female_male_sum.loc[births_per_year_female_male_sum['Year'] == max_diff_year]['Ratio'].values[0],
               color='green', marker='o', label=f'Max Diff Year: {max_diff_year}')
axes[1].legend()
plt.show()