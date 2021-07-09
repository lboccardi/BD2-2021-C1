import pandas
from faker import Faker

if __name__ == '__main__':
    df = pandas.read_csv('../Original Datasets/customers.csv')
    df = df.rename(columns={'X': 'longitude', 'Y': 'latitude'})

    fake = Faker()

    df['name'] = [fake.name() for i in range(100000)]
    df2 = df[['id', 'name', 'latitude', 'longitude']]

    df2.to_csv('customers_modified.csv', index=False)