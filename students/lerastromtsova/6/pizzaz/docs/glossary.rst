############
Glossary
############

.. glossary::
   Pizza
      name, price, ingredient_list: [:term:`Ingredient`]

   Ingredient
      name

   Order
      creation_date, status (enum: принято, готовится, в пути, доставлено), pizza_list: [:term:`Pizza`], delivery_address, client_email
