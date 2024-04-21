
In general, the more layers I added, the more accuracy I saw. But it also came with the cost
of increased duration of program run time. Adding more convolutional layers seem to increase the accuracy than adding more hidden layers. With two convolutional layers and one hidden layer (256 unites in the hidden layer), I received 0.9773 accuracy. This was the best accuracy I received.

When I increase the number of filters, from 32 to 64, in the convolutional layer the accuracy seemed to have reduced a bit to 0.9629. When I increaed the max pool size from 2X2 to 4X4, the job ran quicker but the accuracy reduced to about 0.80.

I had the worst accuracy, 0.5,  when I increased the dropout to 0.8, which makes sense as
we may be ignoring excessive amount of data.

I also found that 128 units in a hidden layer is way less accurate than 256 units, about 20%.

When I tried with two convolutional pools and three hidden layers, I received .9680 accuracy 
but the job ran the longest, for about 5 minutes.



