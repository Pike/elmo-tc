import pytest
from jsonschema import validators


def ensure_schema():
    schema = {
        "$id": "https://firefox-ci-tc.services.mozilla.com/schemas/common/metaschema.json#",
        "$schema": "http://json-schema.org/draft-06/schema#",
        "allOf": [
            {"$ref": "http://json-schema.org/draft-06/schema#"},
            {"$ref": "#/definitions/schema"},
        ],
        "definitions": {
            "recurse": {
                "properties": {
                    "additionalItems": {"$ref": "#/definitions/schema"},
                    "additionalProperties": {"$ref": "#/definitions/schema"},
                    "allOf": {"$ref": "#/definitions/schemaArray"},
                    "anyOf": {"$ref": "#/definitions/schemaArray"},
                    "contains": {"$ref": "#/definitions/schema"},
                    "definitions": {
                        "additionalProperties": {"$ref": "#/definitions/schema"}
                    },
                    "dependencies": {
                        "additionalProperties": {
                            "anyOf": [
                                {"$ref": "#/definitions/schema"},
                                {
                                    "$ref": "http://json-schema.org/draft-06/schema#/definitions/stringArray"
                                },
                            ]
                        }
                    },
                    "items": {
                        "anyOf": [
                            {"$ref": "#/definitions/schema"},
                            {"$ref": "#/definitions/schemaArray"},
                        ]
                    },
                    "not": {"$ref": "#/definitions/schema"},
                    "oneOf": {"$ref": "#/definitions/schemaArray"},
                    "patternProperties": {
                        "additionalProperties": {"$ref": "#/definitions/schema"}
                    },
                    "properties": {
                        "additionalProperties": {"$ref": "#/definitions/schema"}
                    },
                    "propertyNames": {"$ref": "#/definitions/schema"},
                }
            },
            "requiredProperties": {
                "dependencies": {
                    "items": ["type", "uniqueItems"],
                    "properties": ["type", "additionalProperties", "required"],
                }
            },
            "schema": {
                "allOf": [
                    {"$ref": "#/definitions/recurse"},
                    {"$ref": "#/definitions/requiredProperties"},
                ]
            },
            "schemaArray": {
                "items": {"$ref": "#/definitions/schema"},
                "type": "array",
                "uniqueItems": False,
            },
        },
        "description": "This is a refinement of JSON-schema, with the following changes:\n\n  * if `properties` is present, `type` and `additionalProperties` must be present, too\n  * if `entries` is present, `type` and `uniqueItems` must be present, too\n\nNote that any schema that validates against this metaschema will also\nvalidate against the upstream draft-06 metaschema, and is usable by any\nJSON-schema tool.\n",
        "title": "Taskcluster JSON-Schema Meta-Schema, with some stricter validation",
    }
    if schema["$id"] not in validators.meta_schemas:
        pass


