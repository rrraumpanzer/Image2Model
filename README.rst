<h3>**Запуск**</h3>


``poetry shell``


``poetry update``


``uvicorn image2model.__main__:app --host 0.0.0.0 --port 8000``

*Несмотря на то, что имеется код для перезапуска сервера при изменении файла, чтобы запросы к ним работали, его нужно перезапустить вручную и я не понимаю почему*

<h3>**Проверка эндпоинтов:**</h3>


<h4>Для изображения:</h4>

``curl -X POST -F 'image=@test_image.jpg' http://localhost:8000/image``


``curl -o image.jpg http://localhost:8000/image`` *Сохранит результат GET запроса в image.jpg*
 
<h4>Для координат объекта:</h4>


``http POST localhost:8000/post_coords <<<'{ "x": 100, "y": 100 }'``


``http GET localhost:8000/get_coords``