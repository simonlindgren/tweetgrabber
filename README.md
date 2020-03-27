# TWEETGRABBER

Tweetgrabber is a method for filtering and collecting tweets live via the SearchAPI. 

## Usage 

A set of valid Twitter API keys must be provided in `credentials.py`.

Edit the `parameters.py` according to your project.

Start a collection job. It is recommendable to do this in a [`screen`](https://linuxize.com/post/how-to-use-linux-screen/) session.

```
$ python twg.py
```

A launcher bash script is provided if you want your collector to persist after any interruptions:

```
$ sh twh.sh
```


### Extract data to csv

At any point during data collection, run this to write what is currently in the database to csv.

```
$ python getdata.py -p <your-project-name>
```


### Stopping the collection

Enter the relevant `screen` session and terminate by `ctrl`+`C`, or do `ps aux | grep twg` and `kill <process id>` for the relevant process(es).


### Drastic cleanup

`$ python dbkill.py` - delete all databases in the directory.