@pytest.fixture
def create_task_schema():
    return {
        "$id": "https://firefox-ci-tc.services.mozilla.com/schemas/queue/v1/create-task-request.json#",
        "$schema": "https://firefox-ci-tc.services.mozilla.com/schemas/common/metaschema.json#",
        "additionalProperties": False,
        "description": "Definition of a task that can be scheduled\n",
        "properties": {
            "created": {
                "description": "Creation time of task",
                "format": "date-time",
                "title": "Created",
                "type": "string",
            },
            "deadline": {
                "description": "Deadline of the task, `pending` and `running` runs are\nresolved as **exception** if not resolved by other means\nbefore the deadline. Note, deadline cannot be more than\n5 days into the future\n",
                "format": "date-time",
                "title": "Deadline",
                "type": "string",
            },
            "dependencies": {
                "$ref": "task.json#/properties/dependencies",
                "default": [],
            },
            "expires": {"$ref": "task.json#/properties/expires"},
            "extra": {"$ref": "task.json#/properties/extra", "default": {}},
            "metadata": {"$ref": "task-metadata.json#"},
            "payload": {"$ref": "task.json#/properties/payload", "default": []},
            "priority": {"$ref": "task.json#/properties/priority", "default": "lowest"},
            "provisionerId": {"$ref": "task.json#/properties/provisionerId"},
            "requires": {
                "$ref": "task.json#/properties/requires",
                "default": "all-completed",
            },
            "retries": {"$ref": "task.json#/properties/retries", "default": 5},
            "routes": {"$ref": "task.json#/properties/routes", "default": []},
            "schedulerId": {
                "$ref": "task.json#/properties/schedulerId",
                "default": "-",
            },
            "scopes": {"$ref": "task.json#/properties/scopes", "default": []},
            "tags": {"$ref": "task.json#/properties/tags", "default": {}},
            "taskGroupId": {"$ref": "task.json#/properties/taskGroupId"},
            "workerType": {"$ref": "task.json#/properties/workerType"},
        },
        "required": [
            "provisionerId",
            "workerType",
            "created",
            "deadline",
            "payload",
            "metadata",
        ],
        "title": "Task Definition Request",
        "type": "object",
    }


