@Pengfei Cai 

### Summary

In the source code, following key steps are designed to realize the validation:

1. Get the window size.
2. Read and store the actual prices and predicted prices into two seperate lists.
3. Get the stock ID and actual price for hour H, then save them into a dictionary.
4. Process the predicted price of the hour H, then calculate the sum of the absolute difference values and number of the valid stocks.
5. Save the tuple (number of the stocks, the sum of differences) of each hour H in a list. 
6. Go back to step 3 if there are still unprocessed price information in the two lists.
7. Calculate the average difference for each time window and print the results.


