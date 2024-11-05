Запуск
poetry shell
uvicorn image2model.__main__:app --host 0.0.0.0 --port 8000

Несмотря на то, что имеется код для перезапуска сервера при изменении файла, чтобы запросы к ним работали, его нужно перезапустить вручную и я не понимаю почему

Проверка эндпоинтов:
http --verbose -form POST localhost:8000/image file@test_image.jpg             unprocessable entity?????

http POST localhost:8000/post_coords <<<'{ "x": 100, "y": 100 }'
http GET localhost:8000/get_coords