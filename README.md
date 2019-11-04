# Decision_Tree

Decision Tree is very powerful tool in machine learning. It is widely used by people both in regression and classification.

There are many applied version of it like Random Forest and XGboost. They are leading algorithms in machine learning world.

Before we dive into a decision tree, we should know about information entropy.

[1]img1
![equation](https://github.com/hyun11732/Decision_Tree/blob/master/image/img1.JPG)

We can think this entropy same as a entropy we learned in physics.
If a value of entropy is high, there is less purity and organized and vice versa.
If data is organized and high purity, it will look like this. We can clearly distinct this data to two class.

![equation](https://github.com/hyun11732/Decision_Tree/blob/master/image/img2.JPG)

In this implementation, I used "Gini", another measure of information entropy.

![equation](https://github.com/hyun11732/Decision_Tree/blob/master/image/img3.JPG)

"Gini" has a reverse relationship with information entropy. If gini is high, the data has high purity.

Now, let's see how a decision tree is made.
First, if it is a categorical data. We calculate all gini like this.

![equation](https://github.com/hyun11732/Decision_Tree/blob/master/image/img4.JPG)

D = all data, D1 = splited1, D2 = splited2

We calculate this gini for all factors and find out which factor has the highest gini.
The factor which has the highest gini will be selected for the split. Then the data will be split based on the factor chosen.

This process will be continued until the height we want or there are no data left.
