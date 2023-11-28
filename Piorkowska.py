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

fig, axes = plt.subplots(nrows=2, ncols=1, sharex=False, sharey = False, figsize=(11, 10), num='Zadanie 5')

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
# plt.show()

# Zadanie 6: 1000 najpopularniejszych imion dla każdej płci w całym zakresie czasowym
# Dla każdego imienia kumulacyjna suma wartości frequency - jako najpopularniejsze należy uznać imiona, które najdłużej zajmowały wysokie miejsce na liście rankingowej
result_data_test = all_data.groupby(['Year', 'Name', 'Sex'])['Frequency_appearance'].sum().unstack(fill_value=0).reset_index()

top_names_per_year_sex = all_data.groupby(['Year', 'Sex', 'Name'])['Frequency_appearance'].sum().reset_index()
# Year - ascending, Sex - ascending, Frequency - descending 
top_names_per_year_sex = top_names_per_year_sex.sort_values(by=['Year', 'Sex', 'Frequency_appearance'], ascending=[True, True, False])
top_names_per_year_sex['Rank'] = top_names_per_year_sex.groupby(['Year', 'Sex']).cumcount() + 1

top1000_ranking = top_names_per_year_sex[top_names_per_year_sex['Rank'] <= 1000].groupby(['Sex', 'Name'])['Frequency_appearance'].sum().reset_index()
top1000_ranking = top1000_ranking.sort_values(by=['Sex', 'Frequency_appearance'], ascending=[True, False])
top1000_ranking['Rank'] = top1000_ranking.groupby('Sex').cumcount() + 1

print(f"Zadanie 6. \n")
print("Top 1000 imion dla płci żeńskiej:")
print(top1000_ranking[top1000_ranking['Sex'] == 'F'].head(1000))

print("\nTop 1000 imion dla płci męskiej:")
print(top1000_ranking[top1000_ranking['Sex'] == 'M'].head(1000))

# Zadanie 7: Wyświetl na jednym wykresie zmiany dla imienia męskiego John i pierwszego imienia żeńskiego rankingu top-1000 
years_to_plot = [1934, 1980, 2022]

# John count 
john_count = all_data[(all_data['Name'] == 'John')& (all_data['Year'].apply(lambda x: x in years_to_plot))]

# First female name count
first_female_name = top1000_ranking[top1000_ranking['Sex'] == 'F'].head(1)['Name'].values[0]
first_female_name_count = all_data[(all_data['Name'] == first_female_name) & (all_data['Year'].apply(lambda x: x in years_to_plot))]


fig, ax = plt.subplots(figsize=(10, 6), num='Zadanie 7')
# Lewa strona tj. count
bar_width = 0.5
bar_gap = 0.9
bar_positions_john = john_count['Year'] - bar_width - bar_gap
bar_positions_female = first_female_name_count['Year'] + bar_gap

ax.set_xlabel('Year')
ax.set_ylabel('Count of Names', color='tab:blue')
ax.bar(bar_positions_john, john_count['Count'], color='tab:blue', label='Count of Name (John)')
ax.bar(bar_positions_female, first_female_name_count['Count'], color='tab:red', label=f'Count of Name ({first_female_name})')
ax.tick_params(axis='y')
ax.legend(loc='upper left')

bar_positions_john_popularity = bar_positions_john + bar_width + bar_gap
bar_positions_female_popularity = bar_positions_female + bar_width + bar_gap

ax2 = ax.twinx()
ax2.set_ylabel('Popularity', color='tab:green')
ax2.bar(bar_positions_john_popularity, john_count['Frequency_appearance'], color='tab:green', label='Popularity of Name (John)')
ax2.bar(bar_positions_female_popularity, first_female_name_count['Frequency_appearance'], color='tab:brown', label=f'Popularity of Name ({first_female_name})')
ax2.tick_params(axis='y')
ax2.legend(loc='upper right')

# Zadanie 8: Wykreśl wykres z podziałem na lata i płeć zawierający informację jaki procent w danym roku stanowiły imiona należące do rankingu top1000
top1000_men = top1000_ranking[top1000_ranking['Sex'] == 'M'].head(1000)['Name'].tolist()
top1000_female = top1000_ranking[top1000_ranking['Sex'] == 'F'].head(1000)['Name'].tolist()
top1000_male_female = top1000_men + top1000_female
# Czy dane imie w konkretnym roku należy do rankingu top 1000 dla całego przedziału czasowego
all_data['IsInTop1000'] = all_data['Name'].isin(top1000_male_female)
unique_names_count_per_sex_year = all_data.groupby(['Year', 'Sex'])['IsInTop1000'].mean().reset_index()
unique_names_count_per_sex_year['IsInTop1000_percent'] = unique_names_count_per_sex_year['IsInTop1000'] * 100

