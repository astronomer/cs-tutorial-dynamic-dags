# Dynamic DAGs Tutorial
This proof of concept will show users how to build dynamic dags using single file methods and multiple file methods.

## Prerequisites
1. astro cli - you can install using [this quickstart guide](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart)

## Using this Repository
1. In your terminal, use `git clone git@github.com:astronomer/cs-tutorial-dynamic-dags.git` to copy this repository to your preferred project directory
2. Navigate to your newly cloned project using `cd cs-tutorial-dynamic-dags`
3. Run the astro cli command `astro dev start`
4. Open the sandbox in your web browser by navigating to http://localhost:8080

### Generating dynamic DAGs from SQL database
From here, you should see a couple of DAGs, unpause and trigger the DAG named `update_config_variable`

After the `update_config_variable` DAG has run successfully, check your Airflow variables (Admin >> Variables) for a variable named `dag_config`. This variable was generated based on values in your airflow metadatabase. These values were generated by the `initialize_config` PostgresOperator of the `update_config_variable` DAG. To see the SQL behind the values, be sure to check `/include/update_config_variable/initialize_config.sql`. **It is against best practice to store dag configs in the Airflow metadatabase. It is being done here for demonstration purposes only**. To see how Airflow parses through this `dag_config` variable, check the `/dags/dynamic-dags-variable.py` file.

To further explore updating dags dynamically based on a SQL table, try changing the `intialize_config.sql` file and re-running the `update_config_variable` DAG.

### Generating dynamic DAGs from connections
In the `dynamic-dags-connections.py` notice the `conns` defined on line 29. This method is checking for any Airflow Connections (Admin >> Connections) that are have naming containing %MY_DATABASE_CONN% (not case-sensitive). You may have noticed that there is already a DAG named `connection_hello_world_my_database_conn_1` based on the connection `my_database_conn_1`. 

To further explore creating DAGs dynamically based on connections, try adding a connection named `my_database_conn_2` and watch the DAG parse in the DAGs view

### Generating dynamic Tasks from an Airflow Variable
In the `dynamic-dags-variable.py` notice the `dynamic_tasks` Task Group. These tasks are dynamically generated from the `task_number` variable.

To further explore creating Tasks dynamically, try changing the variable named `task_number` (Admin >> Variables) from 3 to a higher number. After updating the variable, check `dag_file_1`, `dag_file_2`, or `dag_file_3` to see the number of tasks in the `dynamic_tasks` group change to your specified number
