# Prencencia

Attendance System with Face Recognition Technology. Built using Tensorflow, OpenCV, Flask Microframework.


## Method

<img src="./plot/architecture.png" />


## Run Locally

Step-by-step to run locally:
1. Fork or clone this repository.
2. Rename the ```.env.example``` file, change to ```.env``` and input all the configurations for admin and database.
3. Create a MySQL database where the database name should be the same as the one that has been written on the .env configuration file.
4. Create a virtual environment.
5. Activate the virtual environment.
6. Install all packages required in the requirements.txt file by using ```pip install -r requirements.txt```.
7. Migrate the table from migrations folder to the database by using ```flask db upgrade```.
8. Run the seeder to seed the **roles** and **admin** by using ```flask seed role``` and ```flask seed admin``` command.
9. To run it locally, use command ```flask run``` and you're good to go. 
10. Access the website by opening http://127.0.0.1:5000 to open the attendance check-in and check-out feature. To access the admin side you need to open http://127.0.0.1:5000/admin.


## License

[MIT](./LICENSE)