# Najwieksza roznica w roznorodnosci miedzy imionami meskimi a zenskimi 
unique_names_count_per_sex_year_male = unique_names_count_per_sex_year[unique_names_count_per_sex_year['Sex'] == 'M']
unique_names_count_per_sex_year_female = unique_names_count_per_sex_year[unique_names_count_per_sex_year['Sex'] == 'F']
diff_percent = unique_names_count_per_sex_year_male.set_index('Year')['IsInTop1000_percent'] - unique_names_count_per_sex_year_female.set_index('Year')['IsInTop1000_percent']
max_diff_year_diversity = diff_percent.idxmax()
max_diff_value_diversity = diff_percent.max()

print(f"Zadanie 8. \n Największa różnica w różnorodności między imionami męskimi a żeńskimi występuje w roku {max_diff_year_diversity} z różnicą wynoszącą {max_diff_value_diversity:.2f}%.")

# Wykres
fig, ax = plt.subplots(figsize=(12, 6), num='Zadanie 8')

# Wykres dla imion męskich
ax.bar(unique_names_count_per_sex_year[unique_names_count_per_sex_year['Sex'] == 'M']['Year'], unique_names_count_per_sex_year[unique_names_count_per_sex_year['Sex'] == 'M']['IsInTop1000_percent'], label='Male Names', color='lightblue')
ax.bar(unique_names_count_per_sex_year[unique_names_count_per_sex_year['Sex'] == 'F']['Year'], unique_names_count_per_sex_year[unique_names_count_per_sex_year['Sex'] == 'F']['IsInTop1000_percent'], label='Female Names', color='lightcoral')

ax.annotate(f'Max Difference\nYear: {max_diff_year_diversity}, Value: {max_diff_value_diversity:.2f}%', xy=(max_diff_year_diversity, max_diff_value_diversity), xytext=(max_diff_year_diversity + 3, max_diff_value_diversity + 5),
            arrowprops=dict(facecolor='black', shrink=0.05))

ax.set_xlabel('Year')
ax.set_ylabel('Percent of names in each year which were in Top1000 of all time')
ax.legend()
ax.set_title('What percent of names per sex and year appear in Top1000 ranking')

# Zadanie 9: Zweryfikuj hipotezę czy prawdą jest, że w obserwowanym okresie rozkład ostatnich liter imion męskich uległ istotnej zmianie? 

# dokonaj agregacji wszystkich urodzeń w pełnym zbiorze danych z podziałem na rok i płeć i ostatnią literę
# Dodanie kolumny Last_letter
all_data['Last_letter'] = all_data['Name'].apply(lambda x: x[-1])

# Agregacja danych
letter_popularity = all_data.groupby(['Year', 'Sex', 'Last_letter'])['Count'].sum().reset_index()

# Wyodrebnienie lat do sprawdzenia 
years_to_compare = [1917, 1967, 2022]
selected_years_data = letter_popularity[letter_popularity['Year'].isin(years_to_compare)].copy()

selected_years_data['Total_births'] = selected_years_data.groupby(['Year', 'Sex'])['Count'].transform('sum')
selected_years_data['Normalized_popularity'] = selected_years_data['Count'] / selected_years_data['Total_births']

print(f"Zagregowane dane z popularnoscia ostatniej litery zadanie 9. \n Dane dla lat 1917, 1967, 2022: \n {selected_years_data}")

fig, ax = plt.subplots(figsize=(12, 8), num='Zadanie 9.4 Wykres slupkowy popularnosc litery')

# Unikalne litery z kolumny dot. ostatniej litery
letters = selected_years_data['Last_letter'].unique()
# Unikalne lata z kolumny dot. lat
years_plot = selected_years_data['Year'].unique()
num_years = len(years_plot)
bar_width = 0.2

