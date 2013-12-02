# coding: utf-8

'''
Version: 0.1

author: chipiga86@mail.ru
'''

import json

from unittest import TestCase

# not used
_json = '''
    [{"value":0,"x":1,"y":2},{"value":4,"x":3,"y":2},
    {"value":2,"x":3,"y":4},{"value":1,"x":1,"y":5},
    {"value":6,"x":3,"y":5},{"value":1,"x":1,"y":4}]
'''


VALID = 1
INVALID = 0


def check_matrix(json_str):

    def _sanitize(json_str):
        '''
        Валидации
        '''
        try:
            # десериализуем json-строку в python-объект
            cells = json.loads(json_str)
        except ValueError:
            raise Exception('Json is invalid')

        if not cells:
            raise Exception('No elements of matrix')

        if not isinstance(cells, list):
            raise Exception("Json isn't a list")

        try:
            for cell in cells:
                tmp = int(cell['x'])
                if tmp < 0:
                    raise Exception("x can't be negative")
                tmp = int(cell['y'])
                if tmp < 0:
                    raise Exception("y can't be negative")
                int(cell['value'])
        except KeyError:
            raise Exception('No key. x, y, value are expected')
        except ValueError:
            raise Exception('Invalid value. Only numeric values are excepted')

        return cells

    '''
    Функция проверки: совпадает ли сумма ячеек (кроме последней)
    в столбце матрицы со значением в последней ячейке столбца
    '''
    sums = {}
    tots = {}

    cells = _sanitize(json_str)

    # находим глубину матрицы
    # мы не уверены, что присутствуют значения всех элементов
    # матрицы, поэтому определим глубину заранее
    depth = max([cell['y'] for cell in cells])

    # накопим сведения о сумме в ячейках
    # и o значениях в последней ячейке
    for cell in cells:
        x = cell['x']
        sums.setdefault(x, 0)
        tots.setdefault(x, 0)
        if cell['y'] == depth:
            tots[x] = cell['value']
        else:
            sums[x] += cell['value']

    # проведем сравнения и отдадим результат
    return json.dumps([
        {'x': key, 'correct': VALID if value == tots[key] else INVALID}
        for key, value in sums.iteritems()
    ])


class TestCheckMatrix(TestCase):

    @classmethod
    def setUpClass(cls):
        print "Let's go!"

    @classmethod
    def tearDownClass(cls):
        print "\nFinish ;)"

    def test_sum_equiv(self):
        '''
        |1|
        |1|
        |2|
        '''
        expect = {'x': 1, 'correct': 1}
        actual = json.loads(
            check_matrix(
                '[{"value":1,"x":1,"y":1},{"value":1,"x":1,"y":2},'
                '{"value":2,"x":1,"y":3}]'))

        self.assertEqual(len(actual), 1)
        self.assertEqual(expect['x'], actual[0]['x'])
        self.assertEqual(expect['correct'], actual[0]['correct'])

    def test_sum_not_equiv(self):
        '''
        |0|
        |1|
        |2|
        '''
        expect = {'x': 1, 'correct': 0}
        actual = json.loads(
            check_matrix(
                '[{"value":0,"x":1,"y":1},{"value":1,"x":1,"y":2},'
                '{"value":2,"x":1,"y":3}]'))

        self.assertEqual(len(actual), 1)
        self.assertEqual(expect['x'], actual[0]['x'])
        self.assertEqual(expect['correct'], actual[0]['correct'])

    def test_last_cell_is_absent(self):
        '''
        |0, |
        | ,1|
        '''
        expect = {'x': 1, 'correct': 1}
        actual = json.loads(
            check_matrix('[{"value":0,"x":1,"y":1},{"value":1,"x":2,"y":2}]'))

        self.assertEqual(len(actual), 2)
        self.assertEqual(expect['x'], actual[0]['x'])
        self.assertEqual(expect['correct'], actual[0]['correct'])

    def test_prev_cell_is_absent(self):
        '''
        |0, |
        | ,1|
        '''
        expect = {'x': 2, 'correct': 0}
        actual = json.loads(
            check_matrix('[{"value":0,"x":1,"y":1},{"value":1,"x":2,"y":2}]'))

        self.assertEqual(len(actual), 2)
        self.assertEqual(expect['x'], actual[1]['x'])
        self.assertEqual(expect['correct'], actual[1]['correct'])

    def test_one2one_matrix(self):
        '''
        |1|
        '''
        expect = {'x': 1, 'correct': 1}
        actual = json.loads(check_matrix('[{"value":0,"x":1,"y":1}]'))

        self.assertEqual(expect['x'], actual[0]['x'])
        self.assertEqual(expect['correct'], actual[0]['correct'])

    def test_no_cells(self):
        with self.assertRaisesRegexp(Exception, 'No elements'):
            check_matrix('[]')

    def test_json_isnot_list(self):
        with self.assertRaisesRegexp(Exception, "isn't a list"):
            check_matrix('{"value":0,"x":1,"y":1}')

    def test_x_isnot_numeric(self):
        with self.assertRaisesRegexp(Exception, 'Only numeric'):
            check_matrix('[{"value":0,"x":"invalid","y":1}]')

    def test_y_isnot_numeric(self):
        with self.assertRaisesRegexp(Exception, 'Only numeric'):
            check_matrix('[{"value":0,"x":1,"y":"invalid"}]')

    def test_value_isnot_numeric(self):
        with self.assertRaisesRegexp(Exception, 'Only numeric'):
            check_matrix('[{"value":"invalid","x":1,"y":1}]')

    def test_no_x(self):
        with self.assertRaisesRegexp(Exception, 'No key'):
            check_matrix('[{"value":0,"y":1}]')

    def test_no_y(self):
        with self.assertRaisesRegexp(Exception, 'No key'):
            check_matrix('[{"value":0,"x":1}]')

    def test_no_value(self):
        with self.assertRaisesRegexp(Exception, 'No key'):
            check_matrix('[{"x":0,"y":1}]')

    def test_negative_x(self):
        with self.assertRaisesRegexp(Exception, "x can't be negative"):
            check_matrix('[{"value":0,"x":"-1","y":1}]')

    def test_negative_y(self):
        with self.assertRaisesRegexp(Exception, "y can't be negative"):
            check_matrix('[{"value":0,"y":"-1","x":1}]')

    def test_invalid_json(self):
        with self.assertRaisesRegexp(Exception, 'Json is invalid'):
            check_matrix('')
