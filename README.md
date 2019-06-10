
#  Compiler for subset of Golan
Евтушенко Данил 
Группа: ИВ-621
- [x] Лексер
- [x] Парсер
- [x] Таблица символов
- [ ] Кодогенератор
***
# Запуск

```
$ python main.py "name_file" -l  #лексер
$ python main.py "name_file" -p  #парсер
$ python main.py "name_file" -s  #семантика, таблицы
```
> ***Визуализирвоать AST***
> https://vanya.jp.net/vtree/index.html
***
### Синтаксис
- Вначале кода обязательно подключение `package "name"`.
- Используемые типы данных: `int`, `string`.
- Точка с запятой в конце, даже у `{}`.
- Объявление переменных происходит в начале каждого блока.
- Значение переменных задается отдельно от их объявления.
***
### Пример
```
package main;
var i, max int;
var word string;
func poisk() {
	var array [5]int;
	i = 0;
	max = 0;
	array[0] = 23;
	array[1] = 2223;
	array[2] = 213;
	array[3] = 66666;
	array[4] = 2233;
	for (i < 5) {
		if (array[i] > max) {
			max = array[i]
		};
		i = i + 1;
	};
	print(max);
};
```
