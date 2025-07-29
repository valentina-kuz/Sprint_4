from main import BooksCollector
import pytest

@pytest.fixture
def collector():
    #Фикстура, которая создает новый экземпляр BooksCollector для каждого теста
    return BooksCollector()

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
    
    def test_set_book_genre(self, collector):
        #Тест установки жанра для книги
        collector.add_new_book('Мастер и Маргарита')
        collector.set_book_genre('Мастер и Маргарита', 'Фантастика')
        assert collector.books_genre['Мастер и Маргарита'] == 'Фантастика' # Проверяем напрямую в словаре books_genre

    def test_get_book_genre(self, collector):
        #Тест получения жанра книги
        collector.add_new_book('1984')
        assert collector.get_book_genre('1984') == '' # Проверяем получение жанра для книги без жанра

    def test_get_books_with_specific_genre(self, collector):
        #Тест получения списка книг с определенным жанром
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

    def test_get_books_genre(self, collector):
        #Тест получения словаря всех книг и их жанров
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Фантастика')
        
        books_dict = collector.get_books_genre()
        assert isinstance(books_dict, dict)
        assert len(books_dict) == 2
        assert books_dict['Книга 1'] == 'Фантастика'
        assert books_dict['Книга 2'] == ''

    def test_get_books_for_children(self, collector):
        #Тест получения списка книг, подходящих детям
        collector.add_new_book('Детская книга')
        collector.add_new_book('Взрослая книга')
        collector.set_book_genre('Детская книга', 'Мультфильмы')
        collector.set_book_genre('Взрослая книга', 'Ужасы')
        
        children_books = collector.get_books_for_children()
        assert len(children_books) == 1
        assert 'Детская книга' in children_books

    def test_add_book_in_favorites(self, collector):
        #Тест добавления книги в избранное
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1
        assert 'Любимая книга' in favorites

    def test_delete_book_from_favorites(self, collector):
        #Тест удаления книги из избранного
        collector.add_new_book('Книга для удаления')
        collector.add_book_in_favorites('Книга для удаления')
        collector.delete_book_from_favorites('Книга для удаления')
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 0

    def test_get_list_of_favorites_books(self, collector):
        #Тест получения списка избранных книг
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Книга 2')
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert 'Книга 1' in favorites

    @pytest.mark.parametrize('book_name, expected_result', [
        ('Война и мир', True),                                    
        ('', False),                                              
        ('Очень длинное название книги которое превышает лимит в сорок символов', False),  
        ('Гарри Поттер', True),                                   
        ('1984', True)                                            
    ])
    def test_add_new_book_parametrized(self, collector, book_name, expected_result):
        #Параметризованный тест добавления книг с различными названиями.
        collector.add_new_book(book_name)
        
        if expected_result:
            assert book_name in collector.get_books_genre(), f"Книга '{book_name}' должна была добавиться"
        else:
            assert book_name not in collector.get_books_genre(), f"Книга '{book_name}' не должна была добавиться"

    @pytest.mark.parametrize('book_name, genre, expected_genre', [
        ('Книга 1', 'Фантастика', 'Фантастика'),           
        ('Книга 2', 'Ужасы', 'Ужасы'),                     
        ('Книга 3', 'Комедии', 'Комедии'),                 
        ('Книга 4', 'Несуществующий жанр', ''),            
        ('Несуществующая книга', 'Фантастика', None),      
    ])
    def test_set_and_get_book_genre_parametrized(self, collector, book_name, genre, expected_genre):
        #Параметризованный тест установки и получения жанров книг.
        if book_name != 'Несуществующая книга':
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        
        actual_genre = collector.get_book_genre(book_name)
        assert actual_genre == expected_genre, f"Ожидался жанр '{expected_genre}', получен '{actual_genre}' для книги '{book_name}'"