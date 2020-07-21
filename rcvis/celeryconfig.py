""" Celery configuration. """

import os

## Broker settings.
broker_url = 'sqs://'  # pylint: disable=invalid-name

# List of modules to import when the Celery worker starts.
imports = ('visualizer.tasks',)

# No backend - we don't care about the results, we'll update the database
result_backend = None  # pylint: disable=invalid-name

task_annotations = {'tasks.create_movie': {'rate_limit': '1/s'}}

sqs_queue_name = os.environ['SQS_QUEUE_NAME']
if not sqs_queue_name:
    # Otherwise we get a cryptic error message
    raise Exception("No queue name set. Set SQS_QUEUE_NAME.")

broker_transport_options = {
    'queue_name_prefix': sqs_queue_name
}
