class Flat:
    price: str
    address: str
    district: str
    upper_address: str
    area: str
    floor: str
    link: str
    image_url: str

    def __str__(self):
        return f"{str(self.price.replace('/мес.', ''))} руб/мес. \n" \
               f"Количество комнат: {self.address} \n" \
               f"{self.upper_address} \n" \
               f"Площадь: {self.area}; {self.floor} \n" \
               f"{self.district} \n" \
               f"Ссылка на основной ресурс:{self.link}."
