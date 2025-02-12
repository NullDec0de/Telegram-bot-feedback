Данный репозиторий является форком 2020 (?) года от одноименного репозитория с незначительными правками/улучшениями.

Чтобы узнать id чата в котором бот должен работать можно использовать встроенную в Telegram Desktop функцию показа id чатов.
Настройки > Продвинутые настройки > Экспериментальные настройки > show peers IDs in profile
после чего перезапустите приложение.
Внимание! Для групповых чатов в начале ставьте минус!
Например: 582183775 мы записываем как -582183775

## Принцип работы

Сообщения от пользователей копируются методом [copyMessage](https://core.telegram.org/bots/api#copymessage) 
в чат к админу (или админам) с добавлением ID пользователя в виде хэштега, например, #id1234567, к тексту или подписи 
к медиафайлу. Когда администратор отвечает на сообщение, этот хэштег извлекается, парсится и используется в качестве 
получателя.

## Установка 

### Системные требования:
1. Python 3.9 и выше (не нужно при запуске с Docker);
2. Linux (должно работать на Windows, но могут быть сложности с установкой);
3. Systemd (для запуска через systemd);
4. Docker (для запуска с Docker). Старые версии Docker требуют отдельно docker-compose.

### Просто потестировать (не рекомендуется)
1. Клонируйте репозиторий;
2. Перейдите (`cd`) в склонированный каталог и создайте виртуальное окружение Python (Virtual environment, venv);
3. Активируйте venv и установите все зависимости из `requirements.txt`;
4. Скопируйте `env_example` под именем `.env` (с точкой в начале), откройте его и заполните переменные;
5. Внутри активированного venv: `python -m bot`.

### Systemd 
1. Выполните шаги 1-4 из раздела "просто потестировать" выше;
2. Скопируйте `feedback-bot.example.service` в `feedback-bot.service`, откройте и отредактируйте переменные `WorkingDirectory` 
и `ExecStart`;
3. Скопируйте (или создайте симлинк) файла службы в каталог `/etc/systemd/system/`;
4. Активируйте сервис и запустите его: `sudo systemctl enable feedback-bot --now`;
5. Проверьте, что сервис запустился: `systemctcl status feedback-bot` (можно без root-прав).