# Bar - plot dla każdego roku (mężczyźni)
for i, year in enumerate(years_plot):
    data_year = selected_years_data[(selected_years_data['Year'] == year) & (selected_years_data['Sex'] == 'M')]
    
    # Pozycjonowanie bar plotów 
    positions = [x + i * bar_width for x in range(len(data_year['Last_letter']))]
    
    ax.bar(positions, data_year['Normalized_popularity'], width=bar_width, label=str(year))


# Pozycjonowanie oznaczeń oś x 
ax.set_xticks([x + (num_years - 1) * bar_width / 2 for x in range(len(letters))])
ax.set_xticklabels(letters)
ax.set_xlabel('Last Letter')
ax.set_ylabel('Normalized Popularity')
ax.set_title('Normalized popularity of last letters of man names over years')

ax.legend(title='Year', loc='upper right')

# Wyświetl, dla której litery wystąpił największy wzrost/spadek między rokiem 1917 a 2022)
# Najwiekszy wzrost lub spadek - najwieksza abs(roznica)
data_1917 = selected_years_data[(selected_years_data['Year'] == 1917) & (selected_years_data['Sex'] == 'M')]
data_2022 = selected_years_data[(selected_years_data['Year'] == 2022) & (selected_years_data['Sex'] == 'M')]

merged_data = pd.merge(data_1917, data_2022, on='Last_letter', suffixes=('_1917', '_2022'))

merged_data['Change'] = abs(merged_data['Normalized_popularity_2022'] - merged_data['Normalized_popularity_1917'])

max_change_letter = merged_data.loc[merged_data['Change'].idxmax()]['Last_letter']
max_change_value = merged_data['Change'].max()

print(f"Zadanie 9.4 \n Największy wzrost/spadek dla litery: '{max_change_letter} (wartosc bezwzgledna z roznicy)'")

# 3 litery z najwieksza zmiana:
top3_changed_letters = merged_data.nlargest(3, 'Change')['Last_letter'].tolist()

# Calkowita liczba urodzen dla kazdego roku i plci 
letter_popularity['Total_births'] = letter_popularity.groupby(['Year', 'Sex'])['Count'].transform('sum')

# Normalizacja popularności
letter_popularity['Normalized_popularity'] = letter_popularity['Count'] / letter_popularity['Total_births']


data_top3_letters = letter_popularity[letter_popularity['Last_letter'].isin(top3_changed_letters) & (letter_popularity['Sex'] == 'M')]

# Wykres trendu popularności dla każdej z wybranych liter
fig, ax = plt.subplots(figsize=(12, 8), num='Zadanie 9.5 Przebieg trendu popularnosci')

for letter in top3_changed_letters:
    # data_letter = data_top3_letters[data_top3_letters['Last_letter'] == letter]
    # ax.plot(data_letter['Year'], data_letter['Count'], label=f'Letter {letter}')

    data_letter = letter_popularity[(letter_popularity['Last_letter'] == letter) & (letter_popularity['Sex'] == 'M')]
    ax.plot(data_letter['Year'], data_letter['Normalized_popularity'], label=f'Letter {letter}')

ax.set_xlabel('Year')
ax.set_ylabel('Normalized popularity of last names letters')
ax.set_title('Trend of popularity for top 3 changed last letters (male mames) over years')
ax.legend()

# Zadanie 10: 
# Imiona nadawane zarówno dziewczynkom jak i chłopcom w obu przedziałach czasowych razem
common_names = set(top1000_ranking[top1000_ranking['Sex'] == 'M']['Name']).intersection(set(top1000_ranking[top1000_ranking['Sex'] == 'F']['Name']))

# Wyszczegolnianie danych dla wspolncyh imion
common_names_data = all_data[all_data['Name'].isin(common_names)].copy()

# Zagregowane dane do roku 1930
data_before_1930 = common_names_data[common_names_data['Year'] <= 1930]

# Zagregowane dane od roku 2000
data_after_2000 = common_names_data[common_names_data['Year'] >= 2000]

# Grupowanie danych po imionach i płci
grouped_data_before_1930 = data_before_1930.groupby(['Name', 'Sex'])['Count'].sum().unstack(fill_value=0).reset_index()
grouped_data_after_2000 = data_after_2000.groupby(['Name', 'Sex'])['Count'].sum().unstack(fill_value=0).reset_index()

