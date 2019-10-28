# -*- coding: utf-8 -*-

import datetime

from fyodorpizza.models import Order


class GetStatistics(object):
    """
    Gets statistics on :term:`Pizza` ordered today.

    .. literalinclude:: user_stories/get_statistics.feature
      :language: gherkin

    .. versionadded:: 0.1.0
    """

    def __call__(self):
        """Method to call when a user wants to see statistics."""
        today = datetime.datetime.today()
        day_ago = today - datetime.timedelta(hours=24)
        orders_today = Order.objects.filter(creation_date__gte=day_ago)

        return (
            self.get_stats_all(orders_today),
            self.get_stats_by_pizza(orders_today),
            self.get_stats_by_status(orders_today),
        )

    def get_stats_by_status(self, orders):
        """Get statistics on orders divided by status."""
        status_choices = Order._meta.get_field('status').choices  # noqa: WPS437
        statuses = [choice[0] for choice in status_choices]
        by_status = dict.fromkeys(statuses)
        for status in statuses:
            by_status[status] = orders.filter(status=status).count()
        return by_status

    def get_stats_by_pizza(self, orders):
        """Get statistics on orders divided by pizza type."""
        by_pizzas = {}
        for order in orders:
            for pizza in order.pizza_list.all():
                try:
                    by_pizzas[pizza.id] += 1
                except KeyError:
                    by_pizzas[pizza.id] = 1
        return by_pizzas

    def get_stats_all(self, orders):
        """Get statistics on all orders."""
        return orders.count()
