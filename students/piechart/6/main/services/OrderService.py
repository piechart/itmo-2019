def count_by_status(orders, status):
    filtered = filter(lambda order: str(order.status) == str(status), orders)
    return len(list(filtered))
