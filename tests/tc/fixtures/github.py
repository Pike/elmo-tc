# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


@pytest.fixture
def repository(user):
    return {
        "id": 213916662,
        "name": "elmo-taskcluster",
        "full_name": "mozilla-services/elmo-taskcluster",
        "html_url": "https://api.github.com/repos/mozilla-services/elmo-taskcluster",
        "url": "https://api.github.com/repos/mozilla-services/elmo-taskcluster",
        "owner": user,
        "default_branch": "master",
    }


@pytest.fixture
def user():
    return {
        "login": "Codertocat",
        "id": 21031067,
        "node_id": "MDQ6VXNlcjIxMDMxMDY3",
        "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/Codertocat",
        "html_url": "https://github.com/Codertocat",
        "followers_url": "https://api.github.com/users/Codertocat/followers",
        "following_url": "https://api.github.com/users/Codertocat/following{/other_user}",
        "gists_url": "https://api.github.com/users/Codertocat/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/Codertocat/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/Codertocat/subscriptions",
        "organizations_url": "https://api.github.com/users/Codertocat/orgs",
        "repos_url": "https://api.github.com/users/Codertocat/repos",
        "events_url": "https://api.github.com/users/Codertocat/events{/privacy}",
        "received_events_url": "https://api.github.com/users/Codertocat/received_events",
        "type": "User",
        "site_admin": False,
    }


@pytest.fixture(params=['refs/heads/master', 'refs/heads/wip'])
def push_event(request, repository, user):
    return {
        "ref": request.param,
        "before": "6113728f27ae82c7b1a177c8d03f9e96e0adf246",
        "after": "0000000000000000000000000000000000000000",
        "created": False,
        "deleted": True,
        "forced": False,
        "base_ref": None,
        "compare": "https://github.com/Codertocat/Hello-World/compare/6113728f27ae...000000000000",
        "commits": [],
        "head_commit": None,
        "repository": repository,
        "pusher": {
            "name": "Codertocat",
            "email": "21031067+Codertocat@users.noreply.github.com",
        },
        "sender": user,
    }

