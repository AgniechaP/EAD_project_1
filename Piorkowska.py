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


plt.show()
