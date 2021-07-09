import pandas

if __name__ == '__main__':

    df = pandas.read_csv('restaurants.csv')
    df2 = df[['address','latitude','longitude','name']]
    df2.to_csv('restaurants_modified.csv', index=False)