#!/usr/bin/env python3

class SetItem(set):
    """
    A Set of Items. It forms part of a SetList.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev = None
        self.next = None

    def copy(self):
        cp = SetItem(self)
        cp.prev = self.prev
        cp.next = self.next
        return cp

    def duplicate_after(self):
        new = self.copy()
        new.prev = self
        self.next = new
        return new

class SetList:
    """
    A LinkedList of SetItems. Has a Dictionary to find items quickly.
    """
    def __init__(self):
        self.first = None
        self.last  = None
        self.set_items = dict()

    def __iter__(self):
        self.curr = self.first
        return self

    def __next__(self):
        if self.curr is None:
            raise StopIteration
        else:
            result = self.curr
            self.curr = self.curr.next
            return result

    def create(self, item):
        curr = SetItem()
        curr.add(item)
        if item not in self.set_items:
            if not self.set_items:
                self.first = curr
                self.last  = curr
            self.set_items[item] = curr
        return curr

    def prepend(self, item):
        curr = self.create(item)
        if curr is not self.first:
            curr.next = self.first
            self.first.prev = curr
            self.first = curr
        return curr

    def append(self, item):
        curr = self.create(item)
        if curr is not self.last:
            curr.prev = self.last
            self.last.next = curr
            self.last = curr
        return curr

    def insert_before(self, item, pos):
        new = self.create(item)
        new.next = pos
        new.prev = pos.prev
        pos.prev.next = new
        pos.prev = new
        return new

    def add_sublist(self, sublist):
        curr = self.first
        prev_item = None
        for item in sublist:
            if curr is None:
                curr = self.append(item)
            else:
                if item in curr:
                    while curr.next is not None and item in curr.next:
                        curr = curr.next # go to last possible position
                else:
                    if item in self.set_items:
                        curr = self.set_items[item] # go to item
                        if prev_item in curr and not prev_item in curr.prev:
                            curr.remove(item)
                            self.set_items[item] = curr.next
                        while curr.next is not None and item in curr.next:
                            curr = curr.next # go to last possible position
                        if prev_item in curr and prev_item not in curr.next:
                            curr.remove(prev_item)
                    else:
                        curr.add(item)
                        self.set_items[item] = curr
                        curr = curr.duplicate_after()
            prev_item = item
            curr = curr.next

    def __str__(self):
        s = ""
        for set_item in self:
            s += str(set_item) + "\n"
        return s + "\n" + str(self.set_items)

if __name__ == "__main__":
    list0 = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grapes"]
    list1 = ["Apple", "Banana", "Elderberry"]
    list2 = ["Apple", "Cherry", "Elderberry"]
    list3 = ["Apple", "Date", "Elderberry"]
    sl = SetList()
    sl.add_sublist(list1)
    print(sl)
    sl.add_sublist(list2)
    print(sl)
    sl.add_sublist(list3)
    print(sl)
    new_list = []
    for si in sl:
        new_list += [ i for i in si ]
    print(new_list)

    # big_list = list(dict.fromkeys(list1 + list2 + list3)) # remove duplicates
    # print(big_list)
    #
    # for lst in [list3, list2, list1]:
    #     prev_idx = -1
    #     for item in lst:
    #         idx = big_list.index(item)
    #         if idx < prev_idx:
    #             big_list.insert(prev_idx, big_list.pop(idx))
    #             prev_idx += 1
    #         else:
    #             prev_idx = idx
    #     print(big_list)
