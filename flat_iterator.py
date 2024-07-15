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

    for item in FlatIterator(list_of_lists_1):
        print(item)

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()
