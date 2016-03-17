# Mahuri(Honey Bees) - HTTP Load Testing

> A HTTP load testing tool which is useful to load test the RESTful APIs.

### Introduction

This was quick and dirty hack to get http load testing with locust up and running for our use case. I believe this might be use case for others too. This wrapper on top of [Locust](http://locust.io/) can perform stress tests against GET, POST, DELETE and PUT endpoints with equal weight. You can create a simple json based configuration to get the stress test up and running.

### Installation

Make sure you have a python 2.x setup and available on your system. Clone this repo and then perform pip install. You should be able to get a working environment for running load testing by then.

```shell
$ git clone https://github.com/techgaun/mahuri.git
$ cd mahuri
$ pip install -r requirements.txt
```

The virtualenv based installation is highly recommended.

### Configuration

The configuration of the environment to be load tested and the API endpoints are all specified in a config file in a json format. The sample config.json file is available with this tool itself. You just have to create your own config.json for the test. Please note that you have to escape your json payloads at the moment or you can specify them via `bodyFile` key as in example below.

Typically, config json file consists of following key-value pairs.

```json
{
  "host": "https://some-micro-service.tld",
  "token": "<auth_token_if_any>",
  "gets": [
    "/",
    "/api/v1/current?latitude=39.0997&longitude=94.5783",
    "/api/v1/forecast?latitude=38.7145&longitude=94.5783&forecast=daily"
  ],
  "posts": [
    {
      "endpoint": "/",
      "content-type": "application/json",
      "body": "[\"name\": \"Samar\"]"
    },
    {
      "endpoint": "/api/v1/pearl",
      "content-type": "application/json",
      "bodyFile": "pearl.json"
    },
    {
      "endpoint": "/v1/tags/firmware",
      "content-type": "multipart/form-data",
      "payload": {
        "softwareFile": "samar01.zip"
      }
    },
    {
      "endpoint": "/v1/users/login",
      "content-type": "application/x-www-form-urlencoded",
      "payload": {
        "email": "coolsamar@nepal.tld",
        "password": "hell0n3pal"
      }
    }
  ],
  "puts": [
    {
      "endpoint": "/",
      "content-type": "application/json",
      "body": "{\"msg\": \"update\"}"
    },
    {
      "endpoint": "/user",
      "content-type": "application/json",
      "body": "{\"msg\": \"update\"}"
    }
  ],
  "deletes": [
    {
      "endpoint": "/user",
      "content-type": "application/json",
      "body": "{\"msg\": \"delete\"}"
    }
  ]
}
```

- You need to specify the host you're going to test with the `host` key. This is very critical.
- You can specify token for passing through Authorization header using the `token` key.
- You can pass the list of get endpoints as an array with `gets` key.
- You can pass the list of post endpoints with associated content-type and payloads with `posts` key. See config above for clarity.
- You can pass the list of put endpoints with associated content-type and payloads with `puts` key. See config above for clarity.
- You can pass the list of delete endpoints with associated content-type and payloads with `deletes` key. See config above for clarity.

To use the framework in a distributed manner with good performance, you need to make use of pyzmq. Since we will be using it by default in distributed mode, I have included it as the dependency.


By default, the port 5557 must be open for this to work successfully.

### Usage

#### Single mode
Just run the locust command and specify the file for locust to pick up.
```shell
$ locust -f main.py
```

#### Master
We start one instance of locust as master and the master will show us the live statistics. We will access the web console via the master's IP address.
```shell
$ locust -f main.py --master
```

#### Slave
The slaves are started with --slave flag and we need to specify the master's IP address or hostname.
```shell
$ locust -f main.py --slave --master-host=<master_host_ip_or_domain>
```

Finally, browse to your web console using appropriate IP. Eg: http://localhost:8089/

### Graphing

You can graph the results of the load tests using any of the graphing tools such as d3.js, matplotlib, excel, etc.

If you're using matplotlib, you might need appropriate dependencies. The modern standard distributions mostly complain about freetype which you can fix for eg. in Ubuntu by install `libfreetype6-dev`.

We've a graphing ability added to mahuri which was basically taken from [this post](http://qszhuan.github.io/test/2013/12/23/using-matplotlib-to-analyse-locust-performance-test-results). The current graphing ability provides following functionalities:
- Bar graph of median response time from request/response csv
- Request count bar chart
- Response time distribution against request counts

#### Commands
```shell
$ python graphs/bar.py -s /tmp/requests.csv # requests.csv needs to be downloaded from Locust UI
$ python graphs/trend.py
```

Please refer to the [screenshots](#Screenshots) section for more details.

### Screenshots

![Locust UI](images/screenshot.png?raw=true "Locust UI")

![Median Response Time](images/median.png?raw=true "Median Response Time")

![Response Distribution](images/response_count.png?raw=true "Response Distribution")


### To Dos
- ~~Add easier support for POST, DELETE and PUT~~
- Add params based dynamic URL generation
- Add support for cookie based authentication along with Authorization header

### Author
- Maintained By Samar Acharya
