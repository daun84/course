from models.enums.EnumTribe import EnumTribe
from controllers.iterators.CollectionTribes import CollectionTribes


if __name__ == '__main__':
    my_list = [EnumTribe.Imperius, EnumTribe.Hoodrick]
    my_iterator = CollectionTribes(my_list)

    print(next(my_iterator))
    print(next(my_iterator))
    print(next(my_iterator))
    print(next(my_iterator))
    print(next(my_iterator))
    print(next(my_iterator))
    print(next(my_iterator))
    