# Stosunek imion męskich do żeńskich z uwzględnieniem zabezpieczenia niedzielenia przez zero tj. zero zastępowane bardzo małą liczbą
grouped_data_before_1930['Ratio'] = grouped_data_before_1930['M'] / (grouped_data_before_1930['F'].replace(0, 1e-10))
grouped_data_after_2000['Ratio'] = grouped_data_after_2000['M'] / (grouped_data_after_2000['F'].replace(0, 1e-10))
# grouped_data_before_1930['Ratio'] = grouped_data_before_1930['M'] / grouped_data_before_1930['F']
# grouped_data_after_2000['Ratio'] = grouped_data_after_2000['M'] / grouped_data_after_2000['F']

# Polaczenie wynikow ratio dla imion dla dat przed 1930 i po 2000
data_before_1930_only_names_and_ratio = grouped_data_before_1930[['Name', 'Ratio']]
data_after_2000_only_names_and_ratio = grouped_data_after_2000[['Name', 'Ratio']]


before1930_after2000_merge_data = pd.merge(data_before_1930_only_names_and_ratio, data_after_2000_only_names_and_ratio, on='Name', suffixes=('_before_1930', '_after_2000'))

# Różnica w stosunkach między latami dla imion
before1930_after2000_merge_data['Ratio_Difference'] = abs(before1930_after2000_merge_data['Ratio_after_2000'] - before1930_after2000_merge_data['Ratio_before_1930'])

# 2 imiona z największą różnicą w ratio między dwoma przedziałami dat 
# Znalezienie dwóch imion z największą różnicą
top_2_diff_ratio_names = before1930_after2000_merge_data.nlargest(2, 'Ratio_Difference')

# Wyświetlenie imion
print("Zadanie 10.1 \n")
print("Dwa imiona z największą zmianą w stosunku między przed 1930 a po 2000: \n")
print(top_2_diff_ratio_names[['Name', 'Ratio_before_1930', 'Ratio_after_2000', 'Ratio_Difference']])

# Wyswietlanie przebiegu - kroki
selected_names_data_before_1930 = data_before_1930[data_before_1930['Name'].isin(top_2_diff_ratio_names['Name'])].copy()
selected_names_data_after_2000 = data_after_2000[data_after_2000['Name'].isin(top_2_diff_ratio_names['Name'])].copy()

selected_names_data_before_1930['Time Period'] = 'Before 1930'
selected_names_data_after_2000['Time Period'] = 'After 2000'

# Łączenie danych przed 1930 i po 2000
combined_data = pd.concat([selected_names_data_before_1930, selected_names_data_after_2000])

# Unikalne lata
years = combined_data['Year'].unique()
ratio_data = []

# Iterowanie po latach
for year in years:
    # Dane dla danego roku
    data_year = combined_data[combined_data['Year'] == year]

    # Pobranie unikalnych imion dla obu płci
    unique_names_male = data_year[data_year['Sex'] == 'M']['Name'].unique()
    unique_names_female = data_year[data_year['Sex'] == 'F']['Name'].unique()

    # Patrzymy tylko na imiona, ktore wystepowaly zarowno u kobiet jak i mezczyzn np. Walter F i Walter M
    common_names = set(unique_names_male) & set(unique_names_female)
    for name in common_names:
        count_male = data_year[(data_year['Name'] == name) & (data_year['Sex'] == 'M')]['Count'].values[0] if name in unique_names_male else 0
        count_female = data_year[(data_year['Name'] == name) & (data_year['Sex'] == 'F')]['Count'].values[0] if name in unique_names_female else 0

        # Obliczamy stosunek i dodajemy do listy
        ratio = count_male / (count_female + 1e-10)  # Dodajemy małą wartość, aby uniknąć dzielenia przez zero
        ratio_data.append({'Year': year, 'Name': name, 'Ratio': ratio})

# Tworzenie DataFrame z listy
ratio_df = pd.DataFrame(ratio_data)
ratio_df = ratio_df.sort_values(by='Year')

fig, ax = plt.subplots(figsize=(12, 8), num='Zadanie 10.')
for name in top_2_diff_ratio_names['Name']:
    data_name = ratio_df[ratio_df['Name'] == name]
    ax.plot(data_name['Year'], data_name['Ratio'], label=name)
ax.set_xlabel('Year')
ax.set_ylabel('male-to-female ratio')
ax.set_title('Trend of male-to-female ratio for names which ratio has the biggest diff data after 2000 and before 1930')
ax.legend()

plt.show()
