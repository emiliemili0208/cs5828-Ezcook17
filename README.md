# CSCI_5828_WebProject

### Setup Django Environment

> Thanks to [Django Girls Tutorial](https://tutorial.djangogirls.org/en/installation/)

1. Setup Virtual Environment in HOME directory
```
$ mkdir <directory_name>
$ cd <directory_name>
$ python3 -m venv <virtualenv_name>
```

2. Start Virtual Environment
```
$ source <virtualenv_name>/bin/activate
```

3. Install Django using pip
```
(myvenv) ~$ pip3 install django~=1.11.0
```

### Build database

```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```


### Run on Localhost

**Activate virtual environment before running the service**

```bash
$ python3 manage.py runserver
```

### The public link for this website
http://ec2-18-188-178-199.us-east-2.compute.amazonaws.com:8080/home/

Our Final Presentation slide in [here](https://docs.google.com/presentation/d/1rhUF6xPapdNi7tXPnt2-WC6IUncK8Pmji1Rsw6t2hvQ/edit#slide=id.g3928e3aff2_0_112).
Pivotal tracker link is [this](https://www.pivotaltracker.com/n/projects/2166399).
