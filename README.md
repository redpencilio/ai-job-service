# ai-job-service

A docker container to create new jobs that have to be executed.

## Info

The jobs service offers the possibility to create jobs that have to be executed based on a specific naming of

* task: the task that has to be performed
* source: id of the file that is obtained after converting the data using
  the [ai-data-importer-service](https://github.com/redpencilio/ai-data-importer-service)

## Getting started

```yml
services:
  jobs:
    image: redpencil/ai-job
    links:
      - db:database
    environment:
      LOG_LEVEL: "debug"
      MODE: "production"
```

## Reference

### Environment variables

- `LOG_LEVEL` takes the same options as defined in the
  Python [logging](https://docs.python.org/3/library/logging.html#logging-levels) module.


- `MU_SPARQL_ENDPOINT` is used to configure the SPARQL query endpoint.

    - By default this is set to `http://database:8890/sparql`. In that case the triple store used in the backend should
      be linked to the microservice container as `database`.
      

- `MU_SPARQL_UPDATEPOINT` is used to configure the SPARQL update endpoint.

    - By default this is set to `http://database:8890/sparql`. In that case the triple store used in the backend should
      be linked to the microservice container as `database`.


- `MU_APPLICATION_GRAPH` specifies the graph in the triple store the microservice will work in.

    - By default this is set to `http://mu.semte.ch/application`. The graph name can be used in the service
      via `settings.graph`.


- `MU_SPARQL_TIMEOUT` is used to configure the timeout (in seconds) for SPARQL queries.

### Endpoints

#### `GET /jobs/new`: create a new job

Arguments:

- source: id of the file that is obtained after converting the data using the [ai-data-importer-service](https://github.com/redpencilio/ai-data-importer-service) service
- task: the task that has to be performed
- description: description of the job