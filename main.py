import types


class FlatIterator:

    def __init__(self, list_of_list):
        self.main_list = list_of_list
        self.start_main_list = 0
        self.end_main_list = len(self.main_list)

        self.inner_list = None
        self.start_inner_list = None
        self.end_inner_list = None

        self.inner_item = None
        self.next_inner_list = True  # Флаг перехода в следующий внутренний список

    def __iter__(self):
        return self

    def get_next_inner_item(self):
        """
        Получение внутреннего списка из основного списка.
        """
        if self.start_main_list == self.end_main_list:
            raise StopIteration

        self.inner_list = self.main_list[self.start_main_list]
        self.start_inner_list = 0
        self.end_inner_list = len(self.inner_list)

        self.next_inner_list = False
        self.start_main_list += 1

    def get_inner_item(self):
        """
        Получение элемента из внутреннего списка.

        :return: Next item
        """
        if self.start_main_list <= self.end_main_list:
            self.inner_item = self.inner_list[self.start_inner_list]
            self.start_inner_list += 1
        # Если внутренний список закончился, то переход к следующему внутреннему
        if self.start_inner_list == self.end_inner_list:
            self.next_inner_list = True
        return self.inner_item

    def __next__(self):
        if self.next_inner_list:
            self.get_next_inner_item()
        if not self.next_inner_list:
            return self.get_inner_item()


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


def flat_generator(list_of_lists):
    for inner_list in list_of_lists:
        for item in inner_list:
            yield item


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


class FlatIteratorAnyNesting:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        return self

    def __next__(self):
        ...
        return item


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIteratorAnyNesting(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIteratorAnyNesting(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


def flat_generator_any_nesting(list_of_list):
    """
    Генератор для вложенных списков.
    Если элемент списка - список, то он рекурсивно перебирает его.
    Иначе возвращаем этот элемент.
    """
    for elem in list_of_list:
        if isinstance(elem, list):
            for item in flat_generator_any_nesting(elem):
                yield item
        else:
            yield elem


def test_4():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator_any_nesting(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator_any_nesting(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None,
                                                                 '!']

    assert isinstance(flat_generator_any_nesting(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
