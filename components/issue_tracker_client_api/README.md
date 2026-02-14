# Issue Tracker API

## Overview
```issue_tracker_client_api``` defines the ```Client``` abstract base class that every issue tracker client must implement. The package contains the abstraction, a factory hook, and no concrete logic.

## Purpose
 - Document the operations available to consumers.
 - Provide a single factory (```get_client```) that implementations can override.
  - Keep issue-type dependencies explicit through the ```issue_tracker_client_api.issue``` module.

## Architecture

### Component Design
The package exposes one abstract base class focused on issue tracking operations - CRUD, assign priority, assign leader, assign status, etc. It depends only on the ```Issue``` abstraction.

### API Integration
```
from issue_tracker_client_api import Client, get_client
from issue_tracker_client_api.issue import Issue

client: Client = get_client()
for issue in client.get_issues(max_issues = 5):
    title: str = issue.title
```

### Dependency Injection
Implementation packages (for example ```trello_client_impl```) replace the factory at import time:
```
import trello_client_impl # rebinds issue_tracker_client_api.get_client
from issue_tracker_client_api import get_client
client = get_client(interactive=False)
```

## API Reference
### Client Abstract Base Class
```
class Client(ABC):
    ...
```

#### Methods
 - ```get_issue(issue_id: str) -> Issue```: Return a single issue
 - ```delete_issue(issue_id: str) -> bool```: Remove the issue from the board
 - ```assign_priority(issue_id: str, priority: str) -> bool```: Assign priority label to issue

 - ```assign_leader(issue_id: str, leader: str) -> bool```: Assign leader to issue
 - ```assign_status(issue_id: str, status: str) -> bool```: Assign status to issue
 - ```get_issues(max_issues: int = 10) -> Iterator[Issue]```: Yield issues lazily

 ### Factory Function
 ```get_client(*, interactive: bool = False) -> Client```: Returns the bound implementation or raises ```NotImplementedError``` if none registered.

 ## Usage Examples

 ### Basic Operations

 ```
 from issue_tracker_client_api import get_client

 client = get_client(interactive=False)
 for issue in client.get_issues(max_issues=3):
    print(f"{issue.id}: {issue.title}")
 ```

 ### Issue Management
 ```
 from issue_tracker_client_api import get_client

 client = get_client()
 initial_issue = client.get_issue("first_issue_of_our_project")
 client.assign_priority(initial_issue.id)
 ```

 ## Implementation Checklist
 1. Implement every method in the abstract base class.
 2. Return objects compatible with issue_tracker_client_api.issue.Issue
 3. Publish a factory (```get_client_impl```) and assign it to issue_tracker_client_api.get_client
 4. Honor the ```interactive``` flag (prompting only when ```True```)

 ## Testing
 ```
 uv run pytest src/issue_tracker_client_api/tests/ -q
 uv run pytest src/issue_tracker_client_api/tests/ --cov=src/issue_tracker_client_api --cov-report=term-missing
 ```