# Airflow 2to3

A small package based on [LibCST](https://github.com/Instagram/LibCST) to fix deprecations in Airflow 2 that were removed in Airflow 3.


## Installation

```
pip install -r requirements.txt
```

## Writing codemod

https://libcst.readthedocs.io/en/latest/codemods_tutorial.html

## Usage

```
python -m libcst.tool list

dag_fixer.DagFixerCommand - Fixes deprecation warning and removals related to DAG construction.
task_fixer.OperatorFixerCommand - Fixes deprecation warning and removals related operators.
```

Use `-u` option to print diff instead of updating the file

```
python -m libcst.tool codemod dag_fixer.DagFixerCommand -u 1 tests/test_dag.py
Calculating full-repo metadata...
Executing codemod...
reformatted -

All done!
1 file reformatted.
--- /home/karthikeyan/stuff/python/libcst-tut/tests/test_dag.py
+++ /home/karthikeyan/stuff/python/libcst-tut/tests/test_dag.py
@@ -10,6 +10,6 @@
     dag_id="my_dag_name",
-    default_view="tree",
+    default_view="grid",
     start_date=datetime.datetime(2021, 1, 1),
-    schedule_interval="@daily",
-    concurrency=2,
+    schedule="@daily",
+    max_active_tasks=2,
 ):
@@ -23,5 +23,4 @@
     start_date=datetime.datetime(2021, 1, 1),
-    schedule_interval=EventsTimetable(event_dates=[datetime.datetime(2022, 4, 5)]),
+    schedule=EventsTimetable(event_dates=[datetime.datetime(2022, 4, 5)]),
     max_active_tasks=2,
-    full_filepath="/tmp/test_dag.py"
 )
Finished codemodding 1 files!
 - Transformed 1 files successfully.
 - Skipped 0 files.
 - Failed to codemod 0 files.
 - 0 warnings were generated.
```

## TODO

* Only one codemod command is allowed per file. Should allow running all codemods at once on the file.
