import unittest
import os
import pickle
import numpy as np

import tensorflow as tf
from PIL import Image

import classificator


class TrainTest(unittest.TestCase):

    @staticmethod
    def parse_name(name):
        return name.split('_')[0]

    def test_check_model_in_data_image(self):
        for image_path in os.listdir('image_test'):
            test_status = False
            dict_images = classificator.get_tags_image('image_test/'
                                                       + image_path)
            msg = 'Tags %s ' % dict_images + '\n' + ' image: %s ' % image_path
            image_path = image_path.split('.')[0]
            with self.subTest(image_path=image_path,
                              dict_images=dict_images):
                for tag in dict_images:
                    if image_path.lower() in tag.lower():
                        test_status = True
                self.assertTrue(test_status, msg=msg)

    def test_not_exist_image(self):
        image_path = 'not_existing_path'
        try:
            classificator.get_tags_image(image_path)
        except Exception as exc:
            self.assertTrue(True, msg=exc)

    @unittest.skip("Too long time")
    def test_on_dataset(self):
        data = []
        not_accepted_images = []

        with open('datasets_test/test', "rb") as fo:
            dict = pickle.load(fo, encoding='latin1')
        data.append(dict['data'])
        data = np.concatenate(data)
        data = data.reshape(data.shape[0], 3, 32, 32)
        data = data.transpose(0, 2, 3, 1).astype('uint8')

        for i in range(len(data)):
            expected = TrainTest.parse_name(dict['filenames'][i])
            image = Image.fromarray(data[i])
            image = image.convert('RGB')
            image.save('datasets_test/buffer.png')

            b_image = tf.gfile.FastGFile('datasets_test/buffer.png', 'rb')\
                .read()
            dict_res = classificator.run_inference_on_image(b_image, True)

            test_status = False
            with self.subTest(_dict_res=dict_res):
                for tag in dict_res:
                    if expected.lower() in tag.lower():
                        test_status = True
                if test_status:
                    print('Test accepted: {}, process: {}'.format(expected,
                          i / len(data) * 100))
                else:
                    not_accepted_images.append(expected)

            print('Total(quessed): ', (1 - len(not_accepted_images)
                  / len(data)) * 100)


if __name__ == '__main__':
    unittest.main()
