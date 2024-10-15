# Description of basic entities of "c0vid bat" online food delivery

## 1. Ingridient

List of avaliable ingridients for preparing dishes.

**Atributes:**

- **ID:** Unique identifier of ingridient.
- **Name:** Name of ingridient.
- **Description:** Detailed description of the ingridient.
- **Date Of Delivery:** Delivery date of the last batch of ingridients.
- **Expiration Date:** Expiration date of the last batch of ingridients.
- **Count:** Remaining ingredients in stock.

## 2. Dish

List of available dishes accounting ingredients.

**Atributes:**

- **ID:** Unique identifier of dish.
- **Name:** Name of dish.
- **Description:** Detailed description of the dish.
- **Ingridients:** List of ingridients used in dish.
- **Availability:** Describes dish availability at the moment.

## 3. Order

List of orders made by users.

**Atributes:**

- **ID:** Unique identifier of order.
- **UserID:** Identifier of user that ordered dishes.
- **Dishes list:** List of ordered dishes.
- **Date/Time of order:** Exact time when order was made.
- **Reservation date:** Option to made reservation of specific dish on specific date.
- **Delivery address:** Address for order delivering.
- **Status:** Order status.

## 4. User

List of registered users

- **ID:** Unique identifier of user.
- **Email:** User email for password restoring and logging in.
- **Phone:** Phone number of user.
- **Login:** User login for logging in.
- **Password:** Password hash for more security.
- **Role:** Role of user. Can be admin or just user.

---

# Main Usage Scenarios

## Scenario 1: Adding a new ingredient

**Steps:**

1. The administrator logs in and selects the option to add a new ingredient.
2. Fill in the ingredient information:
    - Name
    - Description
    - Date of Delivery
    - Expiration date
    - Count
3. The system generates a unique identifier or updates old ingridient.
4. The system updates the availability of dishes in the menu where this ingredient is key.

## Scenario 2: Update ingredient availability after ordering

**Steps:**

1. The customer places an order for a certain dish through the system.
2. The system checks the presence of all the necessary ingredients for the selected dish.
3. After confirming the order, the system automatically reduces the amount of ingredients used to prepare the dish.
4. If the amount of any ingredient drops to 0, the system automatically removes dishes from the menu where this ingredient is mandatory.
5. The administrator receives a notification about the need to replenish stocks, if the amount of ingredients is critically low.

## Scenario 3: Updating the status of a customer's order

**Steps:**

1. The customer places an order through the system.
2. The administrator or the system automatically updates the status of the order (for example, "Accepted", "Preparing", "Ready to ship").
3. The customer receives a notification about the change in the status of the order.
4. The client can view the current status of his order in his personal account.

## Scenario 4: Customers view a dynamic menu

**Steps:**

1. The client enters the restaurant's website or application.
2. The system shows the menu based on the current availability of ingredients.
3. If certain dishes are no longer available due to lack of ingredients, they are not displayed on the menu.
4. The client views the available dishes and makes an order or reservation.
5. The system updates the menu after each order to reflect the current availability of ingredients.


# Possible Project implementation stages

## Stage 1: System design

- Requirements gathering and analysis
- Development of the system architecture
- Creating a data model and database structure

## Stage 2: Initial implementation of functionality

- Implementation of basic functions for working with ingredients
- Implementation of a dynamic menu
- Create a simple admin interface

## Stage 3: Adding functions of orders and reservations

- Implementation of the ordering function
- Implementation of reservation of meals for the future
- User notifications

## Stage 4: Testing and tuning

- Functional testing
- User Interface Testing
- Performance optimization

## Stage 5: Implementation and launch

- Configuring the server environment
- Launching the system for end users
- Monitoring and support

---
