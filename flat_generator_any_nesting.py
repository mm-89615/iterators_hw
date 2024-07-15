import types


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

    for item in flat_generator_any_nesting(list_of_lists_2):
        print(item)

    for flat_iterator_item, check_item in zip(
            flat_generator_any_nesting(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator_any_nesting(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None,
                                                                 '!']

    assert isinstance(flat_generator_any_nesting(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_4()
