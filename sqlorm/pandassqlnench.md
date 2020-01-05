## An Attempt to Benchmark Data Read Write with Pandas
### Objective 

Objective of this excercise is to test the perfromance of Read and Write data with Pandas.

System Spec:

    - OS : Ubuntu 16.04
    - CPU : 8
    - RAM : 16
    - Python : 3.7
    - PostgreSQL : 9.5.19
    - Pandas : 0.25.0
    - SQLAlchemy : 1.2.19

### Data Used

    - https://www.kaggle.com/deeiip/1m-real-time-stock-market-data-nse/version/3#log_inf.csv

Total records in the data - 916722.

Number of columns in the table - 21

### Results
 ** Time in Minutes 

| Run No | tosql | read_sql_table | read_sql | sql_alchemy | read_sqlalch+pandas | to_sql+multi |
|--------|-------|----------------|----------|-------------|---------------------|--------------|
| 1      | 2.50  | 0.13           | 0.13     | 3.30        | 0.15                | 6.30         |
| 2      | 2.42  | 0.13           | 0.14     | 3.40        | 0.13                | 5.59         |
| 3      | 2.32  | 0.13           | 0.13     | 2.47        | 0.13                | 5.44         |
| 4      | 2.28  | 0.13           | 0.13     | 2.46        | 0.13                | 5.31         |
| 5      | 2.30  | 0.13           | 0.13     | 2.48        | 0.13                | 5.35         |

    - to_sql with multi and chunksize 10000 
    - Avg wrie time with to_sql 2.36
    - Avg write time with SQLAlchemy ORM Models - 2.82
    - to_sql with multi write time 5.6