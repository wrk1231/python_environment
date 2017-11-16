import tensorflow as tf
import sys
my_graph = tf.Graph()
with tf.Session(graph = my_graph) as sebi1:
    x = tf.constant([1,3,6])
    y = tf.constant([1,1,1])
    op = tf.add(x,y)
    result = sebi1.run(fetches = op)
    print result
    print sys.version