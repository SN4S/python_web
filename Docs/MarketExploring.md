# Initial domain research for a food ordering system with limited and rare ingredients
## 1. Analysis of existing systems

### In the field of online food ordering, there are several systems that can have similar functionality, but the specifics of working with limited ingredients and dynamic menus are quite unique. Here are some famous examples of systems:

- **Uber Eats, Glovo:** These services allow restaurants to sell food online, but they are not adapted to work with ingredients that are in limited quantities or change availability after each order.
- **Seasonal Restaurant Platforms:** Platforms that offer a seasonal menu that changes depending on the availability of ingredients. For example, such services are used in fine dining restaurants, but most of them do not have the ability to dynamically update the menu based on the composition after each order. 
- **Farm-to-table systems:** They work based on the availability of seasonal and local products, but mostly update the menu every week or even less often. 

## 2. Functionality that may be needed

### A system for a restaurant with limited ingredients requires a special set of features that go beyond standard online ordering systems. Here is the main functionality:

- **Dynamic menu:** The menu should change automatically based on the availability of ingredients after each order. The system must instantly react to a reduction in the number of ingredients and remove dishes from the menu when they cannot be prepared.
- **Ingredient Inventory Management:** The system should track the availability of ingredients in real time and display their status to the kitchen. This will ensure accurate menu updates.
- **Booking meals ahead of time:** Since certain ingredients may not be available for a long time, it is important to give customers the ability to book meals several months in advance. This will help plan deliveries and prepare customer orders.
- **Integration with supplies:** Automation of ordering ingredients from suppliers. For example, the system can automatically send orders when the amount of ingredients drops below a certain level.
- **Notifying customers of menu changes:** Customers should receive instant notifications if their order cannot be filled due to ingredient shortages or if new dishes are available.
- **Customer account:** Customers can view their order history, reservations and receive information about ingredient availability in real time.
- **Flexible management of dishes:** The restaurant can manually regulate the availability of certain dishes, especially in the case of complex gastronomic masterpieces that require advance preparation. 

## 3. Technical implementation

### Several key elements are required to implement this functionality:

- **Database:** Creation of a relational database to store information about ingredients, dishes, their interactions (the relationship between ingredients and dishes), orders, stock status and reservations.
- **Backend:** The server part that will handle the order, ingredient and menu management logic. The most common options for developing the back-end part: Node.js , Django or Flask .
- **Frontend:** User interface for customers and administrators. For its implementation, you can use React , Vue.js or Angular . The interface should be convenient and responsive for mobile devices.
- **Automatic menu update:** Integration of a dynamic menu generation mechanism taking into account changes in the availability of ingredients. This can be implemented via WebSocket or push notification technologies to instantly update the client interface.
- **Notification system:** Implementation of mail or mobile notifications to inform customers about changes in their orders or menu. 

## 4. Competitive advantages and opportunities for development

- **Uniqueness in the use of rare ingredients:** This system is suitable for restaurants that offer rare or seasonal dishes, which is a big marketing plus.
- **Personalized customer experience:** Future bookings, personalized notifications and unique meals can make the customer experience memorable.
- **Automation of processes:** Automatic inventory management and menu updates reduce the human factor and minimize the risk of errors. 