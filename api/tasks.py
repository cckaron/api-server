from .models.position import Position, TypeEnum
from .models.task import Task
from .models.connection import connection
from datetime import datetime

db = connection.db

def addTask(body):  
    """Create a new Task

    :param body: 
    :type body: dict | bytes
    :param task_id: ID of task
    :type task_id: str

    :rtype: None
    """
    
    # if connexion.request.is_json:
    #     body = Task.from_dict(connexion.request.get_json())  
    task = Task(datetime.now())
    task.add()

    accident = Position(
        task_id=task.id, created_at=datetime.now(), 
        type=TypeEnum.Destination, generated_at=None,
        latitude=body['accident_latitude'], longitude=body['accident_longitude'], 
        sequence=1)
    departure = Position(
        task_id=task.id, created_at=datetime.now(), 
        type=TypeEnum.Departure, generated_at=None, 
        latitude=body['departure_latitude'], longitude=body['departure_longitude'], 
        sequence=0)
    destination = Position(
        task_id=task.id, created_at=datetime.now(), 
        type=TypeEnum.Destination, generated_at=None, 
        latitude=body['hospital_latitude'], longitude=body['hospital_longitude'], 
        sequence=2)
    p = [accident, departure, destination]
    db.session.add_all(p)
    db.session.commit()

    return {"taskId":task.id}

def findTask(task_id):  
    """Finds task by id

    :param task_id: ID of task that needs to be found. ID was generated By Server.
    :type task_id: str

    :rtype: Task
    """
    positions = Position.findDepartureAndDestination(task_id)
    dic = {}
    for position in positions:
        if position.type.value == TypeEnum.Departure.value:
            d = {
                'departure_latitude': position.latitude,
                'departure_longitude': position.longitude
            }
            dic.update(d)
        elif position.type.value == TypeEnum.Destination.value:
            if position.sequence == 1:
                d = {
                    'accident_latitude': position.latitude,
                    'accident_longitude': position.longitude
                }
                dic.update(d)

            elif position.sequence == 2:
                d = {
                    'hospital_latitude': position.latitude,
                    'hospital_longitude': position.longitude
                }
                dic.update(d)
            
    return dic