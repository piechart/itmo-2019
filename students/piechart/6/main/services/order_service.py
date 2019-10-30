# -*- coding: utf-8 -*-


def count_by_status(orders, status):
    """Filters array of orders by status and returns its length."""
    filtered = []
    s2 = str(status)
    for order in orders:
        s1 = str(order.status)
        if s1 == s2:
            filtered.append(order)
    return len(list(filtered))