@pytest.fixture
def payload_schema():
    return {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "definitions": {
            "artifact": {
                "type": "object",
                "properties": {
                    "type": {
                        "title": "Artifact upload type.",
                        "type": "string",
                        "enum": ["file", "directory"],
                    },
                    "path": {
                        "title": "Location of artifact in container.",
                        "type": "string",
                    },
                    "expires": {
                        "title": "Date when artifact should expire must be in the future.",
                        "type": "string",
                        "format": "date-time",
                    },
                },
                "required": ["type", "path"],
            }
        },
        "title": "Docker worker payload",
        "description": "`.payload` field of the queue.",
        "type": "object",
        "required": ["image", "maxRunTime"],
        "properties": {
            "log": {
                "title": "Custom log location",
                "description": "Specifies a custom location for the livelog artifact",
                "type": "string",
            },
            "image": {
                "title": "Docker image.",
                "description": "Image to use for the task.  Images can be specified as an image tag as used by a docker registry, or as an object declaring type and name/namespace",
                "oneOf": [
                    {"title": "Docker image name", "type": "string"},
                    {
                        "type": "object",
                        "title": "Named docker image",
                        "properties": {
                            "type": {"type": "string", "enum": ["docker-image"]},
                            "name": {"type": "string"},
                        },
                        "required": ["type", "name"],
                    },
                    {
                        "type": "object",
                        "title": "Indexed docker image",
                        "properties": {
                            "type": {"type": "string", "enum": ["indexed-image"]},
                            "namespace": {"type": "string"},
                            "path": {"type": "string"},
                        },
                        "required": ["type", "namespace", "path"],
                    },
                    {
                        "type": "object",
                        "title": "Docker image artifact",
                        "properties": {
                            "type": {"type": "string", "enum": ["task-image"]},
                            "taskId": {"type": "string"},
                            "path": {"type": "string"},
                        },
                        "required": ["type", "taskId", "path"],
                    },
                ],
            },
            "cache": {
                "title": "Caches to mount point mapping.",
                "description": 'Caches are mounted within the docker container at the mount point specified. Example: ```{ "CACHE NAME": "/mount/path/in/container" }```',
                "type": "object",
            },
            "capabilities": {
                "title": "Capabilities that must be available/enabled for the task container.",
                "description": 'Set of capabilities that must be enabled or made available to the task container Example: ```{ "capabilities": { "privileged": true }```',
                "type": "object",
                "properties": {
                    "privileged": {
                        "title": "Privileged container",
                        "description": "Allows a task to run in a privileged container, similar to running docker with `--privileged`.  This only works for worker-types configured to enable it.",
                        "type": "boolean",
                        "default": False,
                    },
                    "devices": {
                        "title": "Devices to be attached to task containers",
                        "description": "Allows devices from the host system to be attached to a task container similar to using `--device` in docker. ",
                        "type": "object",
                        "properties": {
                            "loopbackVideo": {
                                "title": "Loopback Video device",
                                "description": "Video loopback device created using v4l2loopback.",
                                "type": "boolean",
                            },
                            "loopbackAudio": {
                                "title": "Loopback Audio device",
                                "description": "Audio loopback device created using snd-aloop",
                                "type": "boolean",
                            },
                        },
                    },
                },
            },
            "command": {
                "title": "Docker command to run (see docker api).",
                "type": "array",
                "items": {"type": "string"},
                "default": [],
                "description": "Example: `['/bin/bash', '-c', 'ls']`.",
            },
            "env": {
                "title": "Environment variable mappings.",
                "description": 'Example: ```\n{\n  "PATH": \'/borked/path\' \n  "ENV_NAME": "VALUE" \n}\n```',
                "type": "object",
            },
            "maxRunTime": {
                "type": "number",
                "title": "Maximum run time in seconds",
                "description": "Maximum time the task container can run in seconds",
                "multipleOf": 1,
                "minimum": 1,
                "maximum": 86400,
            },
            "onExitStatus": {
                "title": "Exit status handling",
                "description": "By default docker-worker will fail a task with a non-zero exit status without retrying.  This payload property allows a task owner to define certain exit statuses that will be marked as a retriable exception.",
                "type": "object",
                "properties": {
                    "retry": {
                        "title": "Retriable exit statuses",
                        "description": "If the task exists with a retriable exit status, the task will be marked as an exception and a new run created.",
                        "type": "array",
                        "items": {"title": "Exit statuses", "type": "number"},
                    },
                    "purgeCaches": {
                        "title": "Purge caches exit status",
                        "description": "If the task exists with a purge caches exit status, all caches associated with the task will be purged.",
                        "type": "array",
                        "items": {"title": "Exit statuses", "type": "number"},
                    },
                },
            },
            "artifacts": {
                "type": "object",
                "title": "Artifacts",
                "description": 'Artifact upload map example: ```{"public/build.tar.gz": {"path": "/home/worker/build.tar.gz", "expires": "2016-05-28T16:12:56.693817Z", "type": "file"}}```',
                "additionalProperties": {"$ref": "#/definitions/artifact"},
            },
            "supersederUrl": {
                "title": "URL of the a service that can indicate tasks superseding this one; the current taskId will be appended as a query argument `taskId`.  The service should return an object with a `supersedes` key containing a list of taskIds, including the supplied taskId.  The tasks should be ordered such that each task supersedes all tasks appearing earlier in the list.  See [superseding](/docs/reference/platform/taskcluster-queue/docs/superseding) for more detail.",
                "type": "string",
                "format": "uri",
                "pattern": "^https?://[\\x20-\\x7e]*$",
            },
            "features": {
                "title": "Feature flags",
                "description": "Used to enable additional functionality.",
                "type": "object",
                "properties": {
                    "localLiveLog": {
                        "type": "boolean",
                        "title": "Enable live logging (worker local)",
                        "description": "Logs are stored on the worker during the duration of tasks and available via http chunked streaming then uploaded to s3",
                    },
                    "bulkLog": {
                        "type": "boolean",
                        "title": "Bulk upload the task log into a single artifact",
                        "description": "Useful if live logging is not interesting but the overalllog is later on",
                    },
                    "taskclusterProxy": {
                        "type": "boolean",
                        "title": "Task cluster auth proxy service",
                        "description": "The auth proxy allows making requests to taskcluster/queue and taskcluster/scheduler directly from your task with the same scopes as set in the task. This can be used to make api calls via the [client](https://github.com/taskcluster/taskcluster-client) CURL, etc... Without embedding credentials in the task.",
                    },
                    "balrogVPNProxy": {
                        "type": "boolean",
                        "title": "Balrog proxy service",
                        "description": "The Balrog proxy feature allows tasks to make requests to http://balrog which is a proxied connection through a vpn tunnel to production balrog update server.",
                    },
                    "balrogStageVPNProxy": {
                        "type": "boolean",
                        "title": "Balrog stage proxy service",
                        "description": "The Balrog stage proxy feature allows tasks to make requests to http://balrog which is a proxied connection through a vpn tunnel to the stage balrog update server.",
                    },
                    "artifacts": {
                        "type": "boolean",
                        "title": "Artifact uploads",
                        "description": "",
                    },
                    "dind": {
                        "type": "boolean",
                        "title": "Docker in Docker",
                        "description": "Runs docker-in-docker and binds `/var/run/docker.sock` into the container. Doesn't allow privileged mode, capabilities or host volume mounts.",
                    },
                    "relengAPIProxy": {
                        "type": "boolean",
                        "title": "Releng API proxy service",
                        "description": "The Releng API proxy service allows tasks to talk to releng api using an authorization token based on the task's scopes",
                    },
                    "dockerSave": {
                        "type": "boolean",
                        "title": "Docker save",
                        "description": "Uploads docker images as artifacts",
                    },
                    "interactive": {
                        "type": "boolean",
                        "title": "Docker Exec Interactive",
                        "description": "This allows you to interactively run commands inside the container and attaches you to the stdin/stdout/stderr over a websocket. Can be used for SSH-like access to docker containers.",
                    },
                    "allowPtrace": {
                        "type": "boolean",
                        "title": "Allow ptrace within the container",
                        "description": "This allows you to use the Linux ptrace functionality inside the container; it is otherwise disallowed by Docker's security policy. ",
                    },
                    "chainOfTrust": {
                        "type": "boolean",
                        "title": "Enable generation of ed25519-signed Chain of Trust artifacts",
                        "description": "Artifacts named chain-of-trust.json and chain-of-trust.json.sig should be generated which will include information for downstream tasks to build a level of trust for the artifacts produced by the task and the environment it ran in.",
                    },
                },
            },
        },
    }


