# Point-Of-Sale-SE-project
CLASS DIAGRAM

<img width="3261" height="1611" alt="POS_class_diagram" src="https://github.com/user-attachments/assets/e14651b1-e2a3-4998-ae69-d3874e76d5f7" />

DATABASE DIAGRAM

<img width="798" height="1091" alt="POS_django_models" src="https://github.com/user-attachments/assets/cc58465d-db50-4ac4-bb4e-b5fb61f6be47" />

Django based with PostgreSQL database project.

## TO DO:
1. Logic for pick up dates (now placeholders) in Waiter
2. Logic for creating an order with notes already?
3. Recreate the UML class diagrams:
	-incorporate the visibility
	-add id logic static method
	-order_id now an int from 1 to 99
	-ServingRule modified?
	-maybe add new methods related to custom dashboard views etc
4. Manager report creation
5. Manager database report viewing
6. In OrderCreationPanel, _confirm(self) what exactly?
7. Possibly rewrite the logic behind adding items to the order, link it to OrderService
8. FILTER and PERIOD in ReportingService, what are those arguments exactly? need to link them to input from GUI probably
9. manager adding employees? (because django admin is like an IT guy they hired to just set things up, they're not really a proper restaurant employee)
10. html -> css??? maybe
11. actual logic that will come with more models and views and the dashboards being developed further


