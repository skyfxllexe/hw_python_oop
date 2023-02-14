class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, train):
        self.training_type = training_type
        self.duration = train.duration
        self.distance = train.get_distance()
        self.speed = train.get_mean_speed()
        self.calories = train.get_spent_calories()

    def get_message(self):
        types = {
            'SWM': 'Swimming',
            'RUN': 'Running',
            'WLK': 'SportsWalking'
        }
        return (f'Тип тренировки: {types[self.training_type]};\n'
                f'Длительность: {float(self.duration):.3f} ч.;\n'
                f'Дистанция: {float(self.distance):.3f} км;\n'
                f'Ср. скорость: {float(self.speed):.3f} км/ч;\n'
                f'Потрачено ккал: {float(self.calories):.3f}.\n')


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
        """Получить дистанцию в км."""
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: float, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP: float = 0.65

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / M_IN_KM)

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        CMF: int = 18
        CMS: float = 1.79
        return ((CMF * self.get_mean_speed() + CMS)
                * self.weight / M_IN_KM * self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        return InfoMessage("RUN", self)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.LEN_STEP: float = 0.65

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / M_IN_KM)

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        CMF: float = 0.035
        CMS: float = 0.029
        avgSpeed: float = (self.get_mean_speed() / 3.6) ** 2
        return ((CMF * self.weight + (avgSpeed / (self.height / 100))
                 * CMS * self.weight) * self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        return InfoMessage("WLK", self)


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP: float = 1.38

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        CMF: float = 1.1
        return (self.get_mean_speed() + CMF) * 2 * self.weight * self.duration

    def show_training_info(self) -> InfoMessage:
        return InfoMessage("SWM", self)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    if workout_type == 'RUN':
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
