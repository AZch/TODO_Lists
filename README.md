# TODO task sheet
### Opportunities:
#### 1. User registration (administrator and simple user)
#### 1.1. The administrator sees all TODO, the user sees only his
#### 2. Authorization and subsequent requests are implemented using the django rest framework and JWT (Bearer Token) (token token every 14 days)
#### 3. There is the ability to filter existing TODOs by priority and status

Possible API requests (all information is transmitted through the body (specify content-type: application / json in the header)):
1. / user / create / (only post) - create a user. Parameters: email, password; Optional: role
2. / user / obtain_token / (only post) - user authorization. Parameters: email, password. Will return the user's email, his role and authorization token.
3. / user / update / - update user information (only authorized users)
    3. get Updates the user token and returns it
    3. put updates user information ({'user': {'email': 'new_email', ...}} is passed)
4. / user / todo / - interaction with TODO (only authorized users)
    4. post - adding a new TODO name field is required
    4. get - getting all TODO user (for administrator all TODO)
    4. put - change the user's TODO (all the information about TODO that is displayed on a get request is needed)
    4. delete - delete one user TODO (the necessary parameter id TODO which will be deleted)
5. / user / filter / (only get) - filtering and sorting TODO (only authorized users). As a parameter, you must pass a string in which the filter and sorting will be described:
> {
> 'column': 'priority> = 2,prioritydesc'
>}

where, means "and".
The following variations and the like are also possible:
> priorityasc, priority <5, statusasc, statusdesc, status = new, ...

In the file WordConst.py, the indicated statuses and roles are indicated (there is only one role in this case (admin))