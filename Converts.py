from users.models import Todotbl


class DBtoObject():
    @staticmethod
    def objTODO(TODO):
        newTODO = Todotbl()
        newTODO.status = TODO.status
        newTODO.priority = TODO.priority
        newTODO.user = TODO.user
        newTODO.name = TODO.name
        newTODO.data_task = TODO.data_task
        newTODO.id = TODO.id
        return newTODO

    @staticmethod
    def listTODOs(TODOs):
        result = list()
        for todo in TODOs:
            result.append(DBtoObject.objTODO(todo))
        return result

    @staticmethod
    def dictTODO(TODO):
        newTODO = {}
        newTODO['status'] = TODO.status
        newTODO['priority'] = TODO.priority
        newTODO['user'] = {
            'email': TODO.user.email,
            'id': TODO.user.id,
        }
        newTODO['name'] = TODO.name
        newTODO['data_task'] = TODO.data_task
        newTODO['id'] = TODO.id
        return newTODO

    @staticmethod
    def dictTODOs(TODOs):
        result = {}
        for i in range(len(TODOs)):
            result[i] = DBtoObject.dictTODO(TODOs[i])
        return result
