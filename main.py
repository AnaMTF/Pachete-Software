import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Încărcați fișierul Excel
df = pd.read_excel("Sephora.xlsx")
print(df)

print(" ")
print("##########################################")
print(" ")


#Am creat un map
data_map = {}

for index, row in df.iterrows():
    nr_crt = row['Nr.Crt']
    product_links = row['Product_links']
    brand_name = row['brand_name']
    product_name = row['product_name']
    item_id = row['item_id']

    data_map[nr_crt] = {
        'product_links': product_links,
        'brand_name': brand_name,
        'product_name': product_name,
        'item_id': item_id
    }

for nr_crt, data in data_map.items():
    print(f"Nr.Crt: {nr_crt}")
    print(f"Product Links: {data['product_links']}")
    print(f"Brand Name: {data['brand_name']}")
    print(f"Product Name: {data['product_name']}")
    print(f"Item ID: {data['item_id']}")
    print("--------------------")

print(" ")
print("##########################################")
print(" ")

#Afiseaza cel mai apreciat produs(cel care are cele mai multe voturi cu 5 stele)
max_five_stars = df[df['five_star'] == df['five_star'].max()]
product_name = max_five_stars['product_name'].iloc[0]
num_five_stars = max_five_stars['five_star'].iloc[0]

print("Produsul cu cele mai multe five_stars:")
print("Nume produs:", product_name)
print("Număr de stele:", num_five_stars)

print(" ")
print("##########################################")
print(" ")

#Afiseaza cel mai putin apreciat produs(cel care are cele mai multe voturi cu o stea)
min_one_star = df[df['one_star'] == df['one_star'].max()]
product_name = min_one_star['product_name'].iloc[0]
num_one_star = min_one_star['one_star'].iloc[0]

print("Produsul cu cele mai multe one-star:")
print("Nume produs:", product_name)
print("Număr de stele:", num_one_star)

print(" ")
print("##########################################")
print(" ")

#Afiseaza preturile produselor finale cu TVA(pretul afisat este cel fara tva) -se salveaza intr-un dataframe separat si se afiseaza

df['pret_final'] = df['price'] * (1 + df['TVA%'] / 100)
df_pret_final = df[['product_name', 'pret_final']]

print(df_pret_final)

print(" ")
print("##########################################")
print(" ")

#Sa se calculeze rating ul fiecarul produs(media voturilor acordate) si sa se salveze intr-un dataframe

df["rating"] = df["one_star"] + 2 * df["two_star"] + 3 * df["three_star"] + 4 * df["four_star"] + 5 * df["five_star"]
df["rating"] = df["rating"] / (df["one_star"] + df["two_star"] + df["three_star"] + df["four_star"] + df["five_star"])

rating_df = df[["product_name", "rating"]]

#rating_df.to_excel("output.xlsx", index=False)

print(" ")
print("##########################################")
print(" ")

#Produsul cu cel mai mic rating

min_rating_product = rating_df.loc[rating_df["rating"].idxmin()]
product_name_min_rating = min_rating_product["product_name"]
print("Produsul cu cel mai mic rating:", product_name_min_rating)

print(" ")
print("##########################################")
print(" ")

#Produsul cu cel mai mare rating

max_rating_product = rating_df.loc[rating_df["rating"].idxmax()]
product_name_max_rating = max_rating_product["product_name"]
print("Produsul cu cel mai mare rating:", product_name_max_rating)

print(" ")
print("##########################################")
print(" ")

#Statisici descriptive pe rating

rating_df = df[['product_name', 'rating']]
descriptive_stats = rating_df.describe()
print(descriptive_stats)

print(" ")
print("##########################################")
print(" ")

#Statistici descriptive pe mai multe coloane

selected_columns = ['number_of_reviews', 'number_of_loves', 'price']
statistics = df[selected_columns].describe()
print(statistics)

print(" ")
print("##########################################")
print(" ")

#Agregam doua dataframe-uri cel cu rating si cel cu pret_final (df_pret_final, rating_df)

agregat_df = df_pret_final.merge(rating_df, on='product_name', how='inner')
print(agregat_df)

print(" ")
print("##########################################")
print(" ")

#Sa se realizeze un heatmap cu valorile rating-urilor din dataframe ul rating_df

product_names = rating_df['product_name']
ratings = rating_df['rating']

heatmap_data = pd.pivot_table(data=rating_df, values='rating', index='product_name')

plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f")

plt.title('Heatmap of Ratings')
plt.xlabel('Product Name')
plt.ylabel('Rating')

plt.show()
