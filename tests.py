from main import BooksCollector
import pytest

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_rating()) == 2 #Этот тест Failed, потому что нет метода get_books_rating

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    
    def test_set_book_genre(self):
        #Тест установки жанра для книги
        collector = BooksCollector()
        collector.add_new_book('Мастер и Маргарита')
        collector.set_book_genre('Мастер и Маргарита', 'Фантастика')
        assert collector.get_book_genre('Мастер и Маргарита') == 'Фантастика'

    def test_get_book_genre(self):
        #Тест получения жанра книги
        collector = BooksCollector()
        collector.add_new_book('1984')
        collector.set_book_genre('1984', 'Фантастика')
        assert collector.get_book_genre('1984') == 'Фантастика'

    def test_get_books_with_specific_genre(self):
        #Тест получения списка книг с определенным жанром
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_new_book('Книга 3')
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.set_book_genre('Книга 2', 'Фантастика')
        collector.set_book_genre('Книга 3', 'Ужасы')
        
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert len(fantasy_books) == 2
        assert 'Книга 1' in fantasy_books
        assert 'Книга 2' in fantasy_books

    def test_get_books_genre(self):
        #Тест получения словаря всех книг и их жанров
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Фантастика')
        
        books_dict = collector.get_books_genre()
        assert isinstance(books_dict, dict)
        assert len(books_dict) == 2
        assert books_dict['Книга 1'] == 'Фантастика'
        assert books_dict['Книга 2'] == ''

    def test_get_books_for_children(self):
        #Тест получения списка книг, подходящих детям
        collector = BooksCollector()
        collector.add_new_book('Детская книга 1')
        collector.add_new_book('Детская книга 2')
        collector.add_new_book('Взрослая книга')
        collector.set_book_genre('Детская книга 1', 'Мультфильмы')
        collector.set_book_genre('Детская книга 2', 'Комедии')
        collector.set_book_genre('Взрослая книга', 'Ужасы')
        
        children_books = collector.get_books_for_children()
        assert len(children_books) == 2
        assert 'Детская книга 1' in children_books
        assert 'Детская книга 2' in children_books
        assert 'Взрослая книга' not in children_books

    def test_add_book_in_favorites(self):
        #Тест добавления книги в избранное
        collector = BooksCollector()
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1
        assert 'Любимая книга' in favorites

    def test_delete_book_from_favorites(self):
        #Тест удаления книги из избранного
        collector = BooksCollector()
        collector.add_new_book('Книга для удаления')
        collector.add_book_in_favorites('Книга для удаления')
        collector.delete_book_from_favorites('Книга для удаления')
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 0

    def test_get_list_of_favorites_books(self):
        #Тест получения списка избранных книг
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_new_book('Книга 3')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Книга 2')
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert 'Книга 1' in favorites
        assert 'Книга 2' in favorites
        assert 'Книга 3' not in favorites

    @pytest.mark.parametrize('book_name, expected_result', [
        ('Война и мир', True),                                    
        ('', False),                                              
        ('Очень длинное название книги которое превышает лимит в сорок символов', False),  
        ('Гарри Поттер', True),                                   
        ('1984', True)                                            
    ])
    def test_add_new_book_parametrized(self, book_name, expected_result):
        #Параметризованный тест добавления книг с различными названиями.
        collector = BooksCollector()
        collector.add_new_book(book_name)
        
        if expected_result:
            assert book_name in collector.get_books_genre(), f"Книга '{book_name}' должна была добавиться"
        else:
            assert book_name not in collector.get_books_genre(), f"Книга '{book_name}' не должна была добавиться"

    @pytest.mark.parametrize('book_name, genre, should_be_in_children_list', [
        ('Детская книга 1', 'Мультфильмы', True),      
        ('Детская книга 2', 'Комедии', True),          
        ('Детская книга 3', 'Фантастика', True),       
        ('Взрослая книга 1', 'Ужасы', False),          
        ('Взрослая книга 2', 'Детективы', False),      
        ('Книга без жанра', '', False),                
    ])
    def test_get_books_for_children_parametrized(self, book_name, genre, should_be_in_children_list):
       # Параметризованный тест проверки возрастного рейтинга книг.
        collector = BooksCollector()
        collector.add_new_book(book_name)
        if genre:
            collector.set_book_genre(book_name, genre)
        
        children_books = collector.get_books_for_children()
        
        if should_be_in_children_list:
            assert book_name in children_books, f"Книга '{book_name}' с жанром '{genre}' должна быть в детском списке"
        else:
            assert book_name not in children_books, f"Книга '{book_name}' с жанром '{genre}' НЕ должна быть в детском списке"

    @pytest.mark.parametrize('book_name, genre, expected_genre', [
        ('Книга 1', 'Фантастика', 'Фантастика'),           
        ('Книга 2', 'Ужасы', 'Ужасы'),                     
        ('Книга 3', 'Комедии', 'Комедии'),                 
        ('Книга 4', 'Несуществующий жанр', ''),            
        ('Несуществующая книга', 'Фантастика', None),      
    ])
    def test_set_and_get_book_genre_parametrized(self, book_name, genre, expected_genre):
        #Параметризованный тест установки и получения жанров книг.
        collector = BooksCollector()
        if book_name != 'Несуществующая книга':
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        
        actual_genre = collector.get_book_genre(book_name)
        assert actual_genre == expected_genre, f"Ожидался жанр '{expected_genre}', получен '{actual_genre}' для книги '{book_name}'"