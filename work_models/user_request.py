class UserRequest:
    min_price: int
    max_price: int
    min_floor: int
    max_floor: int
    district: str
    room_count: int

    def __str__(self):
        return f"Цена: от {self.min_price} до {self.max_price} рублей; " \
               f"Этаж: от {self.min_floor} до {self.max_floor}; " \
               f"Район: {self.district} район; " \
               f"Кол-во комнат: {self.room_count};  " \
               f"Пример запроса в систему: <{self.room_count}, от {self.min_price} до {self.max_price}, " \
               f"от {self.min_floor} до {self.max_floor} > "
