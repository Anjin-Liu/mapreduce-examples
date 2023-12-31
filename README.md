MapReduce code for a variety of tasks written in python (2.7).

Following the MapReduce programming model, all the `mapper.py` files perform the **filtering** (typically creating key/value pairs).
All the `reducer.py` files peform the **summary operation** (typically the maths, when required).

# Examples TOC

The CAPTIALISED words indicate how the examples could be used in a more generalised setting:

- **TALLY=word_frequencies**: Returns the frequency of words in a text file(s).
- **MAX=max_value_by_store**: Returns the cost of the item that is most expensive, for each location.
- **COUNT and SUM=count_and_sum**: Returns the total number of sales and the total sales value from all the stores.
- ToDo: Add more design patterns such as those discussed in lesson 4 (i.e. filltering patterns, summarisation patterns, structural patterns).

# Usage

## Bash

A quick and useful way to test MapReduce jobs is via the command line using a smaller dataset.

```
# Create sample (random 50 lines)
shuf -n 50 all_data.txt > testfile

# Test mapper
cat testfile | ./mapper.py

# Test MapReducer job
cat testfile | ./mapper.py | sort | ./reducer.py
```

## Hadoop Streaming

Haddop Streaming allows you to write MapReduce code in any language you like.

To run the code (this is based on running such code in the Udacity VM built as part of the "Intro to Hadoop and MapReduce course" - see [instructions here](https://docs.google.com/document/d/1v0zGBZ6EHap-Smsr3x3sGGpDW-54m82kDpPKC2M6uiY/pub?embedded=true)):

```
hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py -input INPUT_DIR -output OUTPUT_DIR
```

Alternatively, add an alias defined to `~/.bashrc`:

```
run_mapreduce() {
        hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar -mapper $1 -reducer $2 -file $1 -file $2 -input $3 -output $4
}

alias hs=run_mapreduce
```

and run with `hs mapper.py reducer.py INPUT_DIR OUTPUT_DIR`
