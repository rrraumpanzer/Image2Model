**Запуск**


``poetry shell``


``poetry update``


``uvicorn image2model.__main__:app --host 0.0.0.0 --port 8000``

*Несмотря на то, что имеется код для перезапуска сервера при изменении файла, чтобы запросы к ним работали, его нужно перезапустить вручную и я не понимаю почему*

**Проверка эндпоинтов:**


Для изображения:

``curl -X POST -F 'image=@test_image.jpg' http://localhost:8000/image``


``curl -o image.jpg http://localhost:8000/image`` *Сохранит результат GET запроса в image.jpg*
 
Для координат объекта:


``http POST localhost:8000/post_coords <<<'{ "x": 100, "y": 100 }'``


``http GET localhost:8000/get_coords``

/// Для сегментации надо установить refiners через pip
/// Результат в output.png
/// Нужно отредактировать эндпоинт координат для передачи баундинг бокса объекта (левый верхний, правый нижний углы)
``pip install git+https://github.com/finegrain-ai/refiners``