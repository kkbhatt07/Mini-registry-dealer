# # Importing specific items
# from math import sqrt, sin

# A = 16
# B = 3.14
# print(sqrt(A))
# print(sin(B))

# /////////////////////

# import numpy as np
 
# # Creating a rank 1 Array
# arr = np.array([1, 2, 3])
# print(arr)
 
# # Creating a rank 2 Array
# arr = np.array([[1, 2, 3],
#                 [4, 5, 6]])
# print(arr)
 
# # Creating an array from tuple
# arr = np.array((1, 3, 2))
# print(arr)

# ///////////////////////

# import pandas as pd

# lst = ['Geeks', 'For', 'Geeks', 'is', 
#             'portal', 'for', 'Geeks']

# df = pd.DataFrame(lst)
# print(df)

#/////////////////////////

# # Import libraries
# from matplotlib import pyplot as plt
# import numpy as np


# # Creating dataset
# cars = ['AUDI', 'BMW', 'FORD',
#         'TESLA', 'JAGUAR', 'MERCEDES']

# data = [23, 17, 35, 29, 12, 41]

# # Creating plot
# fig = plt.figure(figsize=(10, 7))
# plt.pie(data, labels=cars)

# # show plot
# plt.show()

# //////////////////////////

# import requests
# response = requests.get("https://www.geeksforgeeks.org/")
# print(response.status_code)

# /////////////////////////

# import requests

# # Create a session object
# session = requests.Session()

# # Set a cookie
# session.get('https://httpbin.org/cookies')

# # Access the cookie in the next request
# response = session.get('https://httpbin.org/cookies')
# print(response.text)

# /////////////////////////

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white")

# Generate a random univariate dataset
rs = np.random.RandomState(10)
d = rs.normal(size=100)

# Plot a simple histogram and kde
sns.histplot(d, kde=True, color="m")

# Show the plot
plt.show()
