from random import randint
import requests
import time

class Pokemon:
    pokemons = {}
    cache = {}  # Кэш для данных покемонов
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1, 200)  # Ограничим диапазон для популярных покемонов
        
        # Получаем данные покемона через API
        pokemon_data = self.get_pokemon_data_fast()
        
        # Основные свойства
        self.name = pokemon_data['name']
        self.img = pokemon_data['img']
        self.hp = pokemon_data['hp']
        self.attack = pokemon_data['attack'] 
        self.defense = pokemon_data['defense']
        self.type = pokemon_data['type']
        self.level = 1
        self.experience = 0
        
        Pokemon.pokemons[pokemon_trainer] = self

    def get_pokemon_data_fast(self):
        """Быстрое получение данных покемона с кэшированием"""
        # Проверяем кэш
        if self.pokemon_number in Pokemon.cache:
            return Pokemon.cache[self.pokemon_number]
        
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        
        try:
            # Добавляем таймаут для быстрого ответа
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                
                # Получаем только основные данные
                pokemon_data = {
                    'name': data['name'],
                    'img': data['sprites']['front_default'],
                    'hp': data['stats'][0]['base_stat'],  # HP
                    'attack': data['stats'][1]['base_stat'],  # Attack
                    'defense': data['stats'][2]['base_stat'],  # Defense
                    'type': data['types'][0]['type']['name']  # Первый тип
                }
                
                # Сохраняем в кэш
                Pokemon.cache[self.pokemon_number] = pokemon_data
                return pokemon_data
            else:
                # Если ошибка API - возвращаем дефолтного покемона
                return self.get_default_data()
                
        except Exception as e:
            print(f"Ошибка API: {e}")
            return self.get_default_data()

    def get_default_data(self):
        """Данные по умолчанию при ошибке"""
        return {
            'name': 'pikachu',
            'img': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',
            'hp': 35,
            'attack': 55,
            'defense': 40,
            'type': 'electric'
        }

    def info(self):
        return f"""Имя твоего покемона: {self.name.capitalize()}
Уровень: {self.level}
Тип: {self.type}
HP: {self.hp}
Атака: {self.attack}
Защита: {self.defense}"""

    def detailed_info(self):
        return f"""🐾 {self.name.capitalize()} 🐾
Уровень: {self.level}
Опыт: {self.experience}/100
Тип: {self.type}

📊 Характеристики:
❤️ HP: {self.hp}
⚔️ Атака: {self.attack}
🛡️ Защита: {self.defense}"""

    def show_img(self):
        return self.img

    def level_up(self):
        self.level += 1
        self.hp += randint(1, 3)
        self.attack += randint(1, 2)
        self.defense += randint(1, 2)
        return f"{self.name.capitalize()} достиг уровня {self.level}! 🎉"

    def add_experience(self, exp):
        self.experience += exp
        if self.experience >= 100:
            self.experience = 0
            return self.level_up()
        return f"{self.name.capitalize()} получил {exp} опыта!"

    def evolve(self):
        # Эволюция - меняем на нового покемона через API
        old_name = self.name
        self.pokemon_number = randint(1, 200)  # Новый случайный покемон
        
        pokemon_data = self.get_pokemon_data_fast()
        
        self.name = pokemon_data['name']
        self.img = pokemon_data['img']
        self.hp = pokemon_data['hp']
        self.attack = pokemon_data['attack']
        self.defense = pokemon_data['defense']
        self.type = pokemon_data['type']
        
        return f"🎊 {old_name.capitalize()} эволюционировал в {self.name.capitalize()}! 🎊"