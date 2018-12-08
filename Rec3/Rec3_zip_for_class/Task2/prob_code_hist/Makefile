# add username
USER = myname

EXAMPLE_DIR = /user/$(USER)/hist
INPUT_DIR   = $(EXAMPLE_DIR)/input
OUTPUT_DIR  = $(EXAMPLE_DIR)/output
OUTPUT_FILE = $(OUTPUT_DIR)/part-00000
PARAMS_FILE = $(EXAMPLE_DIR)/params
# add hadoop version
HADOOP_VERSION = 2.8.1

# check $HADOOP_HOME with echo $HADOOP_HOME
TOOLLIBS_DIR=$(HADOOP_HOME)/share/hadoop/tools/lib/
NITERS=25

run: inputs
	hdfs dfs -rm -f -r $(OUTPUT_DIR) 
	hadoop jar $(TOOLLIBS_DIR)/hadoop-streaming-$(HADOOP_VERSION).jar \
		-files ./mmm-map.py,./mmm-combine.py,./mmm-reduce.py \
		-mapper ./mmm-map.py  -combiner ./mmm-combine.py \
	        -reducer ./mmm-reduce.py \
		-input $(INPUT_DIR) \
		-output  $(OUTPUT_DIR)
	hdfs dfs -cat $(OUTPUT_FILE) > mmm
	cat mmm 
	hdfs dfs -rm -f -r $(OUTPUT_DIR) 
	hadoop jar $(TOOLLIBS_DIR)/hadoop-streaming-$(HADOOP_VERSION).jar \
		-files ./hist-map.py,./hist-combine-reduce.py,./nbins,./mmm \
		-mapper ./hist-map.py  -combiner ./hist-combine-reduce.py \
	        -reducer ./hist-combine-reduce.py \
		-input $(INPUT_DIR) \
		-output  $(OUTPUT_DIR) 
	hdfs dfs -cat $(OUTPUT_FILE) | sort -n > hist
	cat hist

directories:
	hdfs dfs -test -e $(EXAMPLE_DIR) || hdfs dfs -mkdir $(EXAMPLE_DIR)
	hdfs dfs -test -e $(INPUT_DIR) || hdfs dfs -mkdir $(INPUT_DIR)
	hdfs dfs -test -e $(OUTPUT_DIR) || hdfs dfs -mkdir $(OUTPUT_DIR)


input/small-data.dat: data.py
	./data.py --npts=5000 > $@

inputs: directories input/small-data.dat 
	hdfs dfs -test -e $(INPUT_DIR)/small-data.dat \
	  || hdfs dfs -put input/small-data.dat $(INPUT_DIR)/small-data.dat

clean:
	-hdfs dfs -rm -f -r $(INPUT_DIR)
	-hdfs dfs -rm -f -r $(OUTPUT_DIR)
	-hdfs dfs -rm -f -r $(EXAMPLE_DIR)
	-rm -f mmm hist

.PHONY: directories inputs clean run 
