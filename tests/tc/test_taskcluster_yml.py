# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jsone
import jsonschema
import slugid


def as_slugid(tid):
    return slugid.nice()


def validate_tasks(rendered_taskcluster_yml, task_schema, payload_schema):
    for task in rendered_taskcluster_yml["tasks"]:
        # According to https://docs.taskcluster.net/docs/reference/integrations/github/taskcluster-yml-v1#result, the tasks
        # will be passed to createTask directly after removing "taskId", so we can validate with the create-task-request schema.
        if "taskId" in task:
            del task["taskId"]

        jsonschema.validate(instance=task, schema=task_schema)
        jsonschema.validate(instance=task["payload"], schema=payload_schema)


def test_push(
    taskcluster_yml,
    push_event,
    taskcluster_yml_v1_schema,
    create_task_schema,
    payload_schema,
):
    rendered_taskcluster_yml = jsone.render(
        taskcluster_yml,
        context={
            "taskcluster_root_url": "https://tc.mozilla.com",
            "tasks_for": "github-push",
            "as_slugid": as_slugid,
            "event": push_event,
        },
    )
    jsonschema.validate(instance=taskcluster_yml, schema=taskcluster_yml_v1_schema)
    expected_decision_tasks = 1 if push_event["ref"].endswith("/master") else 0
    assert len(rendered_taskcluster_yml['tasks']) == expected_decision_tasks
    validate_tasks(rendered_taskcluster_yml, create_task_schema, payload_schema)
