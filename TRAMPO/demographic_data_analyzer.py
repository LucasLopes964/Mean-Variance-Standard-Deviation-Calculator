import pandas as pd

def calculate_demographic_data(print_data=True):
    column_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
        'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
        'hours-per-week', 'native-country', 'salary'
    ]
    # Leia o arquivo CSV, ignorando espaços após vírgulas
    df = pd.read_csv('adult.data.csv', header=None, names=column_names, skipinitialspace=True)

    # Limpeza seletiva: remova linhas com '?' apenas nas colunas problemáticas
    for col in ['workclass', 'occupation', 'native-country']:
        df = df[df[col] != '?']

    # Converta colunas numéricas para o tipo correto
    df['age'] = df['age'].astype(int)
    df['hours-per-week'] = df['hours-per-week'].astype(int)

    # Quantidade de cada raça
    race_count = df['race'].value_counts()

    # Média de idade dos homens
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # Porcentagem de pessoas com Bacharelado
    percentage_bachelors = round((df['education'] == 'Bachelors').sum() / len(df) * 100, 1)

    # Educação avançada
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education

    # Porcentagem com salário >50K
    higher_education_total = df[higher_education].shape[0]
    lower_education_total = df[lower_education].shape[0]

    higher_education_rich = round(
        (df[higher_education & (df['salary'] == '>50K')].shape[0] / higher_education_total) * 100, 1
    ) if higher_education_total > 0 else 0.0

    lower_education_rich = round(
        (df[lower_education & (df['salary'] == '>50K')].shape[0] / lower_education_total) * 100, 1
    ) if lower_education_total > 0 else 0.0

    # Menor número de horas trabalhadas por semana
    min_work_hours = df['hours-per-week'].min()

    # Porcentagem de pessoas que trabalham o mínimo de horas e ganham >50K
    num_min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round(
        (num_min_workers[num_min_workers['salary'] == '>50K'].shape[0] / num_min_workers.shape[0]) * 100, 1
    ) if num_min_workers.shape[0] > 0 else 0.0

    # País com maior porcentagem de pessoas que ganham >50K
    country_counts = df['native-country'].value_counts()
    country_rich_counts = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_rich_percentage = (country_rich_counts / country_counts * 100).fillna(0)
    highest_earning_country = country_rich_percentage.idxmax()
    highest_earning_country_percentage = round(country_rich_percentage.max(), 1)

    # Ocupação mais comum entre os ricos na Índia
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    top_IN_occupation = india_rich['occupation'].value_counts().idxmax() if not india_rich.empty else None

    # DO NOT MODIFY BELOW THIS LINE
    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }