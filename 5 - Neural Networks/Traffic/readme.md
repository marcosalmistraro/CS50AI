# 5. Traffic

In this project I used TensorFlow to build a **neural network** with the aim to classify road signs based on previously existing training data.
The model is based on the German Traffic Sign Recognition Benchmark (GTSRB) dataset, which contains thousands of images of 43 different kinds of road signs.

## Usage

`$ python traffic.py gtsrb`

## Comments on the implementation of the ANN

A first run of the model was performed by implementing the following layer structure:

- Conv2D 
- MaxPool2D
- Flatten
- Dropout
- Final classification layer with the ‘softmax’ activation function.

This yielded an accuracy of 0.8805. In order to improve such metric, I tried to increase the `pool_size` parameter to (4,4). This did not turn out to be a great idea, as it brought down the accuracy to 0.7317, probably due to the excessive amount of details carried onto the network’s further layers.

I then brought back `pool_size` to (2, 2) and tried doubling the number of Conv2D and MaxPool2D layers. This increased the accuracy by a fair amount, leading to 0.9413. In this case, the architecture was the following:

- Conv2D
- MaxPool2D 
- Conv2D
- MaxPool2D
- Flatten
- Dropout
- Final classification layer

The main rationale here was to extract more solid features in the images fed to the network.

Adding a Dense Layer (32 units) before the flattening operation gave a terribly lowered accuracy of 0.0535. I suspect that the number of nodes was way too low for sufficient information to be carried over to the classification task, causing some sort of ‘bottleneck’ issue.
As such, I tried modifying the number of Dense nodes to 128, reaching an accuracy of 0.9673, with an average computational time of 11 seconds per epoch.

I then dramatically increased the number of the units on the same layer to 256, in the hope of getting a better result. Maybe this time the dense layer would have been capable of better leveraging the features extracted at the earlier steps.
As it turns out, I did not get a better accuracy value, reaching instead an accuracy of 0.9582.

I started to experiment with the number of filters (setting it to 64 for each of the two convolutional layers). This yielded an accuracy of 0.9226, slightly lower than before, but with dramatically increased computational times, up to 44 seconds per epoch.

I finally restored the `filters` parameter to a value of 32 and added a second dense layer with 128 nodes before the classification layer. This time I reached an accuracy of 0.9420.  A second run of the model gave an accuracy of 0.9422.

As such, I eventually decided to settle for the following network structure:

- Conv2D 
- MaxPool2D
- Conv2D
- MaxPool2D
- Flatten
- Dense
- Dropout
- Final classification layer with the ‘softmax’ activation function.

A last run of the model in this configuration gave an accuracy of 0.9691.
