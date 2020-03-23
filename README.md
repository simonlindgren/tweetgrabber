# TWEETGRABBER

Tweetgrabber is a method for filtering and collecting tweets live via the SearchAPI. 

## Usage 

A set of valid Twitter API keys must be provided in `credentials.py`.

Start a collection job. It is recommendable to do this in a [`screen`](https://linuxize.com/post/how-to-use-linux-screen/) session.

```
$ python twg.py -p <your-project-name>
```

Use `-p` or `--project` to set the project name (default = twg).

You will be prompted to set filtering terms.

### Extract data to csv

At any point during data collection, run this to write what is currently in the database to csv.

```
$ python getdata.py -p <your-project-name>
```


### Stopping the collection

Enter the relevant `screen` session and terminate by `ctrl`+`C`, or do `ps aux | grep twg` and `kill <process id>` for the relevant process(es).


### Drastic cleanup

`$ python dbkill.py` - delete all databases in the directory.
