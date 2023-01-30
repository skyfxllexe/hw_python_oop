class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, info: dict):
        self.info = info

    def get_message(self):
        return ('Тип тренировки: '
                f'{self.info["typet"]};\n'
                'Длительность: '
                f'{self.info["duration"]} ч.;\n'
                'Дистанция: '
                f'{self.info["distance"]} км;\n'
                'Ср. скорость: '
                f'{float(self.info["avgspeed"]):.3f} км/ч;\n'
                'Потрачено ккал: '
                f'{float(self.info["cal"]):.3f}.')


M_IN_KM: int = 1000


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Пройденная дистанция."""
        ...

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        ...

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        ...

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        ...


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_distance(self):
        len_step: float = 0.65
        return (self.action * len_step / M_IN_KM)  # в километрах

    def get_mean_speed(self):
        return (self.get_distance() / self.duration)  # км/ч

    def get_spent_calories(self):
        calories_mean_speed_multiplier: int = 18
        calories_mean_speed_shift: float = 1.79
        return ((calories_mean_speed_multiplier
                * (self.get_mean_speed() / 3.6)
                + calories_mean_speed_shift)
                * self.weight / M_IN_KM * self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            {
                "typet": __class__.__name__,
                "duration": self.duration,
                "distance": self.get_distance(),
                "avgspeed": self.get_mean_speed(),
                "cal": self.get_spent_calories()
            })


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self):
        len_step: float = 0.65
        return (self.action * len_step / M_IN_KM)  # в км

    def get_mean_speed(self):
        return (self.get_distance() / self.duration)  # км/ч

    def get_spent_calories(self):
        calories_mean_weight_multiplier: float = 0.035
        calories_mean_speed_shift: float = 0.029
        return ((
            calories_mean_weight_multiplier
            * self.weight
            + ((self.get_mean_speed() / 3.6) ** 2 / self.height)
            * calories_mean_speed_shift * self.weight)
            * self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            {
                "typet": __class__.__name__,
                "duration": self.duration,
                "distance": self.get_distance(),
                "avgspeed": self.get_mean_speed(),
                "cal": self.get_spent_calories()
            })


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_distance(self):
        return (self.lenght_pool * self.count_pool)

    def get_mean_speed(self):
        return (self.get_distance()
                / M_IN_KM / self.duration)

    def get_spent_calories(self):
        calories_mean_speed_multiplier: float = 1.1
        return ((self.get_mean_speed()
                + calories_mean_speed_multiplier) * 2
                * self.weight * self.duration)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            {
                "typet": __class__.__name__,
                "duration": self.duration,
                "distance": self.get_distance(),
                "avgspeed": self.get_mean_speed(),
                "cal": self.get_spent_calories()
            })


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == "SWM":
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    if workout_type == "RUN":
        return Running(data[0], data[1], data[2])
    return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