@pytest.fixture
def taskcluster_yml_v1_schema():
    return {
        "$id": "https://firefox-ci-tc.services.mozilla.com/schemas/github/v1/taskcluster-github-config.v1.json#",
        "$schema": "https://firefox-ci-tc.services.mozilla.com/schemas/common/metaschema.json#",
        "additionalProperties": False,
        "description": "Description of a taskcluster.yml file v1, which may be used to generate a taskgraph\nand tasks.\n",
        "properties": {
            "policy": {
                "pullRequests": {
                    "description": "Policy for creating tasks for pull requests.  The effective policy is found in this property\nin the `.taskcluster.yml` file in the repository's default branch.  See the documentation for\ndetailed definition of the options.\n",
                    "enum": ["public", "collaborators"],
                    "type": "string",
                }
            },
            "reporting": {
                "description": "Policy for reporting status of PR or a commit. If absent, Github Statuses API is used",
                "enum": ["checks-v1"],
                "type": "string",
            },
            "tasks": {
                "default": [],
                "description": "Definitions of tasks that can be scheduled. Rendered with JSON-e\n",
                "oneOf": [
                    {
                        "description": "Each element of this should evaluate to a task definition via json-e",
                        "items": {"additionalProperties": True, "type": "object"},
                        "type": "array",
                        "uniqueItems": False,
                    },
                    {
                        "additionalProperties": True,
                        "description": "This must evaluate to an array via json-e i.e. `$flatten`",
                        "type": "object",
                    },
                ],
                "title": 'Task definition template"',
            },
            "version": {
                "description": "Version of the format of this file; must be 1",
                "enum": [1],
                "type": "integer",
            },
        },
        "required": ["version"],
        "title": ".taskcluster.yml format",
        "type": "object",
    }
