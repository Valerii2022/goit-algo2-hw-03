import csv
import timeit
from BTrees.OOBTree import OOBTree


def load_data(filename):

    data = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["ID"] = int(row["ID"])
            row["Price"] = float(row["Price"])
            data.append(row)
    return data


def add_item_to_tree(tree, item):

    tree[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


def add_item_to_dict(dictionary, item):

    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


def range_query_tree(tree, min_price, max_price):

    return [v for k, v in tree.items() if min_price <= v["Price"] <= max_price]


def range_query_dict(dictionary, min_price, max_price):

    return [v for v in dictionary.values() if min_price <= v["Price"] <= max_price]


def measure_time(func, *args):

    return timeit.timeit(lambda: func(*args), number=100)


data = load_data("generated_items_data.csv")

tree = OOBTree()
dictionary = {}


tree_update = lambda: [add_item_to_tree(tree, item) for item in data]
dict_update = lambda: [add_item_to_dict(dictionary, item) for item in data]
timeit.timeit(tree_update, number=1)
timeit.timeit(dict_update, number=1)


min_price, max_price = 10.0, 50.0

tree_time = measure_time(range_query_tree, tree, min_price, max_price)
dict_time = measure_time(range_query_dict, dictionary, min_price, max_price)


print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
