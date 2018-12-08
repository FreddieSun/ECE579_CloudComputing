import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def get_label(line):
    '''
    Write a function to take a number as input.
    Process the input to return a (key, value) pair,
    such that key = label = positive, negative or zero depending
    upon the input. Value is always 1.
    '''
    try:
        pt = [float(i) for i in line.split()] # get point
    except:
        print 'Invalid input'
        return ('Invalid points', 1)

    # Your code starts here

    return (label, 1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise IOError("\nInvalid usage; enter correct format: \n example.py <hostname> <port>")

    # Initialize a SparkContext with a name
    sc = SparkContext(appName="Stream-Example")

    # Create a StreamingContext with a batch interval of 1 seconds
    stc = StreamingContext(sc, 1)

    # Use Checkpointing feature
    # Required for updateStateByKey
    stc.checkpoint("checkpoint")

    # Create a DStream to connect to hostname:port (like localhost:9999)
    lines = stc.socketTextStream(sys.argv[1], int(sys.argv[2]))

    # Function  used to update the current counts
    updateFunc = lambda new_vals, current_count: sum(new_vals) + (current_count or 0)

    # Update all the current counts of labels
    # Get (Key, Value) pair, sum the Value list
    # Add the sum to current count of labels.
    # In our case the value list will have one item only.
    state = lines.map(get_label).updateStateByKey(updateFunc)

    # Print the current state
    state.pprint()

    # Start the computation
    stc.start()

    # Wait for the computation to terminate
    stc.awaitTermination()
