import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


#проверка получения певого курса
@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    # Act
    response = client.get(f'/courses/{courses[0].id}/')
    # Asssert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses[0].name


#проверка получения списка курсов
@pytest.mark.django_db
def test_get_list_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.get('/courses/')
    #Asssert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


#проверка фильтрации курсов по id
@pytest.mark.django_db
def test_get_filter_id_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.get(f'/courses/?id={courses[0].id}')
    #Asssert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


# # проверка фильтрации курсов по name
@pytest.mark.django_db
def test_get_filter_name_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.get(f'/courses/?name={courses[0].name}')
    #Asssert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


#проверка создания одного курса
@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    student_1 = Student.objects.create(name='student_1', birth_date='2000-02-02')
    #Act
    response = client.post('/courses/', data = {'name': 'course_1', 'students': [student_1.id]})
    #Assert
    assert response.status_code == 201

#проверка обновления курса
@pytest.mark.django_db
def test_patch_course(client, course_factory):
    # Arrange
    student = Student.objects.create(name='student_1', birth_date='2000-02-02')
    course = course_factory(_quantity=1)
    # Act
    response = client.patch(f'/courses/{course[0].id}/', data={'students': [student.id]})
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['students'] == [student.id]


#проверка удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    #Arrange
    course = course_factory(_quantity=1)
    #Act
    response = client.delete(f'/courses/{course[0].id}/')
    #Assert
    assert response.status_code == 204




