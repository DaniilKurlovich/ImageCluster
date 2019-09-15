import os.path
import re
import numpy as np
import tensorflow as tf


class NodeLookup(object):
    """Converts integer node ID's to human readable labels."""

    def __init__(self,
                 label_lookup_path=None,
                 uid_lookup_path=None):
        if not label_lookup_path:
            label_lookup_path = os.path.join(
                '/tmp/imagenet', 'imagenet_2012_challenge_label_map_'
                                 'proto.pbtxt')
        if not uid_lookup_path:
            uid_lookup_path = os.path.join(
                '/tmp/imagenet', 'imagenet_synset_to_human_label_map.txt')
        self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

    @staticmethod
    def parse_tags_and_index(parsed_items):
        return re.findall(r'[n\d]*[ \S,]*', parsed_items)

    def load(self, label_lookup_path, uid_lookup_path):
        """Loads a human readable English name for each softmax node.

        Args:
          label_lookup_path: string UID to integer node ID.
          uid_lookup_path: string UID to human-readable string.

        Returns:
          dict from integer node ID to human-readable string.
        """

        if not tf.gfile.Exists(uid_lookup_path):
            tf.logging.fatal('File does not exist %s', uid_lookup_path)
        if not tf.gfile.Exists(label_lookup_path):
            tf.logging.fatal('File does not exist %s', label_lookup_path)

        # Loads mapping from string UID to human-readable string
        proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()

        uid_to_human = {}
        for line in proto_as_ascii_lines:
            uid, _, human_string = NodeLookup.parse_tags_and_index(line)[0:3]
            uid_to_human[uid] = human_string

        # Loads mapping from string UID to integer node ID.
        node_id_to_uid = {}
        proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
        for line in proto_as_ascii:
            if line.startswith('  target_class:'):
                target_class = int(line.split(': ')[1])
            if line.startswith('  target_class_string:'):
                target_class_string = line.split(': ')[1]
                node_id_to_uid[target_class] = target_class_string[1:-2]

        # Loads the final mapping of integer node ID to human-readable string
        node_id_to_name = {}
        for key, val in node_id_to_uid.items():
            if val not in uid_to_human:
                tf.logging.fatal('Failed to locate: %s', val)
            name = uid_to_human[val]
            node_id_to_name[key] = name

        return node_id_to_name

    def id_to_string(self, node_id):
        if node_id not in self.node_lookup:
            return ''
        return self.node_lookup[node_id]


def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(os.path.join('/tmp/imagenet',
                                         'classify_image_graph_def.pb'),
                            'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def get_dict_predictions(image_data, count_keys):
    """
    :param image_data: binary image data
    :param count_keys: count tags of image
    :return: dict with tags and predictions
    """
    res = {}
    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)
        # Creates node ID --> English string lookup.
        node_lookup = NodeLookup()

        top_k = predictions.argsort()[-count_keys:][::-1]
        for node_id in top_k:
            human_string = node_lookup.id_to_string(node_id)
            score = predictions[node_id]
            res[human_string] = score
    return res


def run_inference_on_image(image_data, image_in_bytes=False):
    """Runs inference on an image.
    Args:
        image: Image file name.
    Returns:
        res_dict : dict with tags and value score
    """
    if not image_in_bytes:
        if not tf.gfile.Exists(image_data):
            tf.logging.fatal('File does not exist %s', image_data)
        image_data = tf.gfile.FastGFile(image_data, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    return get_dict_predictions(image_data, 5)


def get_tags_image(image_path):
    dict_tags = run_inference_on_image(image_path)
    return dict_tags
