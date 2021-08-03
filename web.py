import os
from string import Template

from flask import request, jsonify

from helpers import query, update, log, generate_uuid
from escape_helpers import sparql_escape_uri, sparql_escape_string, sparql_escape_int, sparql_escape_datetime


@app.route('/jobs/new', methods=["GET"])
def create_job():
    """
    Build a job request and store in triple store
    :return: Success if correctly created
    """
    source = request.args.get("source")
    task = request.args.get("task")
    description = request.args.get("description") or "New job created"

    job_id = generate_uuid()
    q = Template("""
    PREFIX mu: <http://mu.semte.ch/vocabularies/ext/>
    PREFIX status: <http://mu.semte.ch/vocabularies/ext/status#>
    INSERT DATA {
        GRAPH $graph {
            $job a mu:Job;
                mu:uuid $uuid ;
                <http://purl.org/dc/terms/description> $description;
                mu:source $source;
                mu:task $task;
                mu:status status:queued .
        }
    }
    """).substitute(
        graph=sparql_escape_uri("http://mu.semte.ch/application"),
        uuid=sparql_escape_string(job_id),
        job=sparql_escape_uri("http://mu.semte.ch/job/" + job_id),
        source=sparql_escape_string(source),
        task=sparql_escape_string(task),
        description=sparql_escape_string(description),
    )

    update(q)

    return "Success", 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    """
    Default endpoint/ catch all
    :param path: requested path
    :return: debug information
    """
    return 'You want path: %s' % path, 404


if __name__ == '__main__':
    debug = os.environ.get('MODE') == "development"
    app.run(debug=debug, host='0.0.0.0', port=80)
